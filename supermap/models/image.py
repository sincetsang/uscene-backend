import logging
from django.db import models

logger = logging.getLogger(__name__)


class Image (models.Model):
    CATEGORY_CHOICES = [
        ('spot', 'Spot'),
        ('avatar', 'Avatar'),
        ('task', 'Task'),
        ('other', 'Other'),
    ]
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES,)
    remark = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True, null=True)
    keep_source_name = models.BooleanField(default=False)

    class Meta:
        db_table = "image"

    def __str__(self):
        return f"{self.category} - {self.remark}"

