import logging
from django.db import models
from decimal import Decimal

logger = logging.getLogger(__name__)


class ProductVisitHistory(models.Model):
    user_id = models.BigIntegerField(default=0)
    product_id = models.BigIntegerField(default=0)
    timestamp = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "product_visit_history"
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['product_id'])
        ]
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'product_id'], name='unique_constraint_user_product_history'),  # 唯一索引
        ]
