from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """create User instance"""

    pass


class UserFollows(models.Model):
    """follow and followed by model"""

    class Meta:
        verbose_name = "UserFollow"
        verbose_name_plural = "UserFollows"

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name=_("user"),
    )
    followed_user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="followed_by",
        verbose_name=_("follower"),
    )

    class Meta:
        unique_together = ["user", "followed_user"]

    def __str__(self):
        return f"{self.user} - is following: {self.followed_user}"
