import logging
from django.db import models
from .check_in_point import CheckInPoint

logger = logging.getLogger(__name__)


class CheckInMemberConfig(models.Model):

    period = models.CharField(max_length=20, default='')
    fec_price = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    fec_origin_price = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    usdt_price = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    usdt_origin_price = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    description = models.CharField(max_length=100, default='', blank=True, null=True)
    sort_index = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

