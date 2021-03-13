from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Review

class ReviewForm(forms.ModelForm):
    """Form definition for Review."""

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['desc'].label = _('Description')

    class Meta:
        """Meta definition for Reviewform."""

        model = Review
        fields = ('title', 'desc', 'rating', 'email')
        help_texts = {
            'rating': _('Give a rating out of 5'),
            'email': _('Your email address'),
        }
