import logging
from django.db import models

logger = logging.getLogger(__name__)


class UserLevelConfig(models.Model):
    level_id = models.IntegerField(unique=True, verbose_name="等级ID")
    hash_rate = models.FloatField(default=0, verbose_name='算力')
    stamina = models.IntegerField(default=0, verbose_name='体力')
    stamina_reward = models.BigIntegerField(default=0, verbose_name='每秒运动的奖励')
    checkin_limit = models.IntegerField(default=1, verbose_name="可打卡次数")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "user_level_config"
        verbose_name = "用户等级配置"
        verbose_name_plural = "用户等级配置"

