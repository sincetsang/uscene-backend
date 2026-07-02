import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Conversation(models.Model):
    id = models.CharField(max_length=13,primary_key=True)
    user_id = models.BigIntegerField(default=0)
    title = models.CharField(max_length=255, blank=True, verbose_name='对话标题')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_active = models.BooleanField(default=True, verbose_name='是否活跃')

    class Meta:
        db_table = 'chat_conversation'
        ordering = ['-updated_at']
        verbose_name = '对话'
        verbose_name_plural = '对话'


class Message(models.Model):
    ROLE_CHOICES = (
        ('user', '用户'),
        ('assistant', '助手'),
        ('system', '系统'),
    )
    
    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(default=0)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name='角色')
    content = models.TextField(verbose_name='内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_error = models.BooleanField(default=False, verbose_name='是否错误')

    class Meta:
        db_table = 'chat_message'
        ordering = ['created_at']
        verbose_name = '消息'
        verbose_name_plural = '消息'

    def __str__(self):
        return f"{self.role} - {self.content[:20]}..."


class ChatConfig(models.Model):
    """聊天配置表，用于管理推荐的对话列表"""
    conversation_id = models.CharField(max_length=13,primary_key=True)
    title = models.CharField(max_length=255, verbose_name='标题')
    description = models.TextField(verbose_name='描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    sort_order = models.IntegerField(default=0, verbose_name='排序')

    class Meta:
        db_table = 'chat_config'
        ordering = ['sort_order', '-created_at']
        verbose_name = '聊天配置'
        verbose_name_plural = '聊天配置'

    def __str__(self):
        return self.title 