import re
import random
import string
from mysite.appconfig import AppConfig
from django.conf import settings
import requests

class utils(object):
    """
    timestamp's epoch
    """

    @classmethod
    def epochs(cls, timestamp):
        genesis_time = AppConfig.value_for_key(AppConfig.ETH_EPOCH_GENESIS_TIME)
        epoch_duration = AppConfig.value_for_key(AppConfig.ETH_EPOCH_DURATION_SECONDS)

        return int((int(timestamp) - int(genesis_time)) / int(epoch_duration))

    @classmethod
    def timestamp_of_epoch(cls, epoch):
        genesis_time = int(AppConfig.value_for_key(AppConfig.ETH_EPOCH_GENESIS_TIME))
        epoch_duration = int(AppConfig.value_for_key(AppConfig.ETH_EPOCH_DURATION_SECONDS))
        return genesis_time + epoch_duration * epoch

    @classmethod
    def reverse_by_step_2(cls, content):
        """
        以2为长度, 倒叙字符串
        :param content: 需要被倒叙的内容
        """
        split_list = re.findall(r'.{2}', content)
        split_list.reverse()
        return "".join(split_list)

    @classmethod
    def generate_secure_string(cls, length, use_numbers=True, use_lower=True, use_upper=True):
        """
        生成安全的随机字符串
        参数说明：
        length: 总长度（包括校验位）
        use_numbers: 是否使用数字
        use_lower: 是否使用小写字母
        use_upper: 是否使用大写字母
        """
        if length < 2:
            return ""

        # 构建字符集
        charset = ""
        if use_numbers:
            charset += string.digits
        if use_lower:
            charset += string.ascii_lowercase
        if use_upper:
            charset += string.ascii_uppercase
        if charset == "":
            charset = string.ascii_letters + string.digits  # 默认使用所有字符

        return cls._string_with_checksum(length, charset)

    @classmethod
    def _string_with_checksum(cls, n, charset):
        """
        生成带校验位的随机字符串
        n 是期望的总长度，包括校验位
        """
        if n < 2:
            return ""
        # 生成 n-1 位的随机字符串
        base_str = cls._generate_random_string(n-1, charset)
        # 计算校验位
        checksum = cls._calculate_luhn_checksum(base_str)
        # 返回带校验位的字符串
        return base_str + checksum

    @classmethod
    def _generate_random_string(cls, length, charset):
        """生成指定长度的随机字符串"""
        return ''.join(random.choice(charset) for _ in range(length))

    @classmethod
    def _calculate_luhn_checksum(cls, s):
        """
        使用 Luhn 算法计算校验位
        """
        # 将字符串转换为数字序列
        digits = []
        for c in s:
            if c.isdigit():
                digits.append(int(c))
            else:
                # 对于非数字字符，使用其 ASCII 码的最后一位
                digits.append(ord(c) % 10)

        # 从右向左，偶数位乘以2
        for i in range(len(digits) - 1, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] = digits[i] // 10 + digits[i] % 10

        # 计算所有数字的和
        total = sum(digits)

        # 计算校验位
        checksum = (10 - (total % 10)) % 10
        return str(checksum)

# send_lark_message 变为模块级函数
def send_lark_message(content, key="alarm"):
    if not settings.LARK.get("enable", False):
        return
    endpoint = settings.LARK["endpoint"] + settings.LARK["secret_access_keys"][key]
    data = {
        "msg_type": "text",
        "content": {"text": content}
    }
    try:
        resp = requests.post(endpoint, json=data, timeout=5)
        resp.raise_for_status()
    except Exception as e:
        # 可以加日志
        pass