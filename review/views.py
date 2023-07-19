from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import AskReviewForm
from .models import Ticket, Review


@login_required
def feeds_page_view(request):
    reviews = Review.objects.all()
    tickets = Ticket.objects.all()
    stars = range(1, 6)

    context = {
        'reviews': reviews,
        'tickets': tickets,
        'stars': stars,
        'media_url': settings.MEDIA_URL
    }

    return render(request, 'feeds_page.html', context)


@login_required
def ask_review_view(request):
    form = AskReviewForm

    if request.method == 'POST':
        form = AskReviewForm(request.POST, request.FILES)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            form.save()

            feeds_page_url = reverse('review:feeds_page')
            return redirect(feeds_page_url)

    return render(request, 'ask_review_page.html', context={'form': form})
