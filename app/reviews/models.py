from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import reverse
from django.utils.translation import gettext as _


class Review(models.Model):
    """Model definition for Review."""

    title = models.CharField(max_length=100)
    desc = models.TextField(max_length=5000)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    address = models.ForeignKey("addresses.Address", verbose_name=_("Address"), on_delete=models.CASCADE)

    class Meta:
        """Meta definition for Review."""

        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        """Unicode representation of Review."""
        return "title: {}, rating: {}".format(self.title, self.rating)

    def get_absolute_url(self):
        return reverse('reviews:review_detail', kwargs={'pk': self.pk})
