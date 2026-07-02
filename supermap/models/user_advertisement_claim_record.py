import logging
from django.db import models

logger = logging.getLogger(__name__)


class UserAdvertisementClaimRecord(models.Model):
    user_id = models.BigIntegerField(verbose_name="用户ID")
    advertisement_id = models.BigIntegerField(verbose_name="广告ID")
    reward_amount = models.DecimalField(max_digits=12, decimal_places=4, default=0, verbose_name="奖励金额")
    reward_currency = models.CharField(max_length=20, verbose_name="奖励单位", default='FEC')
    status = models.IntegerField(default=1, verbose_name="状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "user_advertisement_claim_record"
        verbose_name = "用户广告领取记录"
        indexes = [
            models.Index(fields=['user_id', 'advertisement_id'], name='idx_user_adv_id'),
        ]