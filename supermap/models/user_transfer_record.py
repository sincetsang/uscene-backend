import logging
from django.db import models
from decimal import Decimal

logger = logging.getLogger(__name__)


class UserTransferRecord(models.Model):
    sender_id = models.BigIntegerField()
    sender_name = models.CharField(max_length=100)
    receive_id = models.BigIntegerField()
    receive_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
    fee = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "user_transfer_record"
