import logging
from django.db import models

logger = logging.getLogger(__name__)


class UserAsset(models.Model):
    user_id = models.BigIntegerField(verbose_name="用户ID")
    currency = models.CharField(max_length=20, verbose_name="币种")
    balance = models.FloatField(default=0, verbose_name='余额')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "user_asset"
        verbose_name = "用户资产"
        verbose_name_plural = "用户资产"

