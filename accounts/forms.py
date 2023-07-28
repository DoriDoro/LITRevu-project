from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper

from .models import User, UserFollows


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "password1", "password2")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)


class AboForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ("user",)
