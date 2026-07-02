import logging
from django.db import models

logger = logging.getLogger(__name__)


class UserAssetDetail(models.Model):
    CATEGORY_CHOICES = [
        ('move', '移动'),
        ('check_in', '签到'),
        ('event', '活动'),
        ('refund', '签到')
    ]

    user_id = models.BigIntegerField(verbose_name="用户ID")
    invitee_id = models.BigIntegerField(null=True, blank=True, verbose_name="被邀请人ID")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="奖励类别")
    related_id = models.BigIntegerField(verbose_name="相关ID（spot_id）")
    currency = models.CharField(max_length=20, verbose_name="币种")
    rewards = models.FloatField(default=0, verbose_name='奖励数值')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "user_asset_detail"
        verbose_name = "用户资产明细"
        verbose_name_plural = "用户资产明细"

