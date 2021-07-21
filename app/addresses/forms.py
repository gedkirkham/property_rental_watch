from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Address, AddressLookup
from .constants import country_choices


class AddressCreateForm(forms.ModelForm):
    """Form definition for AddressCreate."""

    class Meta:
        """Meta definition for AddressCreateform."""

        model = Address
        fields = ('num_or_name', 'street_1', 'street_2')


class AddressLookupForm(forms.ModelForm):
    """Form definition for AddressLookup."""

    class Meta:
        """Meta definition for AddressLookupForm."""

        model = AddressLookup
        fields = ['suburb', 'city', 'county', 'country',
                  'state_district', 'state', 'postcode']


class AddressPostcodeLookupForm(forms.ModelForm):
    """Form definition for PostCodeLookup."""

    class Meta:
        """Meta definition for AddressPostcodeLookupForm."""

        model = AddressLookup
        fields = ('postcode',)


class CountryForm(forms.Form):
    """CountryForm definition."""

    country = forms.ChoiceField(choices=country_choices)
