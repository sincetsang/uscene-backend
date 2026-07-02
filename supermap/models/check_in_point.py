import logging
from django.db import models

logger = logging.getLogger(__name__)


class CheckInPoint(models.Model):
    title = models.CharField(max_length=255, verbose_name="标题")
    title_en = models.CharField(max_length=255,default='', verbose_name="标题-英文")
    title_cn = models.CharField(max_length=255,default='', verbose_name="标题-中文")
    category = models.CharField(max_length=20, verbose_name="类别", null=True, blank=True)
    currency = models.CharField(max_length=20, verbose_name="币种", null=True, blank=True)
    balance = models.FloatField(default=0, verbose_name='余额')
    level = models.IntegerField(default=1, verbose_name="等级")
    hash_rate = models.FloatField(default=0, verbose_name='算力')
    landmark_image = models.CharField(max_length=255, verbose_name="地标图片", null=True, blank=True)
    country = models.CharField(max_length=50, verbose_name="国家", null=True, blank=True)
    region = models.CharField(max_length=50, verbose_name="省/地区", null=True, blank=True)
    city = models.CharField(max_length=50, verbose_name="城市", null=True, blank=True)
    place_id = models.CharField(max_length=100, verbose_name="地点ID", null=True, blank=True)
    location = models.CharField(max_length=255, verbose_name="具体位置", null=True, blank=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=8, verbose_name="纬度", null=True, blank=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=8, verbose_name="经度", null=True, blank=True)
    total_checked_in = models.IntegerField(default=0, verbose_name="总签到次数")
    status = models.IntegerField(default=0, verbose_name='是否展示')
    owner_id = models.BigIntegerField(default=0,verbose_name="owner_id")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    verification_code = models.CharField(max_length=32, verbose_name="核销码", default='', null=True, blank=True)
    description = models.TextField(verbose_name='描述', null=True, blank=True)
    description_en = models.TextField(verbose_name='描述-英文', default='', null=True, blank=True)
    description_cn = models.TextField(verbose_name='描述-中文', default='', null=True, blank=True)
    is_active = models.IntegerField(default=0, verbose_name="激活状态")
    external_url = models.CharField(max_length=100, verbose_name="外部链接", default='', null=True, blank=True)
    telegram_url = models.CharField(max_length=100, verbose_name="telegram", default='', null=True, blank=True)
    believe_url = models.CharField(max_length=150, verbose_name="believe", default='', null=True, blank=True)
    believe_id = models.CharField(max_length=150, verbose_name="believe_id", default='', null=True, blank=True)
    pcn_url = models.CharField(max_length=150, verbose_name="pcn url", default='', null=True, blank=True)
    whatsapp_url = models.CharField(max_length=150, verbose_name="whatsapp url", default='', null=True, blank=True)
    wechat = models.CharField(max_length=150, verbose_name="wechat", default='', null=True, blank=True)
    audit_status = models.IntegerField(default=0, verbose_name="审核状态")

    like_count = models.BigIntegerField(default=0, verbose_name='收藏数量')
    comment_count = models.BigIntegerField(default=0, verbose_name='用户评论数量')

    checkin_count = models.BigIntegerField(default=0, verbose_name='打卡数量')
    checkin_like_count = models.BigIntegerField(default=0, verbose_name='点赞数量')
    checkin_comment_count = models.BigIntegerField(default=0, verbose_name='打开评论数量')
    checkin_visit_count = models.BigIntegerField(default=0, verbose_name='浏览量')

    class Meta:
        db_table = "check_in_point"
        indexes = [
            models.Index(fields=['status', 'is_active', 'audit_status'], name='idx_check_in_point_status'),
            models.Index(fields=['latitude'], name='idx_check_in_point_latitude')
        ]
