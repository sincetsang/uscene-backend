import logging
from django.db import models

logger = logging.getLogger(__name__)


class Complaint(models.Model):
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('resolved', '已解决'),
        ('rejected', '已拒绝'),
    ]

    TYPE_CHOICES = [
        ('info_error', '地标信息有误(如名称，描述，图片)'),
        ('illegal_content', '地标内容涉及违法违规内容'),
        ('other_issues', '地标有其他问题，我要举报'),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='投诉类型')
    check_in_point_id = models.BigIntegerField(verbose_name='打卡点ID')
    user_id = models.BigIntegerField(verbose_name='投诉用户ID')
    description = models.TextField(verbose_name='投诉描述')
    images = models.TextField(verbose_name='投诉图片', blank=True, null=True)  # 存储图片URL，多个图片用逗号分隔
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='处理状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = "complaint"
        verbose_name = "投诉"
        verbose_name_plural = "投诉"
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['check_in_point_id']),
            models.Index(fields=['status']),
        ]
