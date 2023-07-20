from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import AskReviewForm, CreateReviewForm
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


# TODO create error messages for else
@login_required
def ask_review_view(request):
    form = AskReviewForm()

    if request.method == 'POST':
        form = AskReviewForm(request.POST, request.FILES)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            form.save()

            feeds_page_url = reverse('review:feeds_page')
            return redirect(feeds_page_url)

    return render(request, 'ask_review_page.html', context={'form': form})


# TODO create error messages for else
@login_required
def create_review_view(request):
    ask_review_form = AskReviewForm()
    create_review_form = CreateReviewForm()

    if request.method == 'POST':
        ask_review_form = AskReviewForm(request.POST, request.FILES)
        create_review_form = CreateReviewForm(request.POST)

        if ask_review_form.is_valid() and create_review_form.is_valid():
            ask_review = ask_review_form.save(commit=False)
            create_review = create_review_form.save(commit=False)

            ask_review.user = request.user

            create_review.ticket = ask_review
            create_review.user = request.user

            ask_review_form.save()
            create_review_form.save()

            feeds_page_url = reverse('review:feeds_page')
            return redirect(feeds_page_url)

    context = {'ask_review_form': ask_review_form, 'create_review_form': create_review_form}

    return render(request, 'create_review_page.html', context)


@login_required
def create_review_for_ticket_view(request, pk):
    get_ticket = Ticket.objects.get(pk=pk)

    create_review_ticket_form = CreateReviewForm()

    if request.method == 'POST':
        create_review_ticket_form = CreateReviewForm(request.POST)

        if create_review_ticket_form.is_valid():
            create_review = create_review_ticket_form.save(commit=False)

            create_review.ticket = get_ticket
            create_review.user = request.user

            create_review_ticket_form.save()

            feeds_page_url = reverse('review:feeds_page')
            return redirect(feeds_page_url)

    context = {
        'get_ticket': get_ticket,
        'create_review_ticket_form': create_review_ticket_form,
        'media_url': settings.MEDIA_URL
    }

    return render(request, 'create_review_ticket_page.html', context)
