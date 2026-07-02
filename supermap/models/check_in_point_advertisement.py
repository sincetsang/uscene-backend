import logging
from django.db import models
from .check_in_point import CheckInPoint

logger = logging.getLogger(__name__)


class CheckInPointAdvertisement(models.Model):
    check_in_point = models.ForeignKey(CheckInPoint, on_delete=models.CASCADE, verbose_name="关联地标", related_name="advertisements")
    title = models.CharField(max_length=255, verbose_name="广告标题")
    description = models.TextField(verbose_name="广告描述")
    reward_amount = models.DecimalField(max_digits=12, decimal_places=4, default=0, verbose_name="奖励金额")
    reward_currency = models.CharField(max_length=20, verbose_name="奖励单位", default='USDT')
    image_url = models.CharField(max_length=255, verbose_name="广告图片", default='')
    status = models.IntegerField(default=1, verbose_name="状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    start_time = models.DateTimeField(verbose_name="广告开始时间")
    end_time = models.DateTimeField(verbose_name="广告结束时间")

    class Meta:
        db_table = "check_in_point_advertisement"
        verbose_name = "地标广告"
        indexes = [
            models.Index(fields=['check_in_point_id'], name='idx_adv_check_point_id'),
        ]