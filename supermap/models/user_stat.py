import logging
from django.db import models
from decimal import Decimal


logger = logging.getLogger(__name__)


class UserStat(models.Model):
    user_id = models.BigIntegerField(default=0)
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    checkin_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
