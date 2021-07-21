from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, CreateView
from django.db.models import Avg
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, QueryDict
from django.utils.translation import gettext_lazy as _

from .models import Address, AddressLookup
from reviews.models import Review
from .constants import country_choices

from geopy.geocoders import Nominatim


class AddressDetailView(DetailView):
    """
    Provides more detailed information related to the address. This includes
    related reviews etc.
    """

    model = Address
    template_name = "addresses/address_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.filter(
            address=self.object, user__isnull=False)
        context["reviews"] = reviews
        context["average_rating"] = reviews.aggregate(Avg('rating'))
        context['address_lookup'] = AddressLookup.objects.filter(
            pk=self.object.address_lookup.pk).values()[0]
        return context


class AddressLookupView(CreateView):
    """
    View where user submits postcode. Address lookup is then completed to
    return related address.
    """

    model = AddressLookup
    template_name = "addresses/address_lookup.html"
    form_class = AddressPostcodeLookupForm

    def get_context_data(self, **kwargs):
        """Include the users selected country in the views context."""
        context = kwargs
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
                location_raw = location.raw
                self.object.place_id = location_raw['place_id']
                self.object.lat = location_raw['lat']
                self.object.lon = location_raw['lon']
                self.object.display_name = location_raw['display_name']
                self.object.address_class = location_raw['class']
                self.object.importance = location_raw['importance']
                if 'address' in location_raw:
                    address = location_raw['address']
                    self.object.county = address.get('county', '')
                    self.object.city = address.get('city', '')
                    self.object.country = address.get('country', '')
                    country_code = address.get('country_code', '')
                    if country_code:
                        self.object.country_code = country_code.lower()
                    postcode = address.get('postcode', '')
                    if postcode:
                        self.object.postcode = postcode.upper()
                    self.object.state_district = address.get(
                        'state_district', '')
                    self.object.state = address.get('state', '')
                    self.object.suburb = address.get('suburb', '')
                self.object.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                message = f'Invalid {country_code.upper()} postcode'
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
