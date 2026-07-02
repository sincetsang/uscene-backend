import logging
from django.db import models

logger = logging.getLogger(__name__)


class UserPayRecord(models.Model):
    user_id = models.BigIntegerField()
    wallet_address = models.CharField(max_length=50, verbose_name='用户钱包地址')
    transaction_status = models.IntegerField(default=0, verbose_name='0-未完成 1-已完成')
    transaction_amount = models.FloatField()
    lt = models.BigIntegerField()
    transaction_hash = models.CharField(max_length=64)
    timestamp = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "user_pay_record"
        indexes = [models.Index(fields=['user_id'])]