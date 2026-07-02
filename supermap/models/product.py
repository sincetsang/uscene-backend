import logging
from django.db import models
from decimal import Decimal


logger = logging.getLogger(__name__)


class Product(models.Model):
    LEVEL_CHOICES = (
        (1, '普通会员'),
        (2, '高级会员'),
        (3, 'VIP会员'),
        (4, '至尊会员'),
    )

    name = models.CharField(max_length=100, default='')
    original_price = models.FloatField(default=0, verbose_name='原价')
    amount = models.FloatField(default=0, verbose_name='FEC金额')
    amount_usd = models.FloatField(default=0, verbose_name='金额(USD)')
    description = models.TextField(default='', verbose_name='描述', max_length=500)
    check_code_num = models.IntegerField(default=0, verbose_name='验证码数量')
    level = models.IntegerField(choices=LEVEL_CHOICES, default=1, verbose_name='产品级别')    
    level_tag = models.CharField(max_length=50, default='', verbose_name='级别标签')
    image = models.CharField(max_length=255, default='', verbose_name='产品图片, 废弃')
    category = models.CharField(max_length=20, default='official', verbose_name='产品类别')  # official: 官方, unofficial: 非官方
    check_in_point_id = models.BigIntegerField(default=0, verbose_name="地标ID")
    id = models.AutoField(primary_key=True)  # 或其他实际存在的字段名
    amount_currency = models.CharField(max_length=20, verbose_name="单位", default='FEC')
    tags = models.TextField(max_length=200, default='', blank=True, null=True, verbose_name='标签')
    visited_count = models.BigIntegerField(default=0, verbose_name='用户浏览过')
    comment_count = models.BigIntegerField(default=0, verbose_name='用户浏览过')
    favorite_count = models.BigIntegerField(default=0, verbose_name='收藏数量')
    audit_status = models.IntegerField(default=0, verbose_name="审核状态")
    is_active = models.BooleanField(default=True, verbose_name='上架状态')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "product"
        constraints = [
            models.UniqueConstraint(fields=['id'], name='unique_product_id'),  # 唯一索引
        ]