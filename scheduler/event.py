import json
import os
import time

from django.conf import settings
import requests
from scheduler.eth import ETHService
from django.db import transaction
import logging
from supermap.models.shop_admin_eventconfig import ShopAdminEventConfig 
from supermap.models.verification_code_order import VerificationCodeOrder
from supermap.models.payment_order import PaymentOrder
from supermap.models.product_order import ProductOrder
from supermap.models.checkin_member_order import CheckInMemberOrder
from supermap.models.check_in_member import CheckInMember
from supermap.models.product import Product
from supermap.models.user import User
from supermap.models.verification_code import VerificationCode
from django.utils import timezone
from datetime import datetime
from scheduler.utils import send_lark_message, utils
logger = logging.getLogger(__name__)

ADDRESS_ZERO = '0x0000000000000000000000000000000000000000'

# rpcUrl = "https://1rpc.io/sepolia"
# rpcUrl = "http://51.210.222.104:8545"

rpcUrl = os.getenv('BACKEND_ETH1_RPC') or ''

# 常量定义
TOKEN_DECIMALS = 6  # USDO精度
AMOUNT_TOLERANCE = 0.001  # 金额匹配容差
VERIFICATION_CODE_LENGTH = 13  # 核销码长度
BATCH_SIZE = 100  # 批量插入大小

class EventTask(object):

    @classmethod
    def scan_low_events(cls):
        events = ShopAdminEventConfig.objects.filter(is_active=True)
        for event in events:
            logger.info(f'scan_events transfer {event.memo}')
            try:
                cls._scan_event(event)
            except Exception as e:
                logger.error(f'err: scan_events {event.memo} {str(e)}')

    @classmethod
    def _scan_event(cls, event: ShopAdminEventConfig):
        last_block = max(event.scan_block + 1, event.create_block)
        latest_block = int(ETHService.latest_block()) - 1
        batch = 10000
        for current_block in range(last_block, latest_block, batch):
            toBlock = latest_block if current_block + batch >= latest_block else current_block + batch
            payload = {
                "id": 1,
                "jsonrpc": "2.0",
                "method": "eth_getLogs",
                "params": [{
                    "address": event.contract,
                    "topics": [event.signature],
                    "fromBlock": hex(current_block),
                    "toBlock": hex(toBlock)
                }
                ]
            }
            headers = {'content-type': 'application/json'}
            resp = requests.post(rpcUrl, data=json.dumps(payload), headers=headers).json()
            print('resp', resp)
            if 'result' not in resp:
                logger.error(f"error:{resp}")
                break
            logs = resp['result']
            try:
                with transaction.atomic():
                    success = cls._process_event_logs(event, logs)
                    print('to block', toBlock)
                    if success:
                        event.scan_block = toBlock
                        event.save()
                    else:
                        logger.error(f"[WARN] Process logs failed for {current_block} ~ {toBlock}")
                        break
            except Exception as e:
                logger.error(f"[ERROR] Exception in processing or saving: {e}")
                break

    @classmethod
    def _process_event_logs(cls, event: ShopAdminEventConfig, logs: list) -> bool:
    
        method = "_scan_usdo_transfer"
        return cls._scan_usdo_transfer(event, logs)
        # logging.info('_process_event_logs: %s', method)
        # return method(event, logs)

    @classmethod
    def getBlock(cls, blockNumber, txHash):
        block_info = ETHService.get_block_by_number(blockNumber)
        if not block_info or 'result' not in block_info:
            logger.error(f'Failed to get block info for block {blockNumber}')
            return None, False
        return block_info, True
        # 检查交易是否成功
        # tx_status = ETHService.receipt(txHash)
        # if tx_status is None or not tx_status:
        #     logger.warning(f'Transaction failed or pending: {txHash}')
        #     return None, False
        # return block_info, True

    @classmethod
    def _scan_usdo_transfer(cls, event: ShopAdminEventConfig, logs: list) -> bool:
        logger.info('_scan_usdo_transfer begin')
        for log in logs:
            print(log)
            topics = log['topics']
            from_address = '0x' + topics[1][-40:]
            to_address = '0x' + topics[2][-40:]
            amount = cls._extract_amount_from_log_data(log['data'])
            logIndex = int(log['logIndex'], 16)
            txHash = log["transactionHash"]
            block_number = int(log['blockNumber'], 16)
            block_info, valid = cls.getBlock(int(log['blockNumber'], 16), txHash)
            if not valid or not block_info:
                return False
            timestamp = int(block_info['result']['timestamp'], 16)
            
            # 从事件日志的data字段中提取memo
            memo = cls._extract_memo_from_log_data(log['data'])

            logger.info(f'memo: {memo}')
            logger.info(f'amount: {amount}')
            logger.info(f'to_address: {to_address}')

            # 查询是否存在订单
            if memo:
                order: PaymentOrder = PaymentOrder.objects.filter(
                    order_id=memo,
                    to_address__iexact=to_address,
                    status=PaymentOrder.Status.PENDING.value
                ).first()
                if order:
                    logger.info(f'payment order:{order}, order type:{order.biz_type}')
                    if order.biz_type == PaymentOrder.BizType.CODE:
                        # 检查金额匹配
                        actual_amount = amount / (10 ** TOKEN_DECIMALS)
                        order_amount = float(order.amount)

                        # 允许小的精度差异
                        if abs(actual_amount - order_amount) <= AMOUNT_TOLERANCE:
                            order.status = PaymentOrder.Status.PAID.value
                            order.tx_hash = txHash
                            order.from_address = from_address
                            order.block_number = block_number
                            order.paid_at = cls.format_timestamp(timestamp)
                            order.save()

                            # 更新verification_code_order表并处理相关业务逻辑
                            verification_code_order = VerificationCodeOrder.objects.filter(
                                order_id=memo,
                                status=VerificationCodeOrder.Status.Unpaid.value
                            ).first()

                            if verification_code_order:
                                # 更新订单状态
                                verification_code_order.status = VerificationCodeOrder.Status.Paid.value
                                verification_code_order.save()

                                # 处理用户身份升级和核销码生成
                                cls._process_order_completion(verification_code_order)

                            send_lark_message(f"订单 {order.order_id} 已标记为已支付,\n交易hash: {txHash},\nfrom_address: {from_address},\nto_address: {to_address},\namount: {actual_amount}")
                            logger.info(f"订单 {order.order_id} 已标记为已支付")
                        else:
                            send_lark_message(
                                f"订单 {order.order_id} 金额不匹配: {actual_amount} != {order_amount},\n交易hash: {txHash},\nfrom_address: {from_address},\nto_address: {to_address},\namount: {actual_amount}")
                            logger.warning(f"订单 {order.order_id} 金额不匹配: {actual_amount} != {order_amount}")
                    elif order.biz_type == PaymentOrder.BizType.PRODUCT:
                        # 检查金额匹配
                        actual_amount = amount / (10 ** TOKEN_DECIMALS)
                        order_amount = float(order.amount)
                        # 允许小的精度差异
                        if abs(actual_amount - order_amount) <= AMOUNT_TOLERANCE:
                            order.status = PaymentOrder.Status.PAID.value
                            order.tx_hash = txHash
                            order.from_address = from_address
                            order.block_number = block_number
                            order.paid_at = cls.format_timestamp(timestamp)
                            order.save()

                            product_order: ProductOrder = ProductOrder.objects.filter(
                                order_id=memo,
                                status__in=[ProductOrder.Status.PENDING_PAYMENT.value, ProductOrder.Status.PAYMENT_PROCESSING.value]
                            ).first()
                            if product_order:
                                product_order.status = ProductOrder.Status.PENDING_SHIPMENT.value
                                product_order.save()
                        else:
                            send_lark_message(
                                f"订单 {order.order_id} 金额不匹配: {actual_amount} != {order_amount},\n交易hash: {txHash},\nfrom_address: {from_address},\nto_address: {to_address},\namount: {actual_amount}")
                            logger.warning(f"订单 {order.order_id} 金额不匹配: {actual_amount} != {order_amount}")
                    elif order.biz_type == PaymentOrder.BizType.MEMBER:
                        # 检查金额匹配
                        actual_amount = amount / (10 ** TOKEN_DECIMALS)
                        order_amount = float(order.amount)

                        # 允许小的精度差异
                        if abs(actual_amount - order_amount) <= AMOUNT_TOLERANCE:
                            order.status = PaymentOrder.Status.PAID.value
                            order.tx_hash = txHash
                            order.from_address = from_address
                            order.block_number = block_number
                            order.paid_at = cls.format_timestamp(timestamp)
                            order.save()
                            logger.info("-----")
                            # 更新memberorder
                            member_order: CheckInMemberOrder = CheckInMemberOrder.objects.filter(
                                order_id=memo,
                                status__in=[CheckInMemberOrder.Status.UNPAID.value, CheckInMemberOrder.Status.PAYMENT_PROCESSING.value]
                            ).first()
                            if member_order:
                                member_order.status = CheckInMemberOrder.Status.PAID.value
                                member_order.save()
                            else:
                                send_lark_message(
                                    f"订单 {order.order_id} 对应member order 不存在")
                                logger.warning(f"订单 {order.order_id} 对应member order 不存在")
                            timestamp = int(time.time())
                            # 更新会员信息
                            user_id = member_order.user_id
                            member: CheckInMember = CheckInMember.objects.filter(user_id=user_id).first()
                            if not member:
                                member = CheckInMember()
                                member.user_id = user_id
                                member.expired_timestamp = int(member_order.period) * 86400 + timestamp
                            else:
                                if member.expired_timestamp < timestamp:
                                    member.expired_timestamp = int(member_order.period) * 86400 + timestamp
                                else:
                                    member.expired_timestamp += int(member_order.period) * 86400
                            member.save()

                        else:
                            send_lark_message(
                                f"订单 {order.order_id} 金额不匹配: {actual_amount} != {order_amount},\n交易hash: {txHash},\nfrom_address: {from_address},\nto_address: {to_address},\namount: {actual_amount}")
                            logger.warning(f"订单 {order.order_id} 金额不匹配: {actual_amount} != {order_amount}")
                    else:
                        send_lark_message(f"订单 {order.order_id} payment order 不存在:")
                        logger.warning(f"订单 {order.order_id} payment order 不存在:")
                else:
                    send_lark_message(f"没有找到订单ID为 {memo} 的待支付订单,\n交易hash: {txHash},\nfrom_address: {from_address},\nto_address: {to_address},\namount: {amount / (10 ** TOKEN_DECIMALS)}")
                    logger.warning(f"没有找到订单ID为 {memo} 的待支付订单")
            else:
                logger.warning(f"无法从事件数据中提取memo")
        logger.info('_scan_usdo_transfer end')
        return True

    @classmethod
    def _extract_memo_from_log_data(cls, data: str) -> str:
        try:
            data = data[2:] if data.startswith("0x") else data

            # data 中是 event 参数按顺序 ABI 编码展开的，不是offset跳转结构
            # 第一个参数: amount (32 bytes)
            # 第二个参数: offset (无用，可跳过)
            # 第三个参数: memo长度
            # 第四个参数: memo内容（可能含 padding）

            # 提取 memo 长度（第3个字段）
            length_hex = data[128:192]  # 第3个字段
            length = int(length_hex, 16)

            # 提取 memo 原始 hex
            memo_hex = data[192:192 + length * 2]
            memo_bytes = bytes.fromhex(memo_hex)
            memo = memo_bytes.decode('utf-8')
            return memo
        except Exception as e:
            logger.error(f"从日志data中提取memo失败: {str(e)}")
            return None
        
    @classmethod
    def _extract_amount_from_log_data(cls, data: str) -> int:
        """
        从事件日志的 data 字段中提取 amount（第一个参数）
        参数:
            data (str): 事件日志的 data 字段（0x 开头）
        返回:
            int: 以最小单位表示的金额（如 USDO 是 6 位精度）
        """
        try:
            data = data[2:] if data.startswith("0x") else data
            amount_hex = data[0:64]
            amount = int(amount_hex, 16)
            return amount
        except Exception as e:
            logger.error(f"提取 amount 出错: {str(e)}")
            return 0
        
    @classmethod
    def _process_order_completion(cls, verification_code_order: VerificationCodeOrder):
        """
        处理订单完成后的业务逻辑：用户身份升级和核销码生成
        """
        order_id = verification_code_order.order_id
        user_id = verification_code_order.user_id
        product_id = verification_code_order.product_id
        
        logger.info(f"开始处理订单 {order_id} 的完成逻辑")
        
        try:
            # 查询产品信息
            product = Product.objects.filter(id=product_id).first()
            if not product:
                logger.error(f"查询产品信息失败: product_id={product_id}")
                return

            # 查询用户信息
            user = User.objects.filter(user_id=user_id).first()
            if not user:
                logger.error(f"查询用户信息失败: user_id={user_id}")
                return

            # 如果产品等级大于用户当前等级,更新用户身份标签
            if product.level > user.identity_tag:
                old_level = user.identity_tag
                user.identity_tag = product.level
                user.identity_name = product.level_tag
                user.save(update_fields=['identity_tag', 'identity_name'])
                logger.info(f"用户 {user_id} 身份标签已从 {old_level} 更新为 {product.level}")

            # 批量生成核销码
            code_count = verification_code_order.code_num
            if code_count <= 0:
                logger.warning(f"订单 {order_id} 的核销码数量为 {code_count}，跳过生成")
                return
                
            codes = [
                VerificationCode(
                    buy_uid=user_id,
                    order_id=order_id,
                    code=utils.generate_secure_string(VERIFICATION_CODE_LENGTH, True, False, True),
                    status='unused',
                    use_uid=0,
                    use_time=None
                )
                for _ in range(code_count)
            ]

            # 批量插入核销码
            if codes:
                VerificationCode.objects.bulk_create(codes, batch_size=BATCH_SIZE)
                logger.info(f"为订单 {order_id} 成功生成了 {len(codes)} 个核销码")

        except Exception as e:
            error_msg = f"处理订单 {order_id} 完成逻辑时发生错误: {str(e)}"
            logger.error(error_msg)
            send_lark_message(error_msg)

    @classmethod
    def format_timestamp(cls, timestamp: int):
        """
        将区块链时间戳（秒）转换为带时区的datetime对象
        """
        dt = datetime.fromtimestamp(timestamp)
        return timezone.make_aware(dt)
