import logging

logger = logging.getLogger(__name__)
class Result:
    code = 0
    msg = ""
    data = None
    success = True

    MESSAGE_DICT = {
        'en': {
            'success': 'Success',
            'system_error': 'Please try again later',
            'invalid_params': 'Error',
            'pubkey_existed': 'An existing validator is found, please check again to avoid double-signature penalty.',
        },
        'zh': {
            'success': '成功',
            'system_error': '请稍后重试',
            'invalid_params': '参数错误, 请检查',
            'pubkey_existed': '发现已存在的验证者, 请检查, 避免双签惩罚',
        }
    }

    CODE_DICT = {
        200: 'SUCCESS',
        400: 'INVALID_PARAMS',
        401: 'INVALID_TOKEN',
        402: 'PUBKEY_EXISTED',
        403: 'MISMATCH_REWARD_ADDRESS',
        500: 'SYSTEM_ERROR',
    }

    def __init__(self, code: int, msg: str, data: object = None, success: bool = True):
        self.code = code
        self.msg = msg
        self.data = data
        self.success = success

    @classmethod
    def get_msg(cls, code, language='en', other_msgs=[], request = None):
        """
        根据code和语言, 获取提示语, 并拼接其他内容
        """
        if language not in ['en', 'zh']:
            if language.lower().startswith('zh'):
                language = 'zh'
            elif language.lower().startswith('en'):
                language = 'en'
            elif 'zh' in language.lower() or 'cn' in language.lower():
                language = 'zh'
            else:
                language = 'en'
        if code != 'success':
            logger.warning('request fail, %s', code)
            if request:
                logger.warning('request.method: %s', request.method)
                logger.warning('request.path: %s', request.path)
                logger.warning('request.headers: %s', request.headers)
                logger.warning('request ip: %s', request.META.get('REMOTE_ADDR'))
                logger.warning('request.data: %s', request.data)
                logger.warning('request.GET: %s', request.GET)
                logger.warning('request.POST: %s', request.POST)
                logger.warning('request.META: %s', request.META)
        msg = cls.MESSAGE_DICT[language].get(code)
        msg = msg or 'unknow msg'
        return ','.join([str(m) for m in [msg] + other_msgs])


Success = Result(code=200, msg=Result.get_msg('success', 'en', []), success=True)
Failure = Result(code=400, msg="Failure", success=False)
