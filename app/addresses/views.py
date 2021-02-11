from django.shortcuts import render
from django.views.generic import DetailView

from .models import Address
from reviews.models import Review


class AddressDetailView(DetailView):
    model = Address
    template_name = "addresses/address_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = Review.objects.filter(address=self.object)
        return context
