import asyncio
from supermap.service.ton_service import TonService


# asyncio.run(TonService.getAccount("UQCcarxDrNPRi_pYid3enFo4Vz1DtgwR8UcmblENLvBguV8x"))
# asyncio.run(TonService.getTransactions("UQD9FDq0ZbiOoRf-bIiJo6MZaFCMvgtZN0h4e_zRnMyFTT9_"))


from asgiref.sync import sync_to_async

# asyncio.run(TonService.sync_in_transaction()) /

from supermap.service.report import ReportService
# ReportService.daily_report()
from supermap.service.user_service import UserService

# UserService.check_spot_pay()
# UserService.check_out_of_date_spot_order()
from supermap.models.user import User
from datetime import datetime, timedelta
# u: User = User.objects.first()
# u.primary_end_at = u.primary_end_at + timedelta(days=30)
# print(u.primary_end_at)
# u.nickname = '123123'
# u.save()
# print(u.primary_end_at)
# TonService.sync_in_transaction()
from scheduler.scheduler.ton import TonTask
# TonTask.sync_payment_tx()
from scheduler.scheduler.user import UserTask
# UserTask.update_primary()


# from heyos.service import bot
# bot.main()

import os
from huaweicloudsdkcore.auth.credentials import Credentials
# from huaweicloudsdkcore.exceptions import ClientRequestException
from huaweicloudsdkobs.v1 import ObsClient, PutObjectRequest



ak = os.getenv('HUAWEICLOUD_ACCESS_KEY')
sk = os.getenv('HUAWEICLOUD_SECRET_KEY')
region = os.getenv('HUAWEICLOUD_REGION')
bucket_name = 'heyo/test'  # 替换为你的OBS桶名称
object_name = 'meme1.jpg'  # 替换为你希望在OBS中存储的文件名
file_name = '/Users/pengkang/Desktop/meme.jpg'  # 替换为你本地文件的路径

#
# credentials = Credentials(ak, sk)
# obs_client = ObsClient.new_builder().with_credentials(credentials).build()
#
# try:
#     with open(file_name, 'rb') as file:
#         response = obs_client.put_object(
#             bucket_name=bucket_name,
#             object_key=object_name,
#             body=file
#         )
#         print("Upload Successful")
# except Exception as e:
#     print(f"Failed to upload file: {e}")
#
# # 获取CDN链接
# cdn_domain = 'your_cdn_domain'  # 替换为你的CDN域名
# cdn_url = f'https://{cdn_domain}/{object_name}'
#
# # 输出CDN链接
# print(f"CDN URL: {cdn_url}")


import requests

from supermap.service.ton_service_v2 import TonServiceV2
asyncio.run(TonServiceV2.sync_in_transaction())
