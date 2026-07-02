import logging
from django.db import models

logger = logging.getLogger(__name__)


class AddressTransaction(models.Model):
    hash = models.CharField(max_length=66)
    from_address = models.CharField(max_length=50, verbose_name='from address')
    to_address = models.CharField(max_length=50, verbose_name='to address')
    lt = models.BigIntegerField()
    status = models.CharField(max_length=20)
    amount = models.FloatField()
    timestamp = models.BigIntegerField()
    currency = models.CharField(max_length=20, default='')
    comment = models.CharField(max_length=50, default='')
    message = models.CharField(max_length=200)
    pay_checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    pay_type = models.CharField(max_length=20, default='')
    need_check = models.BooleanField(default=True)

    class Meta:
        db_table = "address_transaction"
        unique_together = ['hash', 'from_address', 'to_address']
        indexes = [models.Index(fields=['hash'])]