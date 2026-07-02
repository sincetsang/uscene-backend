import logging
from django.db import models

logger = logging.getLogger(__name__)


class UserWithdrawOrder(models.Model):
    REFERRALS_CHOICES = [
        ('in_review', 'InReview'),
        ('success', 'Success'),
        ('refuse', 'Refuse'),
    ]
    order_id = models.CharField(max_length=20, default='', null=True, blank=True)
    user_id = models.BigIntegerField()
    withdraw_status = models.CharField(max_length=20,  default='unclaimed', choices=REFERRALS_CHOICES)
    currency = models.CharField(max_length=20, default='')
    amount = models.BigIntegerField()
    value = models.CharField(max_length=50, default='')
    withdraw_wallet_address = models.CharField(max_length=100, default='', null=True, blank=True)
    withdraw_tx_hash = models.CharField(max_length=100, default='', null=True, blank=True)
    withdraw_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "user_withdraw_order"
        indexes = [models.Index(fields=['user_id'])]
        constraints = [
            models.UniqueConstraint(fields=['order_id'], name='unique_order_id'),
        ]