import logging
from django.db import models
from decimal import Decimal


logger = logging.getLogger(__name__)


class VerificationCode(models.Model):
    buy_uid = models.BigIntegerField()
    code = models.CharField(max_length=50, default='')
    status = models.CharField(max_length=20, verbose_name='状态(UNUSE:未使用,USED:已使用)')
    order_id = models.BigIntegerField(verbose_name='订单id')
    use_uid = models.BigIntegerField(verbose_name='使用人id')
    use_time = models.DateTimeField(verbose_name='使用时间', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "verification_code"
        constraints = [
            models.UniqueConstraint(fields=['code'], name='unique_code'),  # 唯一索引
        ]   