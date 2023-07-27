from django.urls import path

from .views import (
    feeds_page_view,
    ask_review_view,
    create_review_view,
    create_review_for_ticket_view,
    list_user_view,
    posts_page_view,
)

app_name = "review"

urlpatterns = [
    path("feeds/", feeds_page_view, name="feeds_page"),
    path("posts/", posts_page_view, name="posts_page"),
    path("abo/", list_user_view, name="abo_page"),
    path("ask_review/", ask_review_view, name="ask_review"),
    path("create_review/", create_review_view, name="create_review"),
    path(
        "create_review_ticket/<int:pk>/",
        create_review_for_ticket_view,
        name="create_review_ticket",
    ),
]
