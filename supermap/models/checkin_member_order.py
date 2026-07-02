import logging
from django.db import models

logger = logging.getLogger(__name__)


class CheckInMemberOrder(models.Model):
    class Status(models.TextChoices):
        UNPAID = 'unpaid', '待支付'
        PAYMENT_PROCESSING = 'payment_processing', '支付处理中'
        PAID = 'paid', '已经支付'
        CANCEL = 'cancel', '已取消'

    order_id = models.BigIntegerField(default=0)
    user_id = models.BigIntegerField(default=0)
    ue_order_id = models.CharField(max_length=100, default='')
    period = models.CharField(max_length=20, default='')
    amount = models.FloatField(default=0, verbose_name='总金额')
    product_price = models.FloatField(default=0, verbose_name='商品单价')
    pay_type = models.CharField(max_length=20, default='FEC', verbose_name='支付方式(FEC:FEC)')
    unit = models.CharField(max_length=20, default='USD', verbose_name='单位(USD:USD)')
    status = models.CharField(max_length=20, default='unpaid', verbose_name='支付状态(unpaid:未支付,paid:已支付,cancel:已取消)', choices=Status.choices)
    member_config_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "member_order"
        indexes = [
            models.Index(fields=['user_id']),
        ]