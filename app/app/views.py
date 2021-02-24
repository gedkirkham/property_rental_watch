from django.views.generic import FormView, CreateView
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, QueryDict

from addresses.models import Address
from addresses.forms import CountryForm


class HomeView(FormView):
    form_class = CountryForm
    template_name = 'index.html'

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        self.country = form.cleaned_data['country']
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""

        query_dictionary = QueryDict('', mutable=True)
        query_dictionary.update(
            {
                'country': self.country.lower()
            }
        )
        url = '{base_url}?{querystring}'.format(
            base_url=reverse_lazy('addresses:address_lookup'),
            querystring=query_dictionary.urlencode()
        )

        self.success_url = url
        return str(self.success_url)
