import logging
from django.db import models

logger = logging.getLogger(__name__)


class UserAttributeRewardsLog(models.Model):
    CATEGORY_CHOICES = [
        ('hash_rate', '算力'),
        ('stamina', '体力'),
        ('sign_in', '签到'),
    ]

    user_id = models.BigIntegerField(verbose_name="用户ID")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="奖励类别")
    label = models.CharField(max_length=50, verbose_name="标签", default="user_upgrade、buy_premium...")
    rewards = models.FloatField(default=0, verbose_name='奖励数值')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "user_attribute_rewards_log"
        verbose_name = "用户属性奖励记录"
        verbose_name_plural = "用户属性奖励记录"
        indexes = [
            models.Index(fields=['user_id'], name='idx_user_id'),  # 为 user_id 添加索引
        ]

    def __str__(self):
        return f"{self.user_id} - {self.category} - {self.rewards}"
