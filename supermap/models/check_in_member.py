import logging
from django.db import models
from .check_in_point import CheckInPoint

logger = logging.getLogger(__name__)


class CheckInMember(models.Model):

    user_id = models.BigIntegerField(default=0)
    expired_timestamp = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)