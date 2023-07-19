from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import CreateTicketForm
from .models import Ticket, Review


@login_required
def review_page_view(request):
    reviews = Review.objects.all()
    tickets = Ticket.objects.all()
    stars = range(1, 6)

    context = {
        'reviews': reviews,
        'tickets': tickets,
        'stars': stars,
        'media_url': settings.MEDIA_URL
    }

    return render(request, 'review_page.html', context)


@login_required
def create_ticket_view(request):
    form = CreateTicketForm

    if request.method == 'POST':
        form = CreateTicketForm(request.POST, request.FILES)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            form.save()

            review_page_url = reverse('review:review_page')
            return redirect(review_page_url)

    return render(request, 'create_ticket_page.html', context={'form': form})
