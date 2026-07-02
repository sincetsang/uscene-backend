import logging
from django.db import models
from decimal import Decimal

logger = logging.getLogger(__name__)


class ProductTagConfig(models.Model):
    tag_cn = models.CharField(max_length=20, default='')
    tag_en = models.CharField(max_length=20, default='')
    sort_index = models.IntegerField(default=0)
    mark = models.CharField(max_length=20, default='')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "product_tag_config"
