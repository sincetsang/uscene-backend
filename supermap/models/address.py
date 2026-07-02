import logging
from django.db import models

logger = logging.getLogger(__name__)


class Address(models.Model):
    user_id = models.BigIntegerField(default=0, verbose_name="用户ID")
    name = models.CharField(max_length=20, default='')
    phone = models.CharField(max_length=20, default='')
    area = models.TextField(max_length=50)
    detail = models.TextField(max_length=200)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "address"
