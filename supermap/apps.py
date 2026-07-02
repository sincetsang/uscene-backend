import logging
from django.apps import AppConfig
from django.db.models.signals import post_migrate

logger = logging.getLogger(__name__)

class ValidatorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'supermap'

    def ready(self):
        post_migrate.connect(app_ready_handler, self)


def app_ready_handler(sender, **kwargs):
    from supermap.models.config import Config
    try:
        Config.init_config()
    except Exception as e:
        logger.error('app_ready_handler error %s' % str(e))
