import logging
from django.db import models
from decimal import Decimal

logger = logging.getLogger(__name__)


class SpotBoostConfig(models.Model):
    MATCH_CHOICES = [
        ('all', 'All'),
        ('all_official', 'All_official'),
        ('specified', 'Specified'),  # 1,2,3,4
        ('early_bird', 'Early_bird'),  # 50:1,500:0.5
    ]
    match_type = models.CharField(max_length=20, default='', choices=MATCH_CHOICES, blank=True, null=True,
                                  verbose_name='all|specified')
    spots = models.TextField(default='', verbose_name='specified ids, 逗号分隔', blank=True, null=True)
    ratio = models.FloatField(default=0)
    remark = models.CharField(max_length=20, default='', verbose_name='备注')
    start_time = models.DateTimeField(verbose_name='上线时间')
    end_time = models.DateTimeField(verbose_name='下线时间')

    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return str(self.id) + '_' + self.match_type

    class Meta:
        db_table = "spot_boost_config"
