import logging
from django.db import models
from decimal import Decimal


logger = logging.getLogger(__name__)


class User(models.Model):
    user_id = models.BigIntegerField()
    password = models.CharField(max_length=128, verbose_name='密码', null=True, blank=True)
    nickname = models.CharField(max_length=50, default='')
    avatar_url = models.CharField(max_length=200, blank=True, null=True)
    level = models.IntegerField(default=1, verbose_name='用户等级')
    invite_code = models.CharField(max_length=50, verbose_name='邀请码')
    hash_rate = models.FloatField(default=0, verbose_name='算力')
    stamina = models.IntegerField(default=0, verbose_name='体力')
    remaining_stamina = models.IntegerField(default=0, verbose_name='剩余体力')
    available_signins = models.IntegerField(default=1)
    is_premium = models.IntegerField(default=1)
    balance = models.FloatField(default=0, verbose_name='余额')
    latitude = models.DecimalField(max_digits=12, decimal_places=8, blank=True, null=True, default=Decimal('0.000000'))
    longitude = models.DecimalField(max_digits=12, decimal_places=8, blank=True, null=True, default=Decimal('0.000000'))
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    moved_at = models.DateTimeField(auto_now_add=True,  blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    identity_tag = models.IntegerField(default=0, verbose_name='身份标签')   
    identity_name = models.CharField(max_length=50, default='', verbose_name='身份标签')
    description = models.TextField(max_length=200, default='', null=True, blank=True)

    class Meta:
        db_table = "user"
        constraints = [
            models.UniqueConstraint(fields=['user_id'], name='unique_user_id'),  # 唯一索引
        ]