import logging
from django.db import models
from decimal import Decimal


logger = logging.getLogger(__name__)


class VerificationCodeOrder(models.Model):
    class Status(models.TextChoices):
        Unpaid = 'unpaid', '未支付'
        Paid = 'paid', '已支付'
        Cancel = 'cancel', '已取消'
    order_id = models.BigIntegerField(default=0)
    ue_order_id = models.CharField(max_length=100, default='')
    user_id = models.BigIntegerField()
    product_id = models.BigIntegerField()
    product_name = models.CharField(max_length=100, default='')
    code_num = models.IntegerField(default=0, verbose_name='验证码数量')
    product_num = models.IntegerField(default=1, verbose_name='商品数量')
    amount = models.FloatField(default=0, verbose_name='总金额')
    product_price = models.FloatField(default=0, verbose_name='商品单价')
    pay_type = models.CharField(max_length=20, default='FEC', verbose_name='支付方式(FEC:FEC)')
    unit = models.CharField(max_length=20, default='USD', verbose_name='单位(USD:USD)')
    status = models.CharField(max_length=20, default='unpaid', verbose_name='支付状态(unpaid:未支付,paid:已支付,cancel:已取消)', choices=Status.choices)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "verification_code_order"
        # constraints = [
        #     models.Index(fields=['user_id', 'product_id'], name='idx_user_product'),  # 普通复合索引
        # ]