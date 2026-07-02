import logging
import asyncio
import threading

from supermap.service.sol import SolService
logger = logging.getLogger(__name__)


class SolTask(object):

    @classmethod
    def sync_payment_tx(cls):
        SolService.sync_sol_transaction()

