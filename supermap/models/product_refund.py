import logging
from django.db import models
from decimal import Decimal

logger = logging.getLogger(__name__)


class ProductRefund(models.Model):
    class Status(models.TextChoices):
        # PENDING_APPROVE = 'pending_approve', '待审核'
        REFUNDING = 'refunding', '退款中'
        REFUNDED = 'refunded', '已退款'
        REFUND_FAILED = 'refund_rejected', '已拒绝'

    order_id = models.BigIntegerField(default=0)
    user_id = models.BigIntegerField()
    amount = models.FloatField(default=0, verbose_name='总金额')
    unit = models.CharField(max_length=20, default='USD', verbose_name='单位(USD:USD)')
    status = models.CharField(choices=Status.choices, default=Status.REFUNDING, max_length=20)
    remark = models.CharField(max_length=50, default='', null=True, blank=True)
    timestamp = models.BigIntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "product_refund"
