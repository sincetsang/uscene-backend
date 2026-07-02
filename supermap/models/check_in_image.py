import logging
from django.db import models
from .check_in import CheckIn

logger = logging.getLogger(__name__)


class CheckInImage(models.Model):

    check_in_id = models.BigIntegerField(default=0)
    image_url = models.CharField(max_length=255, verbose_name="图片地址")
    sort_index = models.IntegerField(default=0, verbose_name="排序索引")
    status = models.IntegerField(default=1, verbose_name="状态")
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)