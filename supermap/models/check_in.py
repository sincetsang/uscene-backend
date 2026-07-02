import logging
from django.db import models
from .check_in_point import CheckInPoint

logger = logging.getLogger(__name__)


class CheckIn(models.Model):

    class Status(models.IntegerChoices):
        Pending = 0, 'pending'
        Approved = 1, 'approved'
        Rejected = 2, 'rejected'
        Hidden = 3, 'hidden'

    check_in_point = models.ForeignKey(CheckInPoint, on_delete=models.CASCADE, verbose_name="关联地标")
    user_id = models.BigIntegerField(default=0, verbose_name="user_id")
    content = models.TextField(max_length=500, default='')
    status = models.SmallIntegerField(default=0, choices=Status.choices)
    private = models.BooleanField(default=False)
    comment_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    visit_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
