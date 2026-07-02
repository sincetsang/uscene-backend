import logging
from django.db import models
from decimal import Decimal

logger = logging.getLogger(__name__)


class ProductFavorite(models.Model):
    user_id = models.BigIntegerField(default=True)
    product_id = models.BigIntegerField(default=True)
    mark = models.CharField(max_length=20, default='')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "product_favorite"
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['product_id'])
        ]
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'product_id'], name='unique_constraint_user_product'),  # 唯一索引
        ]
