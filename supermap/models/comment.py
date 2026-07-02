import logging
from django.db import models

logger = logging.getLogger(__name__)


class Comment(models.Model):
    spot_id = models.BigIntegerField(default=0, verbose_name="地标ID")
    order_id = models.BigIntegerField(default=0, verbose_name="order ID")
    product_id = models.BigIntegerField(default=0, verbose_name="product ID")
    user_id = models.BigIntegerField(default=0, verbose_name="用户ID")
    content = models.TextField(max_length=500, blank=True, null=True)
    star = models.IntegerField(default=5)
    timestamp = models.IntegerField(default=0)
    audit_status = models.IntegerField(default=0, verbose_name="审核状态")
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "comment"
