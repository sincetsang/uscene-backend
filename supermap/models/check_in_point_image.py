import logging
from django.db import models
from .check_in_point import CheckInPoint

logger = logging.getLogger(__name__)


class CheckInPointImage(models.Model):
    check_in_point = models.ForeignKey(CheckInPoint, on_delete=models.CASCADE, verbose_name="关联地标", related_name="images")
    image_url = models.CharField(max_length=255, verbose_name="图片地址")
    sort_index = models.IntegerField(default=0, verbose_name="排序索引")
    status = models.IntegerField(default=1, verbose_name="状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "check_in_point_image"
        ordering = ['sort_index', '-created_at']
        verbose_name = "地标图片"
        verbose_name_plural = "地标图片"

    def __str__(self):
        return f"{self.check_in_point.title} - 图片{self.id}" 
