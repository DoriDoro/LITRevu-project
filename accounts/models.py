from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """ Create User instance """
    pass


class UserFollows(models.Model):
    """  """
    class Meta:
        verbose_name = "UserFollow"
        verbose_name_plural = "UserFollows"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name=_("user")
    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_by',
        verbose_name=_("follower")
    )

    class Meta:
        unique_together = ['user', 'followed_user']
