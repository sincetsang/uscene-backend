import logging
from django.db import models
from decimal import Decimal


logger = logging.getLogger(__name__)


class UserImage(models.Model):
    user_id = models.BigIntegerField()
    spot_id = models.BigIntegerField()
    image_url = models.CharField(max_length=200, blank=True, null=True)
    status = models.IntegerField(default=0, verbose_name='鉴黄审核状态(0:未审核,1:审核通过,2:审核不通过)')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "user_image"
        constraints = [
            models.Index(fields=['user_id', 'spot_id'], name='idx_user_spot'),  # 普通复合索引
        ]