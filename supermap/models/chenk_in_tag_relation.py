import logging
from django.db import models
from .check_in import CheckIn
from .check_in_tag import CheckInTag
logger = logging.getLogger(__name__)


class CheckInTagRelation(models.Model):

    check_in_id = models.BigIntegerField(default=0)
    check_in_tag_id = models.BigIntegerField(default=0, verbose_name="check_in_tag_id")
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)