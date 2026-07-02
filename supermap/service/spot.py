import logging
from supermap.models.check_in_point import CheckInPoint
from supermap.models.spot_boost import SpotBoost
from supermap.models.spot_boost_config import SpotBoostConfig
from datetime import datetime, timedelta
import json
from django.contrib import messages
from django.shortcuts import get_object_or_404
from ..models import Product, ProductImage

logger = logging.getLogger(__name__)


class SpotService(object):


    @classmethod
    def update_boost(cls):
        configs = SpotBoostConfig.objects.all()
        cls.generate_or_update_boost(configs)

    @classmethod
    def generate_or_update_boost(cls, configs: [SpotBoostConfig]):
        now = datetime.now()
        for config in configs:
            config: SpotBoostConfig = config
            boosts = SpotBoost.objects.filter(boost=config).all()
            boost_dic = {}
            for boost in boosts:
                boost_dic[boost.spot_id.id] = boost
            # spots = []
            if config.match_type == 'all':
                spots = CheckInPoint.objects.filter(start_time__lte=now, end_time__gt=now).all()
            else:
                return
            for spot in spots:
                boost: SpotBoost = boost_dic.get(spot.id)
                if not boost:
                    boost = SpotBoost()
                    boost.boost = config
                boost.start_time = config.start_time
                boost.end_time = config.end_time
                boost.ratio = config.ratio
                boost.spot_id = spot
                boost.save()

    @staticmethod
    def process_room_data(room_data: str) -> dict:
        """
        处理房型数据，提取有效信息
        """
        try:
            data = json.loads(room_data)
            room_list = []
            
            # 获取物理房型信息
            physic_room_map = data.get('data', {}).get('physicRoomMap', {})
            # 获取销售房型信息
            sale_room_map = data.get('data', {}).get('saleRoomMap', {})
            
            # 遍历物理房型
            for room_id, room_info in physic_room_map.items():
                room_name = room_info.get('name', '')
                # 获取房型图片
                picture_info = room_info.get('pictureInfo', [])
                image_urls = [img.get('smallPicUrl', '') for img in picture_info if img.get('smallPicUrl')]
                
                # 查找对应的销售房型
                for sale_room in sale_room_map.values():
                    if str(sale_room.get('physicalRoomId')) == str(room_id):
                        price_info = sale_room.get('priceInfo', {})
                        meal_info = sale_room.get('mealInfo', {})
                        cancel_info = sale_room.get('cancelInfo', {})
                        confirm_info = sale_room.get('confirmInfo', {})
                        
                        # 准备房型数据
                        room_data = {
                            'name': room_name,
                            'price': price_info.get('displayPrice', ''),
                            'breakfast': meal_info.get('title', ''),
                            'cancel_policy': cancel_info.get('title', ''),
                            'confirm_time': confirm_info.get('title', ''),
                            'room_code': sale_room.get('roomCode', ''),
                            'is_booking': sale_room.get('bookingStatusInfo', {}).get('isBooking', False),
                            'remain_quantity': sale_room.get('bookingStatusInfo', {}).get('remainRoomQuantity', 0),
                            'images': image_urls,
                        }
                        room_list.append(room_data)
            
            return {
                'success': True,
                'room_list': room_list,
                'message': f'找到 {len(room_list)} 个房型'
            }
        except json.JSONDecodeError:
            return {
                'success': False,
                'message': '无效的 JSON 数据'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'处理数据时出错: {str(e)}'
            }

    @staticmethod
    def save_room_data(point_id: int, room_data: str) -> dict:
        """
        保存房型数据到数据库
        """
        try:
            data = json.loads(room_data)
            saved_count = 0
            
            # 获取物理房型信息
            physic_room_map = data.get('data', {}).get('physicRoomMap', {})
            # 获取销售房型信息
            sale_room_map = data.get('data', {}).get('saleRoomMap', {})
            
            # 遍历物理房型
            for room_id, room_info in physic_room_map.items():
                room_name = room_info.get('name', '')
                # 获取房型图片
                picture_info = room_info.get('pictureInfo', [])
                image_data = [
                    {
                        'small_url': img.get('smallPicUrl', ''),
                        'big_url': img.get('bigPicUrl', ''),
                        'original_url': img.get('url', '')
                    }
                    for img in picture_info 
                    if img.get('url')
                ]
                
                # 获取第一张小图作为封面图
                cover_image = image_data[0]['small_url'] if image_data else ''
                
                # 查找对应的销售房型
                for sale_room in sale_room_map.values():
                    if str(sale_room.get('physicalRoomId')) == str(room_id):
                        price_info = sale_room.get('priceInfo', {})
                        meal_info = sale_room.get('mealInfo', {})
                        cancel_info = sale_room.get('cancelInfo', {})
                        confirm_info = sale_room.get('confirmInfo', {})
                        
                        try:
                            # 转换价格为浮点数
                            price = float(price_info.get('displayPrice', '0').replace('¥', '').replace(',', ''))
                            
                            # 创建或更新 Product
                            product, created = Product.objects.update_or_create(
                                check_in_point_id=point_id,
                                name=room_name,
                                defaults={
                                    'original_price': price,
                                    'amount': price,
                                    'description': f"早餐: {meal_info.get('title', '')}\n取消政策: {cancel_info.get('title', '')}\n确认时间: {confirm_info.get('title', '')}",
                                    'level': 0,
                                    'level_tag': '',
                                    'category': 'unofficial',
                                    'amount_currency': 'CNY',
                                    'image': cover_image,  # 设置封面图，
                                    'audit_status': 1
                                }
                            )
                            
                            # 保存图片
                            if image_data:
                                # 删除旧的图片记录
                                ProductImage.objects.filter(product_id=product.id).delete()
                                # 创建新的图片记录
                                for index, img_data in enumerate(image_data):
                                    # 保存小图
                                    ProductImage.objects.create(
                                        product_id=product.id,
                                        image_url=img_data['small_url'],
                                        image_type='small',
                                        sort_index=index,
                                        status=1
                                    )
                                    # 保存大图
                                    ProductImage.objects.create(
                                        product_id=product.id,
                                        image_url=img_data['big_url'],
                                        image_type='large',
                                        sort_index=index,
                                        status=1
                                    )
                            
                            saved_count += 1
                        except Exception as e:
                            return {
                                'success': False,
                                'message': f'保存房型 {room_name} 时出错: {str(e)}'
                            }
            
            return {
                'success': True,
                'message': f'成功保存 {saved_count} 个房型数据'
            }
            
        except json.JSONDecodeError:
            return {
                'success': False,
                'message': '无效的 JSON 数据'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'处理数据时出错: {str(e)}'
            }
