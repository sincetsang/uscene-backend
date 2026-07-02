import base64
import logging
import json
import random
import time
from django.db import transaction
from solana.rpc.api import Client
from solana.rpc.commitment import Confirmed, Finalized
from solders.signature import Signature
from solders.pubkey import Pubkey
from heyos.models.sol_transaction import SolTransaction
from mysite.appconfig import AppConfig
from heyos.models.rpc_config import RpcConfig
from heyos.notification.notification import Notification, NotificationType

logger = logging.getLogger(__name__)

# client = Client("https://api.mainnet-beta.solana.com")

DEFAULT_RPC = "https://evocative-proportionate-owl.solana-mainnet.quiknode.pro/d98f73d8c5b25341a7a33ea038a7152e0f4e61b1"
SOL_PROGRAMID = "11111111111111111111111111111111"
# USDT_MINT = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"
USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

class SolClient(object):
    client: Client
    rpc_config: RpcConfig

    def __init__(self, sol_client, rpc_config):
        self.client = sol_client
        self.rpc_config = rpc_config


class SolService(object):

    @classmethod
    def get_client(cls) -> SolClient:
        rpc: RpcConfig = RpcConfig.objects.filter(type='sol', active=True).first()
        if not rpc:
            rpcs: [RpcConfig] = RpcConfig.objects.filter(type='sol').all()
            rpc = rpcs[random.randint(0, len(rpcs)-1)]
            # rpc: RpcConfig = RpcConfig.objects.filter(type='sol').first()
        return SolClient(sol_client=Client(rpc.url, timeout=3), rpc_config=rpc)


    @classmethod
    def get_token_account_info(cls, token_account):
        logger.info(f'get_token_account_info')
        res = cls.get_client().client.get_account_info_json_parsed(pubkey=Pubkey.from_string(token_account),
                                                                   commitment=Confirmed).to_json()
        res = json.loads(res)
        value = res['result']['value']
        if value:
            data = value.get('data')
            if isinstance(data, dict) and data.get('parsed'):
                parsed = data.get('parsed')
                info = parsed['info']
                mint = info['mint']
                owner = info['owner']
                return owner, mint
        return None, None

    @classmethod
    def get_transaction_history(cls, address, before_signature=None, limit=100, until=None):
        params = {
            "limit": limit,
            "before": Signature.from_string(before_signature)
        } if before_signature else {
            "limit": limit
        }
        if until:
            params['until'] = Signature.from_string(until)
        params['commitment'] = Finalized
        pubkey = Pubkey.from_string(address)
        result = None
        sol_client = cls.get_client()
        try:
            response = sol_client.client.get_signatures_for_address(pubkey, **params)
            res_json = json.loads(response.to_json())
            result = res_json['result']
            sol_client.rpc_config.active = True
        except Exception as e:
            sol_client.rpc_config.active = False
            cls.send_alert([f'err: sol sync failed', f'rpc:{sol_client.rpc_config.name}'])
        sol_client.rpc_config.save()
        return result

    @classmethod
    def send_alert(cls, messages):
        content = ['【告警】Sol sync tx 失败']
        for message in messages:
            content.append(f'- {message}')
        # all_data = {
        #     "msgtype": "markdown",
        #     "markdown": {
        #         "title": "【告警】Sol sync tx 失败",
        #         "text": "\n".join(content)
        #     },
        # }
        Notification.send_contents(content, NotificationType.ALARM)

    @classmethod
    def get_transaction_details(cls, signature, address, owner, address_type):
        sig = Signature.from_string(signature)
        response = cls.get_client().client.get_transaction(tx_sig=sig, encoding='jsonParsed', commitment=Confirmed, max_supported_transaction_version=0)
        res_json = json.loads(response.to_json()).get('result')
        if not res_json:
            return []
        # print(res_json)
        meta = res_json.get('meta', {})
        err = meta.get('err', None)
        if err:
            return []
        blockTime = int(res_json.get('blockTime'))
        slot = int(res_json.get('slot'))
        transfers = []
        memo = None
        instructions = res_json['transaction']['message']['instructions']
        for instruction in instructions:
            if instruction.get('program') == 'spl-memo':
                memo = instruction.get('parsed')
        for index, instruction in enumerate(instructions):
            if instruction.get('programId') == SOL_PROGRAMID:
                parsed = instruction.get('parsed', {})
                info = parsed.get('info', {})
                if info.get('destination') == address and parsed.get('type') == 'transfer':
                    destination = info.get('destination')
                    source = info.get('source')
                    amount = info.get('lamports')
                    value = f"{int(amount) / 1e9:.9f}".rstrip('0').rstrip('.')
                    currency = 'SOL'
                    transfer = SolTransaction(lt=slot,
                                              hash=signature,
                                              from_address=source,
                                              to_address=address,
                                              status='success',
                                              amount=amount,
                                              value=value,
                                              currency=currency,
                                              timestamp=blockTime,
                                              comment=memo,
                                              token_address='SOL',
                                              need_check=True if memo else False,
                                              instruction_index=index,
                                              pay_type=address_type)
                    transfers.append(transfer)
            elif instruction.get('program') == 'spl-token':
                parsed = instruction.get('parsed', {})
                info = parsed.get('info', {})
                if parsed.get('type') == 'transfer' or parsed.get('type') == 'transferChecked':
                    currency = 'USDC'
                    amount = None
                    value = None
                    destination = info.get('destination')
                    source = info.get('source')
                    authority = info.get('authority')
                    des_owner, des_mint = cls.get_token_account_info(destination)
                    source_owner, source_mint = cls.get_token_account_info(source)
                    mint = info.get('mint')
                    if des_owner != owner:
                        logger.warning(f"------des_owner:{des_owner}, owner:{owner}")
                        continue
                    if des_mint != USDC_MINT and mint != USDC_MINT:
                        logger.warning(f"get_transaction_details signature:{signature} des_mint:{des_mint} mint:{mint}, USDC_MINT:{USDC_MINT} ")
                        continue
                    if source_owner:
                        source = source_owner
                    else:
                        if authority:
                            source = authority
                    if des_mint == USDC_MINT or mint == USDC_MINT:
                        _amount = info.get('amount')
                        if _amount:
                            amount = int(_amount)
                            value = f"{int(_amount) / 1e6:.6f}".rstrip('0').rstrip('.')
                        else:
                            tokenAmount = info.get('tokenAmount')
                            if tokenAmount:
                                amount = tokenAmount.get('amount')
                                value = tokenAmount.get('uiAmountString')
                    else:
                        continue
                    if source and destination == address and amount is not None and value is not None:
                        transfer = SolTransaction(lt=slot,
                                                  hash=signature,
                                                  from_address=source,
                                                  to_address=owner,
                                                  status='success',
                                                  amount=amount,
                                                  value=value,
                                                  currency=currency,
                                                  timestamp=blockTime,
                                                  comment=memo,
                                                  token_address=USDC_MINT,
                                                  need_check=True if memo else False,
                                                  instruction_index=index,
                                                  pay_type=address_type)
                        transfers.append(transfer)

        return transfers

    @classmethod
    def _sync_tx_for_address(cls, address, owner, address_type):
        logger.info('sol _sync_tx_for_address begin')
        # 初始设置
        all_transfer_in_transactions = []
        before_signature = None

        tran: SolTransaction = SolTransaction.objects.filter(to_address=owner).order_by('-lt').first()
        until = tran.hash if tran else None
        print('until', until)
        # 每次获取100条记录
        while True:
            tx_history = cls.get_transaction_history(address, before_signature, limit=10, until=until)
            if not tx_history:
                break

            for tx in tx_history:
                logger.info(f"signature:{tx['signature']}")
                details = cls.get_transaction_details(signature=tx['signature'], address=address, owner=owner, address_type=address_type)
                if details and len(details):
                    all_transfer_in_transactions.extend(details)
            # 打印获取到的转入记录
            # for tx in all_transfer_in_transactions:
            #     print(f"Signature: {tx.signature}, Slot: {tx.slot}")

            # 准备下一次获取
            before_signature = tx_history[-1]["signature"]
            logger.info(f'_sync_tx_for_address:{before_signature}')

        # 打印所有转入记录
        with transaction.atomic():
            all_transfer_in_transactions.reverse()
            for tx in all_transfer_in_transactions:
                tx.save()

        logger.info('sol _sync_tx_for_address end')

    @classmethod
    def sync_sol_transaction(cls):
        receipt = AppConfig.value_for_key(AppConfig.PRIMARY_ACCEPT_ADDRESS)
        if not receipt:
            return
        receipts = receipt.split(',')
        for receipt in receipts:
            arr = receipt.split(':')
            if len(arr) == 3:
                SolService._sync_tx_for_address(address=arr[0], owner=arr[1], address_type=arr[2])
