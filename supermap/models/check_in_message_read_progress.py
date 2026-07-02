import logging
from django.db import models

logger = logging.getLogger(__name__)


class CheckInMessageReadProgress(models.Model):

    user_id = models.BigIntegerField(default=0)
    last_read_id = models.BigIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)