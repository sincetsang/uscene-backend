import logging
from django.db import models

logger = logging.getLogger(__name__)


class OTA(models.Model):
    PLATFORM_CHOICES = [
        ('ios.cn', 'iOS-国内'),
        ('ios.global', 'iOS-海外'),
        ('android.cn', 'Android-国内'),
        ('android.global', 'Android-海外'),
    ]

    FORCE_UPDATE_CHOICES = [
        ('force', '强制更新'),
        ('optional', '可选更新'),
    ]

    version = models.CharField(max_length=50, verbose_name='版本号')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, verbose_name='平台')
    force_update = models.CharField(max_length=20, choices=FORCE_UPDATE_CHOICES, default='optional', verbose_name='更新类型')
    download_url = models.CharField(max_length=255, verbose_name='下载地址')
    release_notes = models.TextField(verbose_name='更新说明')
    min_version = models.CharField(max_length=50, verbose_name='最低支持版本', blank=True, null=True)
    file_size = models.BigIntegerField(verbose_name='文件大小(字节)', default=0)
    md5 = models.CharField(max_length=32, verbose_name='文件MD5', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = "ota"
        verbose_name = "APP版本更新"
        verbose_name_plural = "APP版本更新"
        indexes = [
            models.Index(fields=['platform', 'version']),
            models.Index(fields=['is_active']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.platform} v{self.version}"
