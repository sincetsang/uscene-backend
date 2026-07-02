import logging
from django.db import models
from .check_in import *

logger = logging.getLogger(__name__)


class CheckInComment(models.Model):

    class Status(models.IntegerChoices):
        NORMAL = 0, 'normal'
        hidden = 1, 'hidden'
        deleted = 2, 'deleted'

    check_in_id = models.BigIntegerField(default=0)
    parent_id = models.IntegerField(default=0, null=True, blank=True)
    reply_to_id = models.IntegerField(default=0)
    reply_to_user_id = models.BigIntegerField(default=0)
    user_id = models.BigIntegerField(default=0)
    content = models.TextField(max_length=200, default='', null=True, blank=True)
    status = models.SmallIntegerField(default=0, choices=Status.choices)
    city = models.TextField(max_length=50, default='', blank=True, null=True)
    like_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)