import logging
from django.db import models

logger = logging.getLogger(__name__)


class PremiumOrder(models.Model):
    user_id = models.BigIntegerField()
    order_id = models.BigIntegerField(null=True, blank=True)
    comment = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    err_msg = models.CharField(max_length=50, blank=True, null=True)
    order_finished = models.BooleanField(null=True, blank=True)
    amount = models.BigIntegerField(null=True, blank=True)
    currency = models.CharField(max_length=10)
    value = models.CharField(max_length=30, blank=True, null=True)
    sol_address = models.CharField(max_length=100, blank=True, null=True)
    ton_address = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} - User {self.user_id}"

    class Meta:
        db_table = "premium_order"
