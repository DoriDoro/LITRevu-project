from django import forms

from .models import Ticket, Review


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("title", "description", "image")


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("headline", "rating", "body")

    # rating = forms.ChoiceField(choices=[(i, str(i)) for i in range(6)])
    rating = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=[
            (1, "1 star"),
            (2, "2 stars"),
            (3, "3 stars"),
            (4, "4 stars"),
            (5, "5 stars"),
        ],
    )
