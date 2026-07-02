import logging
import json
import requests

from django.core import mail
from django.conf import settings
from supermap.models.config import Config
from enum import Enum
from supermap.tool.request import Request

logger = logging.getLogger(__name__)

class NotificationType(Enum):
    DAILY_REPORT = 'daily_report'
    HOUR_REPORT = 'hour_report'
    WEEK_REPORT = 'week_report'
    NOTICE_REPORT = 'notice_report'
    ALARM = 'alarm'

class Notification(object):

    @classmethod
    def send_contents(cls, contents, notification_type=NotificationType.NOTICE_REPORT):
        """
        :param contents: 行消息数组
        """
        notification_methods = Config.get_by_key("notification_methods")
        if 'ding' in notification_methods:
            cls.send_contents_ding(contents, notification_type)
        if 'lark' in notification_methods:
            cls.send_contents_lark(contents, notification_type)

    @classmethod
    def send_contents_ding(cls, contents, notification_type=NotificationType.NOTICE_REPORT):
        """
        :param contents: 行消息数组
        """
        try:
            logger.info('send_contents_ding')

            all_data = {
                "msgtype": "markdown",
                "markdown": {
                    "title": contents[0],
                    "text": "\n".join(contents)
                },
            }

            cls.send_ding(all_data, notification_type)
        except Exception as e:
            logger.info('send_contents_ding %s', str(e))


    @classmethod
    def send_contents_lark(cls, contents, notification_type=NotificationType.NOTICE_REPORT):
        """
        :param contents: 行消息数组
        """
        try:
            logger.info('send_contents_lark')

            # 格式化消息
            message = {
                "msg_type": "interactive",
                "card": {
                    "header": {
                        "title": {
                            "content": "【通知】{}".format(contents[0]),
                            "tag": "plain_text"
                        }
                    },
                    "elements": [
                        {
                            "tag": "markdown",
                            "text_size": "small",
                            "content": "\n".join(contents)
                        }
                    ]
                }
            }
            cls.send_lark(message, notification_type)

        except Exception as e:
            logger.info('send_contents_lark %s', str(e))

    @classmethod
    def send_ding(cls, data, notificationType: NotificationType):
        """
        发送钉钉消息
        """
        logger.info('send_ding %s', data)
        url = cls.ding_url(notificationType)

        json_data = json.dumps(data).encode(encoding="utf-8")

        header_encoding = {'User-Agent': 'Python3.9',
                           "Content-Type": "application/json"}
        res = requests.post(url, data=json_data, headers=header_encoding).json()
        logger.info('res %s', str(res))

    @classmethod
    def send_mail(cls, subject: str, message: str, from_email, recipient_list: list, html_message: str,
                  fail_silently: bool = False):
        logger.info('send_mail %s', message)
        logger.info("%s,%s,%s", subject, recipient_list, html_message)
        enable = settings.EMAIL_SEND_ENABLE
        if not enable:
            return
        mail.send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=fail_silently
        )

    @classmethod
    def ding_url(cls, notification_type: NotificationType):
        url = settings.DING['endpoint'] + settings.DING['secret_access_key']
        try:
            url = settings.DING['endpoint'] + settings.DING['secret_access_keys'][notification_type.value]
        except Exception as e:
            print(e)
            logger.error("ding_url error notification_type")
        print(url)
        return url

        # 发送Lark消息
    @classmethod
    def send_lark(cls, data, notification_type: NotificationType):
        logger.info('send_lark:\n %s', data)
        enable = bool(settings.LARK["enable"])
        if not enable:
            return
        json_data = json.dumps(data).encode(encoding="utf-8")
        headers = {'User-Agent': 'Python3.9', "Content-Type": "application/json; ; charset=utf-8"}
        url = cls.lark_url(notification_type)
        result = Request.post(url, data=json_data, headers=headers)
        logger.info(result)


    @classmethod
    def lark_url(cls, notification_type: NotificationType):
        url = settings.LARK['endpoint'] + settings.LARK['secret_access_keys']['daily_report']
        try:
            # 尝试使用 notification_type.value 查找对应的密钥
            url = settings.LARK['endpoint'] + settings.LARK['secret_access_keys'][notification_type.value]
        except KeyError as e:
            # 更详细的错误日志，显示缺失的键
            logger.error(f"KeyError: {e} - The key for {notification_type.value} is missing in secret_access_keys.")
        except Exception as e:
            # 捕获其他类型的异常
            logger.error(f"lark_url error: {str(e)}")
        return url