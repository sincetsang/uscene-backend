from asgiref.sync import sync_to_async
from django.conf import settings
from supermap.models.config import Config


class AppConfig(object):
    DING_ENABLE = 'ding_enable'
    TON_PRIMARY_RECEIPT = 'ton_primary_receipt'
    SOL_SPOT_RECEIPT = 'sol_spot_receipt'
    SOL_SPOT_ADDRESS = 'spot_sol_accept_address'
    TON_SPOT_RECEIPT = 'spot_accept_address'
    PRIMARY_ACCEPT_ADDRESS = 'primary_accept_address'
    PRIMARY_PRICE = 'primary_price'
    PRIMARY_DENOM = 'primary_denom'

    TRANSFER_SPOT_RATE = 'transfer_spot_rate'
    TRANSFER_SPOT_REFUND_RATE = 'transfer_spot_refund_rate'

    SPOT_PRICE_LEVEL = "spot_price_level"

    SPOT_FIRST_BUY_COMMISSION = "spot_first_buy_commission"

    @classmethod
    def config(cls):
        config_ret = Config.objects.all()
        return config_ret

    @classmethod
    def value_for_key(cls, key):
        config = cls.config().filter(_key=key).first()
        if config:
            return config._value
        return None

    @classmethod
    @sync_to_async
    def async_value_for_key(cls, key):
        return AppConfig.value_for_key(key)

    @classmethod
    def save(cls, key, value, value_type, force=False):
        config_old = Config.objects.filter(_key=key)
        if len(config_old):
            if force:
                config = Config(id=config_old[0].id, _key=key, _value=value,
                                created_time=config_old[0].created_time)
                config.save(force_update=force)
        else:
            config = Config(_key=key, _value=value)
            config.save()
