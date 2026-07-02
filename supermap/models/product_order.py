import logging
from django.db import models
from decimal import Decimal


logger = logging.getLogger(__name__)


class ProductOrder(models.Model):

    class Status(models.TextChoices):
        PENDING_PAYMENT = 'pending_payment', '待支付'
        PAYMENT_PROCESSING = 'payment_processing', '支付处理中'
        PENDING_SHIPMENT = 'pending_shipment', '已支付'
        PENDING_RECEIPT = 'pending_receipt', '待收货'
        COMPLETED = 'completed', '交易完成'
        CANCELLED = 'cancelled', '已取消'
        CLOSED = 'closed', '已关闭'

    class RefundStatus(models.TextChoices):
        # PENDING_APPROVE = 'pending_approve', '待审核'
        NO_REFUND = 'no_refund', '无退款'
        REFUNDING = 'refunding', '退款中'
        REFUNDED = 'refunded', '已退款'
        REFUND_FAILED = 'refund_rejected', '已拒绝'

    order_id = models.BigIntegerField(default=0)
    spot_id = models.BigIntegerField(default=0)
    ue_order_id = models.CharField(max_length=100, default='')
    user_id = models.BigIntegerField(verbose_name='买家')
    seller_id = models.BigIntegerField(default=0, verbose_name='卖家')
    product_id = models.BigIntegerField()
    product_name = models.CharField(max_length=100, default='')
    product_num = models.IntegerField(default=1, verbose_name='商品数量')
    amount = models.FloatField(default=0, verbose_name='总金额')
    product_price = models.FloatField(default=0, verbose_name='商品单价')
    pay_type = models.CharField(max_length=20, default='FEC', verbose_name='支付方式(FEC:FEC)')
    unit = models.CharField(max_length=20, default='USD', verbose_name='单位(USD:USD)')
    status = models.CharField(max_length=20, default='unpaid', verbose_name='支付状态(unpaid:未支付,paid:已支付,cancel:已取消)', choices=Status.choices)
    is_commented = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.BigIntegerField(default=0)
    refund_status = models.CharField(max_length=20,choices=RefundStatus.choices, default=RefundStatus.NO_REFUND)
    cancel_reason = models.CharField(max_length=50, default='', null=True, blank=True)
    cancel_by_buyer = models.BooleanField(default=False)
    cancel_at = models.BigIntegerField(default=0)
    contact_name = models.CharField(max_length=20, default='', null=True, blank=True)
    contact_phone = models.CharField(max_length=20, default='', null=True, blank=True)
    contact_address = models.CharField(max_length=100, default='', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "product_order"
        indexes = [
            models.Index(fields=['user_id', 'product_id']),  # 普通复合索引
        ]