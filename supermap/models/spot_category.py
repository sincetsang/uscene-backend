import logging
from django.db import models

logger = logging.getLogger(__name__)


class SpotCategory(models.Model):
    type = models.CharField(max_length=20, default='')
    label = models.CharField(max_length=20, default='')
    label_zh = models.CharField(max_length=20, default='', verbose_name='中文名')
    label_zh_tw = models.CharField(max_length=20, default='', verbose_name='中文繁体名')
    label_ru = models.CharField(max_length=20, default='', verbose_name='俄语名')
    image_url = models.CharField(max_length=400, default='')
    sort_index = models.IntegerField(default=0)
    display = models.BooleanField(default=True, verbose_name='是否展示')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "spot_category"
