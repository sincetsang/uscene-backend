import logging
from django.db import models

logger = logging.getLogger(__name__)


class Banner(models.Model):
    image_url = models.CharField(max_length=200, default='')
    link_type = models.CharField(max_length=20, default='', verbose_name='external、inside、image、activity')
    link_url = models.CharField(max_length=200, default='', verbose_name='要跳转的外部url', null=True, blank=True)
    show_start_at = models.DateTimeField(blank=True, verbose_name='展示开始时间')
    show_end_at = models.DateTimeField(blank=True, verbose_name='展示结束时间')
    activity_short_id = models.CharField(max_length=20, default='', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "banner"
