import logging
from django.db import models

logger = logging.getLogger(__name__)

class PaymentOrder(models.Model):
        
    class Status(models.TextChoices):
        PENDING = 'pending', '待支付'
        PAID = 'paid', '已支付'
        FAILED = 'failed', '支付失败'
        EXPIRED = 'expired', '已过期'
        REFUNDED = 'refunded', '已退款'

    class BizType(models.TextChoices):
        CODE = 'code', '核销码'
        PRODUCT = 'product', '产品'
        MEMBER = 'member', '会员'

    order_id = models.CharField(max_length=32, unique=True)
    chain = models.CharField(max_length=20)
    currency = models.CharField(max_length=10)
    amount = models.FloatField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    tx_hash = models.CharField(max_length=66, null=True, blank=True)
    from_address = models.CharField(max_length=42, null=True, blank=True)
    to_address = models.CharField(max_length=42)
    block_number = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField()
    paid_at = models.DateTimeField(null=True, blank=True)
    expired_at = models.DateTimeField(null=True, blank=True)
    description = models.CharField(max_length=200)
    metadata = models.JSONField()
    biz_type = models.CharField(max_length=20, default=BizType.CODE, choices=BizType.choices)
    tx_data = models.CharField(max_length=100, null=True, blank=True)
    pay_order_id = models.CharField(max_length=32, unique=True, null=True, blank=True)
    is_callback = models.BooleanField()

    class Meta:
        db_table = "payment_orders"
        verbose_name = "支付订单列表"
        verbose_name_plural = "支付订单列表" 