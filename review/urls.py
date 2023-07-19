from django.urls import path

from .views import feeds_page_view, ask_review_view
app_name = 'review'

urlpatterns = [
    path('feeds/', feeds_page_view, name="feeds_page"),
    path('ask_review/', ask_review_view, name="ask_review"),
]
