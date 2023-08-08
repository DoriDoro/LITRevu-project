from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import redirect, render

from .forms import SignupForm, LoginForm, AboForm
from .models import User, UserFollows


def signup_page_view(request):
    """register view"""

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = SignupForm()

    return render(request, "register/register_page.html", context={"form": form})


def login_page_view(request):
    """login to user interphase"""

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )

            if user is not None:
                login(request, user)
                return redirect("review:feeds_page")

            else:
                messages.error(request, "Invalid username or password!")

    else:
        form = LoginForm()

    return render(request, "login/login_page.html", context={"form": form})


def logout_page_view(request):
    """logout from user interphase"""

    logout(request)
    return redirect("accounts:login")


# abo page
@login_required
def abo_page_view(request):
    """abo page, with follow and unfollow logic, see which users is following request.user"""

    if request.method == "POST":
        form = AboForm(request.POST, user=request.user)

        if "follow" in request.POST:
            if form.is_valid():
                to_be_followed_user = form.cleaned_data["search"]
                try:
                    user_to_follow = User.objects.get(username=to_be_followed_user)
                    UserFollows.objects.create(
                        user=request.user, followed_user=user_to_follow
                    )
                except User.DoesNotExist:
                    messages.error(
                        request, "User does not exist. Please choose another name."
                    )
                except IntegrityError:
                    messages.error(request, "You are already following this User.")

            else:
                messages.error(request, "Please choose an other name.")

        elif "unfollow" in request.POST:
            user_id = request.POST.get("unfollow")
            user_to_unfollow = User.objects.get(id=user_id)
            UserFollows.objects.get(
                user=request.user, followed_user=user_to_unfollow
            ).delete()

        return redirect("accounts:abo_page")

    else:
        form = AboForm(user=request.user)

    # get data out of database for the context
    followed_users = request.user.following.all()
    followed_by_others = UserFollows.objects.filter(followed_user=request.user)

    users = (
        User.objects.filter(
            is_superuser=False,
        )
        .exclude(
            id__in=request.user.following.values_list("followed_user_id", flat=True)
        )
        .exclude(id=request.user.id)
    )

    context = {
        "form": form,
        "users": users,
        "followed_users": followed_users,
        "followed_by_others": followed_by_others,
    }

    return render(request, "abo/abo_page.html", context)
