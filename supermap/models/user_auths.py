import logging
from django.db import models

logger = logging.getLogger(__name__)


class UserAuth(models.Model):
    user = models.ForeignKey('User', to_field='user_id', on_delete=models.CASCADE, related_name='user_auths')
    provider = models.CharField(max_length=50, verbose_name='第三方提供者')
    external_id = models.CharField(max_length=100, verbose_name='外部用户 ID')
    wallet_address = models.CharField(max_length=100, blank=True, null=True, verbose_name='钱包地址')
    access_token = models.CharField(max_length=255, blank=True, null=True, verbose_name='访问令牌')
    refresh_token = models.CharField(max_length=255, blank=True, null=True, verbose_name='刷新令牌')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        db_table = 'user_auths'
        constraints = [
            models.UniqueConstraint(fields=['user', 'provider'], name='unique_user_provider')
        ]
