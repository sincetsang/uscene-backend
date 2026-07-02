import logging
import json
import jwt
import time
import requests
from eth_account import Account
from eth_account.messages import encode_defunct
from django.conf import settings
from functools import reduce
from decimal import Decimal
from supermap.models import Config
from rest_framework.response import Response
from rest_framework import status
from apis.results import Result
from django.core.cache import cache
from supermap.notification.notification import Notification
from supermap.notification.notification import NotificationType

logger = logging.getLogger(__name__)


def verifity_sign(text, signature, address):
    """
    验证钱包签名
    :param text: 原文本
    :param signature: 签名
    :param address: 公钥
    :return: 验证结果
    """
    try:
        message = encode_defunct(text=text)
        address_new = Account.recover_message(message, signature=signature)
        if address.upper() == address_new.upper():
            return True
        else:
            return False
    except:
        return False


def verify_params(params, arr):
    """
    验证参数齐全
    :param params: 参数
    :param arr: 需要验证的参数数组
    """
    return reduce(lambda x, y: x and y, map(lambda x: params.get(x) != None, arr))


def sum_gas_fee_of(address):
    """
    统计某地址获取的总gas fee
    """
    reward = Decimal(0)
    try:
        url = "%s/api?module=account&action=getminedblocks&address=%s&blocktype=blocks&apikey=%s" % (
            settings.ETH['api_url'], address, settings.ETH['api_key'])
        ret = requests.get(url).json()
        if ret['status'] == '1':
            for tx in ret['result']:
                reward = reward + Decimal(tx['blockReward'])

        return reward / Decimal(1e18)
    except Exception as e:
        logger.error("eth_fee unclaimed_reward err%s", str(e))
        Notification.send_template_ding('handled_exception', {"msg": e}, notification_type=NotificationType.ALARM_REPORT)
        return reward
    return None


def get_current_slot():
    """
    获取当前slot
    """
    url = "%s/eth/v1/node/syncing" % (settings.ETH2['endpoint'])
    headers = {'content-type': 'application/json'}
    try:
        res = requests.get(url, headers=headers).json()
        if res['data']:
            return int(res['data']['head_slot'])
    except Exception as e:
        logger.error("eth get_current_slot err%s", str(e))
        Notification.send_template_ding('handled_exception', {"msg": e}, notification_type=NotificationType.ALARM_REPORT)
    return False


def clean_cache(keys=[]):
    """
    删除缓存，在数据更新时触发
    :param keys: 待删缓存key数组
    """
    try:
        for key in keys:
            cache.delete(key)
        return True
    except Exception as e:
        logger.error("clean cache err%s", str(e))
        Notification.send_template_ding('handled_exception', {"msg": e}, notification_type=NotificationType.ALARM_REPORT)
    return False
