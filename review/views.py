from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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
