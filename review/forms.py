from django import forms

from .models import Ticket, Review


class AskReviewForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')


class CreateReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('headline', 'rating', 'body')

    rating = forms.ChoiceField(choices=[(i, str(i)) for i in range(6)])
