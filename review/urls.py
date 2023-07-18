from django.urls import path

from .views import review_page_view
app_name = 'review'

urlpatterns = [
    path('review/', review_page_view, name="review_page")
]
