import logging
from django.db import models
from .check_in import CheckIn
logger = logging.getLogger(__name__)


class CheckInLike(models.Model):

    check_in_id = models.BigIntegerField(default=0)
    user_id = models.BigIntegerField(default=0, verbose_name="user_id")
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)