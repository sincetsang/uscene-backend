import logging
from django.db import models
from .check_in_point import CheckInPoint

logger = logging.getLogger(__name__)


class CheckInTag(models.Model):

    sort_index = models.IntegerField(default=0)
    name = models.CharField(max_length=20, default='')
    reference_count = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)