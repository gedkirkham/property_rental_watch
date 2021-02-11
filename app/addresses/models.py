from django.db import models

from address.models import AddressField


class Address(models.Model):
    """Model definition for Address."""

    address = AddressField()

    class Meta:
        """Meta definition for Address."""

        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        """Unicode representation of Address."""
        return self.address.raw