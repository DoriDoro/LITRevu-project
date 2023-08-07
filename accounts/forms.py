from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, UserFollows


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "password1", "password2")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)


class AboForm(forms.Form):
    search = forms.CharField(max_length=50, label=False)

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_search(self):
        search = self.cleaned_data["search"]

        if self.user and self.user.username == search:
            raise forms.ValidationError("You can not follow yourself!")

        if User.objects.filter(username=search, is_superuser=True).exists():
            raise forms.ValidationError("Please choose an other name to follow!")

        return search
