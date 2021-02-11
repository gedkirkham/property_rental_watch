from django.views.generic import FormView, CreateView
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from addresses.models import Address
from addresses.forms import AddressLookupForm

class HomeView(CreateView):
    model = Address
    template_name = "index.html"
    form_class = AddressLookupForm

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        self.success_url = reverse_lazy('addresses:address_detail', kwargs= { 'pk': self.object.pk})
        return str(self.success_url)  # success_url may be lazy

    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        try:
            self.object = Address.objects.filter(address__raw=self.object).first()
        except:
            self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())
