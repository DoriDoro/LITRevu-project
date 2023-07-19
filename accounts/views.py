from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render

from .forms import SignupForm, LoginForm


def signup_page_view(request):
    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'register_page.html', context={'form': form})


def login_page_view(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )

            if user is not None:
                login(request, user)
                return redirect('review:review_page')

    return render(request, 'login_page.html', context={'form': form})


def logout_page_view(request):
    logout(request)
    return redirect('accounts:login')
