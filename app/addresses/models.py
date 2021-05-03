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
        return f"{self.num_or_name}, {self.street_1}, {self.address_lookup}"

    def get_absolute_url(self):
        return reverse_lazy('addresses:address_detail', kwargs={'pk': self.pk})


class AddressLookup(models.Model):
    """Model definition for AddressLookup."""

    address_class = models.CharField(_('Class'), max_length=50)
    city = models.CharField(_('City'), max_length=50)
    county = models.CharField(_('County'), max_length=50)
    country = models.CharField(_('Country'), max_length=50)
    country_code = models.CharField(_('Country code'), max_length=50)
    display_name = models.CharField(_('Display name'), max_length=100)
    importance = models.FloatField()
    lat = models.FloatField()
    lon = models.FloatField()
    place_id = models.IntegerField()
    postcode = models.CharField(_('Postcode'), max_length=50)
    state_district = models.CharField(_('State district'), max_length=50)
    state = models.CharField(_('State'), max_length=50)
    suburb = models.CharField(_('Suburb'), max_length=50)

    class Meta:
        """Meta definition for AddressLookup."""

        verbose_name = 'AddressLookup'
        verbose_name_plural = 'AddressLookups'

    def __str__(self):
        """Unicode representation of AddressLookup."""
        return self.display_name
