import logging
from django.db import models
from mysite import settings

logger = logging.getLogger(__name__)


class Config (models.Model):
    _key = models.CharField(max_length=255, unique=True)
    _value = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "config"

    @classmethod
    def init_config(cls):
        cons = settings.APP_CONFIG
        for con in cons:
            logger.info('init config')
            conf = Config.objects.filter(_key=con['key'])
            if not len(conf):
                new_con = Config(_key=con['key'], _value=con['value'])
                new_con.save()
            else:
                logger.warning('warning: config key: %s value: %s exists' % (conf[0]._key, conf[0]._value))

    @classmethod
    def get_by_key(cls, _key, default='lark'):
        """
        获取一个配置
        :param _key: 配置的名字
        :param default: 未查询到配置时，返回的默认值
        """
        item = cls.objects.filter(_key=_key).first()
        if not item:
            return default
        return item._value  # 访问第一个匹配的配置项
