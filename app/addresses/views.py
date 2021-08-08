from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, CreateView, TemplateView
from django.db.models import Avg, Q
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, QueryDict
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from .models import Address, AddressLookup
from reviews.models import Review
from .forms import AddressPostcodeLookupForm, AddressCreateForm, \
    AddressLookupForm
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
                'address_lookup': self.object.id,
                'postcode': self.object.postcode,
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
                # TODO: add to translation
                message = f'Invalid {country_code.upper()} postcode'
                form.add_error('postcode', _(message))
                return super(AddressLookupView, self).form_invalid(form)


class AddressCreateView(TemplateView):
    """
    Generates address form with pre-populated or empty fields. Fields are
    pre-populated as user provided postcode in previous form and lookup was
    completed to internal or external database dependent on condition.
    """

    template_name = "addresses/address_create.html"
    address_form_class = AddressCreateForm
    address_lookup_form_class = AddressLookupForm

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def post(self, request):
        address_form, address_lookup_form = self._init_forms()

        if address_form.is_valid() and address_lookup_form.is_valid():
            address = self._get_or_create_address(
                address_form=address_form)
            address_lookup = self._get_or_create_address_lookup(
                address_lookup_form=address_lookup_form)
            address.address_lookup = address_lookup
            address.save()
            return redirect(reverse_lazy('addresses:address_detail', kwargs={'pk': address.pk}))

        similar_addresses = self._get_similar_addresses()
        context = self.get_context_data(
            address_form=address_form, address_lookup_form=address_lookup_form, similar_addresses=similar_addresses)

        return self.render_to_response(context)

    def _init_forms(self):
        """
        Initialise data in forms. If address_lookup query param is passed,
        add address data to form.
        """

        post_data = self.request.POST or None
        address_form = self.address_form_class(post_data, prefix='address')

        address_lookup_kwarg = self.request.GET.get('address_lookup', None)
        initial = None
        if address_lookup_kwarg:
            address_lookup = get_object_or_404(
                AddressLookup, pk=address_lookup_kwarg)
            initial = {'suburb': address_lookup.suburb, 'city': address_lookup.city, 'county': address_lookup.county, 'country': address_lookup.country,
                       'state_district': address_lookup.state_district, 'state': address_lookup.state, 'postcode': address_lookup.postcode}
        address_lookup_form = self.address_lookup_form_class(
            post_data, prefix="address_lookup", initial=initial)

        return address_form, address_lookup_form

    def _get_or_create_address(self, address_form):
        """
        Get data from form and determine if address is already in database. If
        true, return address, otherwise create a new address object.
        """

        num_or_name = address_form.cleaned_data['num_or_name']
        street_1 = address_form.cleaned_data['street_1']
        street_2 = address_form.cleaned_data['street_2']

        try:
            address = Address.objects.get(
                num_or_name__iexact=num_or_name, street_1__iexact=street_1, street_2__iexact=street_2)
        except ObjectDoesNotExist:
            address = Address(num_or_name=num_or_name,
                              street_1=street_1, street_2=street_2)
        except MultipleObjectsReturned:
            address = Address.objects.filter(
                num_or_name__iexact=num_or_name, street_1__iexact=street_1, street_2__iexact=street_2).first()
        finally:
            return address

    def _get_or_create_address_lookup(self, address_lookup_form):
        """
        Get data from form and determine if address_lookup is already in database. If
        true, return address, otherwise create a new address_lookup object.
        """

        suburb = address_lookup_form.cleaned_data['suburb']
        city = address_lookup_form.cleaned_data['city']
        county = address_lookup_form.cleaned_data['county']
        country = address_lookup_form.cleaned_data['country']
        state_district = address_lookup_form.cleaned_data['state_district']
        state = address_lookup_form.cleaned_data['state']
        postcode = address_lookup_form.cleaned_data['postcode']

        try:
            address_lookup = AddressLookup.objects.get(
                suburb__iexact=suburb, city__iexact=city, county__iexact=county, country__iexact=country, state_district__iexact=state_district, state__iexact=state, postcode__iexact=postcode)
        except ObjectDoesNotExist:
            address_lookup = AddressLookup(suburb=suburb, city=city, county=county, country=country,
                                           state_district=state_district, state=state, postcode=postcode)
            address_lookup.save()
        except MultipleObjectsReturned:
            address_lookup = AddressLookup.objects.filter(
                suburb__iexact=suburb, city__iexact=city, county__iexact=county, country__iexact=country, state_district__iexact=state_district, state__iexact=state, postcode__iexact=postcode).first()
        finally:
            return address_lookup

    def _get_similar_addresses(self):
        """
        Locate similar addresses by postcode and return queryset.
        """

        postcode = self.request.GET.get('postcode', None)
        similar_addresses = None
        if postcode:
            similar_addresses = Address.objects.filter(Q(address_lookup__postcode__iexact=postcode) | Q(
                address_lookup__postcode__iexact=postcode.replace(" ", "")))
        return similar_addresses
