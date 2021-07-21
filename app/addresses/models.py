from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


class Address(models.Model):
    """Model definition for Address."""

    address_lookup = models.ForeignKey(
        "AddressLookup", on_delete=models.CASCADE)
    num_or_name = models.CharField(_('House number or name'), max_length=50)
    street_1 = models.CharField(max_length=50)
    street_2 = models.CharField(max_length=50, blank=True)

    class Meta:
        """Meta definition for Address."""

        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        """Unicode representation of Address."""
        text = f"{self.num_or_name}, {self.street_1}"
        if self.street_2:
            text += f", {self.street_2}"
        return text

    def get_absolute_url(self):
        return reverse_lazy('addresses:address_detail', kwargs={'pk': self.pk})


class AddressLookup(models.Model):
    """Model definition for AddressLookup."""

    address_class = models.CharField(_('Class'), max_length=50)
    city = models.CharField(_('City'), max_length=50)
    county = models.CharField(_('County'), max_length=50, blank=True)
    country = models.CharField(_('Country'), max_length=50, blank=True)
    country_code = models.CharField(
        _('Country code'), max_length=50, blank=True)
    display_name = models.CharField(
        _('Display name'), max_length=100, blank=True)
    importance = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    place_id = models.IntegerField(blank=True, null=True)
    postcode = models.CharField(_('Postcode'), max_length=50)
    state_district = models.CharField(
        _('State district'), max_length=50, blank=True)
    state = models.CharField(_('State'), max_length=50, blank=True)
    suburb = models.CharField(_('Suburb'), max_length=50, blank=True)

    class Meta:
        """Meta definition for AddressLookup."""

        verbose_name = 'AddressLookup'
        verbose_name_plural = 'AddressLookups'

    def __str__(self):
        """Unicode representation of AddressLookup."""
        return self.display_name
