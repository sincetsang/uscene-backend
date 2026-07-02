import logging
from django.db import models
from decimal import Decimal

logger = logging.getLogger(__name__)


class UserCheckRecord(models.Model):
    user_id = models.BigIntegerField()
    point_id = models.BigIntegerField(verbose_name='打开点id')
    day = models.CharField(max_length=10, verbose_name='打卡日期 YYYYMMDD')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "user_check_record"
        indexes = [
            models.Index(fields=['user_id', 'day']),  # 复合索引
        ]