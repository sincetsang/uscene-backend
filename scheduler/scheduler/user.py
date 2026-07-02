import logging

from supermap.service.user_service import UserService
from django_apscheduler.models import DjangoJobExecution

logger = logging.getLogger(__name__)


class UserTask(object):

    @classmethod
    def update_order(cls):
        logging.info('UserTask update_primary')
        UserService.check_primary()
        # UserService.check_spot_pay()
        # UserService.check_out_of_date_spot_order()

