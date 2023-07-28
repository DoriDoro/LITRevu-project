from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import SignupForm, LoginForm, AboForm
from .models import User, UserFollows


def signup_page_view(request):
    form = SignupForm()

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, "register/register_page.html", context={"form": form})


def login_page_view(request):
    form = LoginForm()

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

    return render(request, "login/login_page.html", context={"form": form})


def logout_page_view(request):
    logout(request)
    return redirect("accounts:login")


# abo page
@login_required
def abo_page_view(request):
    """abo page"""

    form = AboForm()
    # TODO: if request.user is trying to add an already followed user, error message
    # TODO: not possible ti follow user itself
    if request.method == "POST":
        form = AboForm(request.POST)
        current_user = User.objects.get(id=request.user.id)

        if "follow" in request.POST:
            if form.is_valid():
                form.save(commit=False)
                to_be_followed_user = form.cleaned_data["user"]
                user_to_follow = User.objects.get(username=to_be_followed_user)
                UserFollows.objects.create(
                    user=current_user, followed_user=user_to_follow
                )

        elif "unfollow" in request.POST:
            user_id = request.POST.get("unfollow")
            user_to_unfollow = User.objects.get(id=user_id)
            UserFollows.objects.get(
                user=current_user, followed_user=user_to_unfollow
            ).delete()

        return redirect("accounts:abo_page")

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
