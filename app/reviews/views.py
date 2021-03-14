from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, TemplateView
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from .models import Review
from .forms import EmailForm, ReviewForm
from addresses.models import Address
from accounts.models import Profile
from app.tokens import review_activation_token


class ActivateReview(View):
    def get(self, request, uidb64, reviewb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            user = None

        try:
            rid = force_text(urlsafe_base64_decode(reviewb64))
            review = Review.objects.get(pk=rid)
        except ObjectDoesNotExist:
            review = None

        if user is not None and review is not None and review_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            profile = Profile.objects.get(user=user)
            profile.email_confirmed = True
            profile.save()

            review.user = user
            review.save()

            login(request, user)
            messages.success(request, _('Your review have been activated.'))
            return redirect('home')
        else:
            messages.warning(
                request, _('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('home')

    def get(self, request, uidb64, reviewb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            user = None

        try:
            rid = force_text(urlsafe_base64_decode(reviewb64))
            review = Review.objects.get(pk=rid)
        except ObjectDoesNotExist:
            review = None

        if user is not None and review is not None and review_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            profile = Profile.objects.get(user=user)
            profile.email_confirmed = True
            profile.save()

            review.user = user
            review.save()

            login(request, user)
            messages.success(request, _('Your review have been activated.'))
            return redirect('home')
        else:
            messages.warning(
                request, _('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('home')


class ReviewCreateView(TemplateView):
    template_name = "reviews/review_create.html"
    review_form_class = ReviewForm
    email_form_class = EmailForm

    def post(self, request):
        post_data = request.POST or None

        review_form = self.review_form_class(post_data, prefix="review")
        email_form = self.email_form_class(post_data, prefix="email")

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.address = get_object_or_404(
                Address, pk=self.request.GET.get('addr'))
            review.save()

        if email_form.is_valid():
            email = email_form.cleaned_data['email']

            user, created = User.objects.get_or_create(
                username=email, email=email)
            if not created:
                password = User.objects.make_random_password()
                user.set_password(password)
                user.is_active = False
                user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Review'
            message = render_to_string('emails/review_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'review': urlsafe_base64_encode(force_bytes(review.pk)),
                'token': review_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(
                self.request, ('Please follow the link in your email to activate your review.'))

        context = self.get_context_data(
            review_form=review_form,
            email_form=email_form,
        )

        if review_form.is_valid() and email_form.is_valid():
            return redirect(reverse_lazy('reviews:review_detail', kwargs={'pk': review.pk}))

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form
        """
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


class ReviewDetailView(DetailView):
    model = Review
    template_name = 'reviews/review_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["address"] = Address.objects.get(pk=self.object.address.pk)
        return context
