import logging
from django.db import models
from .check_in import *

logger = logging.getLogger(__name__)


class CheckInCommentLike(models.Model):
    
    check_in_id = models.BigIntegerField(default=0)
    comment_id = models.BigIntegerField(default=0)
    comment_user_id = models.BigIntegerField(default=0)
    user_id = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)