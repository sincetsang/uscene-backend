import logging
from django.db import models

logger = logging.getLogger(__name__)

class ShopAdminEventConfig(models.Model):
    contract = models.CharField(max_length=100)
    event_name = models.CharField(max_length=20)
    signature = models.CharField(max_length=100)
    memo = models.CharField(max_length=100)
    is_active = models.BooleanField()
    scan_speed = models.IntegerField()
    create_block = models.BigIntegerField()
    scan_block = models.BigIntegerField()
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()

    class Meta:
        db_table = "shop_admin_eventconfig"
        unique_together = ("contract", "signature")
        verbose_name = "event配置"
        verbose_name_plural = "event配置" 