import logging
from django.db import models

logger = logging.getLogger(__name__)


class SpotLevelConfig(models.Model):
    level = models.IntegerField(verbose_name="等级")
    experience = models.FloatField(default=0, verbose_name='经验值')
    hash_rate = models.FloatField(default=0, verbose_name='算力')
    checkin_radius = models.IntegerField(default=0, verbose_name="签到半径")

    class Meta:
        db_table = "spot_level_config"
        verbose_name = "地点等级配置"
        verbose_name_plural = "地点等级配置"
