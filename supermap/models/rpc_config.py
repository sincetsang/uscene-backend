from django.db import models


class RpcConfig(models.Model):

    name = models.CharField(default='', max_length=50)
    url = models.CharField(default='', max_length=200)
    type = models.CharField(default='', max_length=20, verbose_name='type:sol|ton')
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "rpc_config"
        verbose_name = "RPC配置"
        verbose_name_plural = "RPC配置"
