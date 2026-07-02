import logging
from django.db import models

logger = logging.getLogger(__name__)


class SolTransaction(models.Model):
    hash = models.CharField(max_length=100)
    from_address = models.CharField(max_length=50, verbose_name='from address')
    to_address = models.CharField(max_length=50, verbose_name='to address')
    # slot
    lt = models.BigIntegerField()
    status = models.CharField(max_length=20)
    amount = models.FloatField()
    value = models.CharField(default='', blank=True, null=True, max_length=20)
    timestamp = models.BigIntegerField()
    currency = models.CharField(max_length=20, default='')
    comment = models.CharField(max_length=50, default='', blank=True, null=True)
    token_address = models.CharField(max_length=50, verbose_name='token address')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    pay_checked = models.BooleanField(default=False)
    need_check = models.BooleanField(default=True)
    pay_type = models.CharField(max_length=20, default='')
    instruction_index = models.IntegerField(default=0)

    class Meta:
        db_table = "sol_transaction"
        unique_together = ['hash', 'lt', 'from_address', 'to_address', 'instruction_index']
        indexes = [models.Index(fields=['hash']), models.Index(fields=['lt'])]