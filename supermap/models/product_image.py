import logging
from django.db import models
from decimal import Decimal


logger = logging.getLogger(__name__)


class ProductImage(models.Model):
    product_id = models.BigIntegerField()
    image_url = models.CharField(max_length=200, blank=True, null=True)
    sort_index = models.IntegerField(default=0, verbose_name='排序索引')
    status = models.IntegerField(default=1, verbose_name='状态(0:pending;1:approved;2:rejected)')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    image_type = models.CharField(max_length=10, default='small', verbose_name='图片类型(small:小图,large:大图)')

    class Meta:
        db_table = "product_image"
        constraints = [
            models.Index(fields=['product_id'], name='idx_product_id'),  # 普通复合索引
        ]