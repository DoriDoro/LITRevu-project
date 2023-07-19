from django import forms

from .models import Ticket, Review


class AskReviewForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')
