import logging
from django.db import models
from decimal import Decimal


logger = logging.getLogger(__name__)


class UserLike(models.Model):
    user_id = models.BigIntegerField()
    spot_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "user_like"
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'spot_id'], name='idx_user_id_spot_id'),
        ]