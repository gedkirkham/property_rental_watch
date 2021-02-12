from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, DetailView
from django.core.exceptions import ImproperlyConfigured

from .models import Review
from .forms import ReviewForm
from addresses.models import Address


class ReviewCreateView(CreateView):
    model = Review
    template_name = "reviews/review_create.html"
    form_class = ReviewForm

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if self.success_url:
            url = self.success_url.format(**self.object.__dict__)
        else:
            try:
                url = self.object.get_absolute_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model.")
        return url

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.address = get_object_or_404(Address, pk=self.request.GET.get('addr'))
        self.object.save()
        return super().form_valid(form)


class ReviewDetailView(DetailView):
    model = Review
    template_name = 'reviews/review_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["address"] = Address.objects.get(pk=self.object.address.pk)
        return context