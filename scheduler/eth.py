import logging
from django.conf import settings
import requests, json
import os
logger = logging.getLogger(__name__)

# rpcUrl = "https://1rpc.io/sepolia"
# rpcUrl = "http://51.210.222.104:8545"
rpcUrl = os.getenv('BACKEND_ETH1_RPC') or ''

class ETHService(object):

    @classmethod
    def latest_block(cls):
        payload = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "eth_blockNumber",
            "params": []
        }
        headers = {'content-type': 'application/json'}
        resp = requests.post(rpcUrl, data=json.dumps(payload), headers=headers).json()
        return int(resp['result'], 16)

    @classmethod
    def receipt(cls, hash):
        payload = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "eth_getTransactionReceipt",
            "params": [hash]
        }
        # print('hash', hash)
        headers = {'content-type': 'application/json'}
        resp = requests.post(rpcUrl, data=json.dumps(payload), headers=headers).json()
        # print(resp)
        if isinstance(resp['result'], dict):
            if resp['result'].__contains__("status"):
                return bool(resp['result']['status'])
            return None
        return None

    @classmethod
    def latest_finalized_block(cls):
        eth1_endpoint = rpcUrl
        payload = {
            'jsonrpc': '2.0',
            'method': 'eth_getBlockByNumber',
            'params': ['finalized', False],
            'id': 1
        }
        headers = {
            'Content-Type': 'application/json'
        }
        ret = requests.post(url=eth1_endpoint, data=json.dumps(payload), headers=headers).json()
        logger.info('get_latest_finalized_block ret1 json %s', ret)
        latest_finalized_block = int(ret['result']['number'], 16)
        return latest_finalized_block

    @classmethod
    def get_block_by_number(cls, block_number: int):
        block_detail = None
        try:
            eth1_endpoint = rpcUrl
            payload = {
                'jsonrpc': '2.0',
                'method': 'eth_getBlockByNumber',
                'params': [hex(block_number), False],
                'id': 1
            }
            headers = {
                'Content-Type': 'application/json'
            }
            ret = requests.post(url=eth1_endpoint, data=json.dumps(payload), headers=headers).json()
            return ret
        except Exception as e:
            logger.error('WithdrawalTask get_latest_finalized_block err %s', str(e))

        return block_detail

    @classmethod
    def get_latest_finalized_block(cls):
        latest_finalized_block = None
        try:
            eth1_endpoint = rpcUrl
            print(eth1_endpoint)
            payload = {
                'jsonrpc': '2.0',
                'method': 'eth_getBlockByNumber',
                'params': ['finalized', False],
                'id': 1
            }
            headers = {
                'Content-Type': 'application/json'
            }
            ret = requests.post(url=eth1_endpoint, data=json.dumps(payload), headers=headers).json()
            latest_finalized_block = int(ret['result']['number'], 16)
            return latest_finalized_block
        except Exception as e:
            logger.error('get_latest_finalized_block err %s', str(e))

        return latest_finalized_block