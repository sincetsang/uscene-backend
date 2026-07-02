import logging
from django.db import models
from supermap.models.spot_boost_config import SpotBoostConfig
from supermap.models.check_in_point import CheckInPoint

logger = logging.getLogger(__name__)


class SpotBoost(models.Model):

    boost = models.ForeignKey(SpotBoostConfig, on_delete=models.CASCADE)
    ratio = models.FloatField(default=0)
    spot_id = models.ForeignKey(CheckInPoint, on_delete=models.CASCADE, db_column='spot_id', null=True)
    start_time = models.DateTimeField(verbose_name='上线时间')
    end_time = models.DateTimeField(verbose_name='下线时间')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "spot_boost"
        unique_together = [('boost', 'spot_id')]
        indexes = [models.Index(fields=["spot_id"])]