import logging
from django.db import models
from .check_in_point import CheckInPoint

logger = logging.getLogger(__name__)


class UserFollow(models.Model):

    user_id = models.BigIntegerField(default=0)
    followed_user_id = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)