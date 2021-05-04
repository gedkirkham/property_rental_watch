from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, CreateView
from django.db.models import Avg
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, QueryDict
from django.utils.translation import gettext_lazy as _

from .models import Address, AddressLookup
from reviews.models import Review
from .forms import AddressLookupForm, AddressCreateForm, country_choices

from geopy.geocoders import Nominatim


class AddressDetailView(DetailView):
    model = Address
    template_name = "addresses/address_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.filter(
            address=self.object, user__isnull=False)
        context["reviews"] = reviews
        context["average_rating"] = reviews.aggregate(Avg('rating'))
        return context


class AddressLookupView(CreateView):
    """
    View where user submits postcode. Address lookup is then completed to
    return full address.
    """

    model = AddressLookup
    template_name = "addresses/address_lookup.html"
    form_class = AddressLookupForm

    def get_context_data(self, **kwargs):
        """Include the users selected country in the views context."""
        context = {}
        context['country'] = dict(country_choices)[
            self.request.GET['country'].upper()]
        return super().get_context_data(**context)

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""

        query_dictionary = QueryDict('', mutable=True)
        query_dictionary.update(
            {
                'address_lookup': self.object.id
            }
        )
        base_url = reverse_lazy('addresses:address_create')
        querystring = query_dictionary.urlencode()
        self.success_url = f'{base_url}?{querystring}'

        return str(self.success_url)

    def form_valid(self, form, *args, **kwargs):
        """If the form is valid, save the associated model."""
        country_code = self.request.GET['country']
        postcode = form.cleaned_data['postcode']

        queryset = AddressLookup.objects.filter(
            postcode=postcode.upper(), country_code=country_code.lower())
        if queryset.count() > 0:
            self.object = queryset.first()
            return HttpResponseRedirect(self.get_success_url())
        else:
            self.object = form.save(commit=False)

            geolocator = Nominatim(user_agent="property_rental_watch")
            location = geolocator.geocode(
                {'postalcode': postcode}, addressdetails=True, country_codes=country_code)
            if location:
                self.object.place_id = location.raw['place_id']
                self.object.lat = location.raw['lat']
                self.object.lon = location.raw['lon']
                self.object.display_name = location.raw['display_name']
                self.object.address_class = location.raw['class']
                self.object.importance = location.raw['importance']
                if 'address' in location.raw:
                    if 'county' in location.raw['address']:
                        self.object.county = location.raw['address']['county']
                    if 'city' in location.raw['address']:
                        self.object.city = location.raw['address']['city']
                    if 'country' in location.raw['address']:
                        self.object.country = location.raw['address']['country']
                    if 'country_code' in location.raw['address']:
                        self.object.country_code = location.raw['address']['country_code'].lower(
                        )
                    if 'postcode' in location.raw['address']:
                        self.object.postcode = location.raw['address']['postcode'].upper(
                        )
                    if 'state_district' in location.raw['address']:
                        self.object.state_district = location.raw['address']['state_district']
                    if 'state' in location.raw['address']:
                        self.object.state = location.raw['address']['state']
                    if 'suburb' in location.raw['address']:
                        self.object.suburb = location.raw['address']['suburb']

                self.object.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                message = f'Invalid {country_code.upper()} postcode'
                if len(postcode) == 5:
                    postcode = postcode.upper()
                    postcode = f'"{postcode[0]}{postcode[1]} {postcode[2]}{postcode[3]}{postcode[4]}"'
                    message = f'{message}. Did you mean {postcode}? Please take note of any spaces between characters'

                form.add_error('postcode', _(message))
                return super(AddressLookupView, self).form_invalid(form)


class AddressCreateView(CreateView):
    """
    Generates address form with pre-populated fields. Fields pre-populated as
    user provided postcode in previous form and lookup was completed to internal
    or external database dependent on condition.
    """

    model = Address
    template_name = "addresses/address_create.html"
    form_class = AddressCreateForm

    def get_context_data(self, **kwargs):
        """
        Get data from model and update context so that form fields can be 
        pre-populated with data.
        """
        context = {}
        obj = get_object_or_404(
            AddressLookup, id=self.request.GET['address_lookup'])
        context['city'] = obj.city
        context['suburb'] = obj.suburb
        context['county'] = obj.county
        context['country'] = obj.country
        context['state_district'] = obj.state_district
        context['state'] = obj.state
        context['postcode'] = obj.postcode
        context['similar_addresses'] = Address.objects.filter(
            address_lookup=obj.id)
        return super().get_context_data(**context)

    def get_initial(self):
        """Set field to be included within form."""
        dict = {
            'address_lookup': get_object_or_404(AddressLookup, id=self.request.GET['address_lookup'])
        }
        self.initial = dict
        return self.initial.copy()

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)

        queryset = Address.objects.filter(num_or_name=self.object.num_or_name.lower(
        ), street_1=self.object.street_1.lower(), street_2=self.object.street_2.lower(), address_lookup=self.object.address_lookup)
        if queryset.count() > 0:
            self.object = queryset.first()
        else:
            self.object.save()

        self.success_url = reverse_lazy(
            'addresses:address_detail', kwargs={'pk': self.object.pk})
        return HttpResponseRedirect(self.get_success_url())
