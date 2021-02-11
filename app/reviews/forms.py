from django import forms

from .models import Review

class ReviewForm(forms.ModelForm):
    """Form definition for Review."""

    class Meta:
        """Meta definition for Reviewform."""

        model = Review
        fields = ('title', 'desc', 'rating',)
