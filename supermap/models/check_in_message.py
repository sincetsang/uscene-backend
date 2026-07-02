import logging
from django.db import models

logger = logging.getLogger(__name__)


class CheckInMessage(models.Model):
    class MessageType(models.IntegerChoices):
        CHECKINLIKE = 0, 'check_in_like'
        CHECKINCOMMENT = 1, 'check_in_comment'
        CHECKINCOMMENTLIKE = 2, 'check_in_comment_like'

    user_id = models.BigIntegerField(default=0)
    other_user_id = models.BigIntegerField(default=0)
    message_type = models.SmallIntegerField(default=0, choices=MessageType.choices)
    check_in_id = models.BigIntegerField(default=0, null=True, blank=True)
    content = models.CharField(max_length=200, default='', null=True, blank=True)
    comment_id = models.BigIntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)