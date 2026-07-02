import logging
from django.db import models

logger = logging.getLogger(__name__)

class AddressCheckpoint(models.Model):
    address = models.CharField(max_length=42, unique=True)
    chain = models.CharField(max_length=20)
    currency = models.CharField(max_length=10)
    last_check_block = models.BigIntegerField()
    last_check_time = models.DateTimeField()
    is_active = models.BooleanField()
    error_count = models.IntegerField()
    last_error = models.TextField()
    description = models.CharField(max_length=200)
    metadata = models.JSONField()
    contract_address = models.CharField(max_length=42)
    token_decimals = models.IntegerField()

    class Meta:
        db_table = "address_checkpoints"
        verbose_name = "支付方式列表"
        verbose_name_plural = "支付方式列表" 