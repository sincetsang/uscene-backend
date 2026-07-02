import logging
from typing import Union
import random

import pytz
import time
import base64
import json
import random
import string
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from django.db import transaction
from supermap.models.address_transaction import AddressTransaction
from supermap.models.user_pay_record import UserPayRecord
from supermap.models.user import User
from mysite.appconfig import AppConfig

logger = logging.getLogger(__name__)


class UserService(object):

    @classmethod
    @transaction.atomic()
    def check_primary(cls):
        logger.info('check_primary')
        txs = AddressTransaction.objects.filter(pay_checked=False, pay_type='primary')
        for tx in txs:
            UserService._update_user_primary(tx)

    @classmethod
    def _update_user_primary(cls, tx: AddressTransaction):
        logger.info("update_user_primary %s %s %s" % (tx.hash, tx.amount, tx.currency))
        old_record = UserPayRecord.objects.filter(wallet_address__iexact=tx.from_address,
                                                  transaction_hash=tx.hash,
                                                  lt=tx.lt).order_by('lt').first()

        if old_record:
            tx.pay_checked = True
            tx.save()
            return

        user: User = User.objects.filter(wallet_address__iexact=tx.from_address).first()
        if not user:
            logger.info("update_user_primary no user %s %s %s" % (tx.hash, tx.amount, tx.currency))
            return

        comment_arr = tx.comment.split('-')
        if len(comment_arr) < 2:
            return
        if comment_arr[0].lower() != 'primary':
            return
        if str(comment_arr[1]) != str(user.user_id):
            logger.info("update_user_primary uid != user.user_id")
            return
        logger.info("update_user_primary %s %s %s %s" % (tx.hash, tx.amount, tx.currency, user.user_id))

        address = AppConfig.value_for_key(AppConfig.PRIMARY_ACCEPT_ADDRESS)
        denom = AppConfig.value_for_key(AppConfig.PRIMARY_DENOM)
        price = AppConfig.value_for_key(AppConfig.PRIMARY_PRICE)
        logger.info(f'update_user_primary config  {address} {denom} {price}')
        if not address or not denom or not price:
            logger.info(f'update_user_primary config not correct {address} {denom} {price}')
            return
        if address.lower() != tx.to_address.lower() or denom.lower() != tx.currency.lower() or int(price) != int(
                tx.amount) or not tx.comment or (tx.comment and tx.comment.lower() != str(user.user_id)):
            logger.warning(
                f'update_user_primary {user.user_id} hash:{tx.hash}, payment miss match config {address.lower() != tx.to_address.lower()},{denom.lower() != tx.currency.lower()} {int(price) != int(tx.amount)} {tx.comment}')
            tx.pay_checked = True
            tx.save()
            return
        record = UserPayRecord()
        record.timestamp = tx.timestamp
        record.wallet_address = tx.from_address
        record.lt = tx.lt
        record.user_id = user.user_id
        record.transaction_status = 1
        record.transaction_amount = tx.amount
        record.transaction_hash = tx.hash
        record.save()

        now_date = datetime.now(pytz.utc)
        if user.primary_end_at <= now_date:
            user.primary_start_at = now_date
            end_date = now_date + timedelta(days=30)
            user.primary_end_at = end_date
            user.created_at = end_date
            logger.info(f'save user primary 0 {end_date} {user.user_id} {user.primary_end_at}')
            user.save()
            UserService.addUpgradeHistory(user=user, renew=False)
        else:
            user.primary_end_at = user.primary_end_at + timedelta(days=30)
            logger.info(f'save user primary 1 {user.primary_end_at}')
            user.save()
            UserService.addUpgradeHistory(user=user, renew=True)
            logger.info('User primary dates saved successfully.')

        tx.pay_checked = True
        tx.save()

   