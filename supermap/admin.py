import logging
import os
import hashlib
import json

from django.contrib import admin
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponse
import csv
from django.contrib import messages


# Register your models here.
from django.urls import path

from .models import Config
from .models import SolTransaction
from .models import UserInviteRecord
from .models.user import User as CustomUser
from .models import CheckInPoint
from .models import UserCheckRecord
from .models import Image
from .models import SpotLevelConfig
from .models import SpotCategory
from .models import Banner
from .models import UserTransferRecord
from .models import SpotBoostConfig, SpotBoost
from .models import Product
from .models import ProductTagConfig

from supermap.models.user_asset import UserAsset
from supermap.models.user_asset_detail import UserAssetDetail
from supermap.models.product_order import ProductOrder
from supermap.models.verification_code_order import VerificationCodeOrder

from .models import UserWithdrawOrder
from .service.user_service import UserService

from .service.spot import SpotService
from import_export.admin import ExportActionMixin
from django.shortcuts import render, redirect
from django import forms
import boto3
from mimetypes import guess_type
from .models import OTA
from .models import ShopAdminEventConfig, PaymentOrder, AddressCheckpoint
from .models import ProductImage, CheckInPointImage
from .forms import SimpleExcelUploadForm
from .service.simple_excel_service import SimpleExcelService

from .models.check_in_member_config import CheckInMemberConfig
from .models.check_in_comment import CheckInComment
from .models.checkin_member_order import CheckInMemberOrder
from .models.check_in_member import CheckInMember
from .models.check_in_image import CheckInImage
from .models.check_in import CheckIn

@admin.register(OTA)
class OTAAdmin(admin.ModelAdmin):
    list_filter = ['platform', 'force_update', 'is_active']
    list_display = ('id', 'version', 'platform', 'force_update', 'download_url', 'file_size', 'is_active', 'created_at')
    search_fields = ('version',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('基本信息', {
            'fields': ('version', 'platform', 'force_update', 'is_active')
        }),
        ('更新内容', {
            'fields': ('release_notes',)
        }),
        ('下载信息', {
            'fields': ('download_url', 'file_size', 'md5', 'min_version')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_filter = ['id', '_key', '_value']
    list_display = ('id', '_key', '_value', 'created_at', 'updated_at')


class UserTaskRecordAdmin(admin.ModelAdmin):
    # list_filter = ['id', 'user_id', 'task_id',]
    list_display = ('id', 'user_id', 'task_id', 'rewards', 'day', 'created_at', 'updated_at')

    search_fields = ('user_id', 'task_id')


class UserAdmin(admin.ModelAdmin):
    # list_filter = ['user_id', 'nickname', 'first_name']
    list_display = ('id', 'user_id', 'nickname',  'invite_code', 'created_at')

    search_fields = ('user_id', 'nickname')

    actions = ['new_user']

    def new_user(self, request, object_id, form_url='', extra_context=None):
        UserService.add_new_user()


class UserInviteRecordAdmin(ExportActionMixin, admin.ModelAdmin):
    # list_filter = ['id', 'inviter_id', 'invitee_id']
    list_display = ('id', 'inviter_id', 'invitee_id', 'inviter_name', 'invitee_name', 'day', 'rewards', 'created_at')
    actions = ['export_as_csv']
    search_fields = ('inviter_id', 'invitee_id')

    def inviter_name(self, obj):
        try:
            inviter = CustomUser.objects.get(user_id=obj.inviter_id)
            return inviter.nickname
        except CustomUser.DoesNotExist:
            return None
    inviter_name.short_description = '邀请人用户名'

    def invitee_name(self, obj):
        try:
            invitee = CustomUser.objects.get(user_id=obj.invitee_id)
            return invitee.nickname
        except CustomUser.DoesNotExist:
            return None
    invitee_name.short_description = '被邀请人用户名'

    def export_as_csv(self, request, queryset=None):
        # 创建 HTTP 响应对象
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user_invite_records.csv"'

        writer = csv.writer(response)
        # 写入 CSV 表头
        writer.writerow(['Inviter ID', 'Inviter Name', 'Invitee ID', 'Invitee Name', '邀请时间'])

        for record in queryset:
            inviter_name = self.inviter_name(record)
            invitee_name = self.invitee_name(record)
            writer.writerow([record.inviter_id, inviter_name, record.invitee_id, invitee_name, record.created_at])

        return response
    export_as_csv.short_description = "导出为 CSV"


class UserCheckRecordAdmin(admin.ModelAdmin):
    # list_filter = ['point_id', 'user_id']
    list_display = ('id', 'user_id', 'day', 'created_at', 'updated_at')

    search_fields = ('point_id', 'user_id')


class FileUploadForm(forms.Form):
    file = forms.FileField(required=False)


# @admin.register(Image)
# class ImageAdmin(admin.ModelAdmin):
#     list_filter = ['category', 'remark']
#     list_display = ('id', 'category', 'remark', 'url', 'upload_image_link', 'keep_source_name')

#     # actions = ['upload_image']
#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('<int:image_id>/upload/', self.admin_site.admin_view(self.upload_image), name='image_upload'),
#         ]
#         return custom_urls + urls

#     def upload_image(self, request, image_id):
#         image_instance: Image = get_object_or_404(Image, pk=image_id)
#         if request.method == 'POST':
#             form = FileUploadForm(request.POST, request.FILES)
#             if form.is_valid():
#                 if 'file' in request.FILES:
#                     file = request.FILES['file']
#                     s3_client = boto3.client(
#                         's3',
#                         aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
#                         aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
#                         region_name=os.getenv('AWS_S3_REGION_NAME')
#                     )
#                     image_name = image_instance.category+'/'+file.name
#                     if not image_instance.keep_source_name:
#                         image_name_arr = file.name.split('.')
#                         final_name = file.name
#                         if len(image_name_arr) > 1:
#                             image_name_origin = image_name_arr[0]
#                             image_ext = image_name_arr[1]
#                             final_name = get_md5_hash(image_name_origin) + '.' + image_ext

#                         image_name = image_instance.category + "/" + datetime.now().strftime("%Y%m%d%H%M%S") + "_" + final_name
#                     content_type, _ = guess_type(image_name)
#                     if not content_type:
#                         content_type = 'application/octet-stream'
#                     s3_client.upload_fileobj(
#                         file,
#                         os.getenv('AWS_STORAGE_BUCKET_NAME'),
#                         image_name,
#                         ExtraArgs={'ContentType': content_type}
#                     )
#                     image_url = f"{os.getenv('AWS_S3_CUSTOM_DOMAIN')}/{image_name}"
#                     image_instance.url = image_url

#                 # 保存表单数据
#                 image_instance.save()
#                 return redirect('admin:supermap_image_changelist')
#         else:
#             form = FileUploadForm()

#         context = self.admin_site.each_context(request)
#         context['form'] = form
#         context['image_instance'] = image_instance
#         return render(request, 'admin/upload_image.html', context)

#     def upload_image_link(self, obj):
#         return format_html('<a href="{}">Upload Image</a>', reverse('admin:image_upload', args=[obj.id]))

#     upload_image_link.short_description = 'Upload Image'

def get_md5_hash(input_str):
    """
    生成字符串的MD5哈希值

    参数:
    input_str (str): 要进行MD5哈希的输入字符串

    返回:
    str: 字符串的MD5哈希值
    """
    md5_hash = hashlib.md5()
    md5_hash.update(input_str.encode('utf-8'))
    return md5_hash.hexdigest()


# @admin.register(SolTransaction)
# class SolTransactionAdmin(admin.ModelAdmin):
#     list_filter = ['status', 'pay_type']
#     list_display = ('id', 'pay_checked', 'from_address',  'to_address', 'lt', 'status', 'amount', 'timestamp', 'currency', 'comment', 'pay_type', 'hash', 'created_at')

#     search_fields = ('from_address', 'to_address', 'comment')

@admin.register(CheckInPoint)
class CheckInPointAdmin(admin.ModelAdmin):
    list_filter = ('is_active', 'audit_status', 'category', 'city', 'owner_id')
    list_display = ('id', 'title', 'title_en', 'title_cn', 'category', 'currency', 'country', 'region', 'city', 'location', 'latitude', 'longitude',
    'landmark_image', 'city', 'location', 'owner_name', 'audit_status_display', 'external_url', 'telegram_url', 'believe_url', 'believe_id', 'pcn_url', 'whatsapp_url', 'wechat',
    'description', 'description_en', 'description_cn', 'like_count', 'comment_count', 'is_active_display', 'created_at', 'room_data_action', 'product_list_action')
    search_fields = ('title', 'location', 'city', 'owner_id')
    readonly_fields = ('created_at', 'updated_at')


    def product_list_action(self, obj):
        return format_html(
            '<a class="button default" style="text-decoration: none;" href="{}">查看房型</a>',
            f'/admin/supermap/product/?check_in_point_id={obj.id}'
        )
    product_list_action.short_description = '房型列表'

    def changelist_view(self, request, extra_context=None):
        """重写changelist视图，添加上传Excel按钮"""
        extra_context = extra_context or {}
        extra_context['show_excel_upload'] = True
        extra_context['excel_upload_url'] = reverse('admin:excel-upload')
        return super().changelist_view(request, extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('room-data/<int:point_id>/', self.admin_site.admin_view(self.room_data_view), name='room-data'),
            path('room-data-preview/<int:point_id>/', self.admin_site.admin_view(self.room_data_preview), name='room-data-preview'),
            path('room-data-save/<int:point_id>/', self.admin_site.admin_view(self.room_data_save), name='room-data-save'),
            path('excel-upload/', self.admin_site.admin_view(self.excel_upload_view), name='excel-upload'),
        ]
        return custom_urls + urls

    def room_data_action(self, obj):
        return format_html(
            '<a class="button default" style="text-decoration: none;" href="{}">提交房型数据</a>',
            reverse('admin:room-data', args=[obj.id])
        )
    room_data_action.short_description = '房型数据'

    def room_data_view(self, request, point_id):
        point = get_object_or_404(CheckInPoint, id=point_id)
        if request.method == 'POST':
            room_data = request.POST.get('room_data')
            try:
                # 验证 JSON 数据
                json_data = json.loads(room_data)
                # 保存到 session 用于预览
                request.session['room_data_preview'] = room_data
                return redirect('admin:room-data-preview', point_id=point_id)
            except json.JSONDecodeError:
                messages.error(request, '无效的 JSON 数据')
        
        context = {
            'title': '提交房型数据',
            'point': point,
            'opts': self.model._meta,
        }
        return render(request, 'admin/room_data_form.html', context)

    def room_data_preview(self, request, point_id):
        point = get_object_or_404(CheckInPoint, id=point_id)
        room_data = request.session.get('room_data_preview')
        if not room_data:
            messages.error(request, '没有找到房型数据')
            return redirect('admin:room-data', point_id=point_id)
        
        result = SpotService.process_room_data(room_data)
        if not result['success']:
            messages.error(request, result['message'])
            return redirect('admin:room-data', point_id=point_id)
        
        context = {
            'title': '房型数据预览',
            'point': point,
            'room_list': result['room_list'],
            'opts': self.model._meta,
        }
        return render(request, 'admin/room_data_preview.html', context)

    def room_data_save(self, request, point_id):
        point = get_object_or_404(CheckInPoint, id=point_id)
        room_data = request.session.get('room_data_preview')
        if not room_data:
            messages.error(request, '没有找到房型数据')
            return redirect('admin:room-data', point_id=point_id)
        
        result = SpotService.save_room_data(point_id, room_data)
        if result['success']:
            messages.success(request, result['message'])
            # 清除 session 中的预览数据
            request.session.pop('room_data_preview', None)
            return redirect('admin:supermap_checkinpoint_changelist')
        else:
            messages.error(request, result['message'])
            return redirect('admin:room-data', point_id=point_id)

    def excel_upload_view(self, request):
        """Excel文件上传视图 - 导入数据并处理图片"""
        upload_result = None
        
        if request.method == 'POST':
            form = SimpleExcelUploadForm(request.POST, request.FILES)
            if form.is_valid():
                excel_file = form.cleaned_data['excel_file']
                
                # 保存临时文件
                import tempfile
                import os
                import base64
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
                    for chunk in excel_file.chunks():
                        temp_file.write(chunk)
                    temp_file_path = temp_file.name
                
                try:
                    # 检查是否是预览模式还是导入模式
                    if '_preview' in request.POST:
                        # 预览模式：预览Excel数据
                        result = SimpleExcelService.preview_excel_data(temp_file_path)
                        
                        if result['success']:
                            # 为每个图片添加base64编码用于显示
                            for row_data in result['preview_data']:
                                for image in row_data['images']:
                                    # 检查是否有base64_preview，如果没有则生成
                                    if 'base64_preview' in image and image['base64_preview']:
                                        image['base64'] = image['base64_preview']
                                    else:
                                        # 如果没有base64_preview，尝试从data生成
                                        if 'data' in image and image['data']:
                                            image['base64'] = base64.b64encode(image['data']).decode('utf-8')
                                        else:
                                            image['base64'] = None
                            
                            messages.success(request, result['message'])
                        else:
                            messages.error(request, result['message'])
                        
                        upload_result = result
                    else:
                        # 导入模式：导入数据并处理图片
                        result = SimpleExcelService.import_excel_data(temp_file_path)
                        
                        if result['success']:
                            messages.success(request, result['message'])
                        else:
                            messages.error(request, result['message'])
                        
                        upload_result = result
                        
                except Exception as e:
                    messages.error(request, f'处理Excel文件时发生错误: {str(e)}')
                    upload_result = {
                        'success': False,
                        'message': f'处理失败: {str(e)}'
                    }
                finally:
                    # 清理临时文件
                    try:
                        os.unlink(temp_file_path)
                    except:
                        pass
        else:
            form = SimpleExcelUploadForm()
        
        context = {
            'title': 'Excel数据导入',
            'form': form,
            'upload_result': upload_result,
            'opts': self.model._meta,
        }
        return render(request, 'admin/simple_excel_upload.html', context)

    class IsActiveFilter(admin.SimpleListFilter):
        title = '状态'
        parameter_name = 'is_active'

        def lookups(self, request, model_admin):
            return (
                ('1', '已激活'),
                ('0', '未激活'),
            )

        def queryset(self, request, queryset):
            if self.value() == '1':
                return queryset.filter(is_active=True)
            if self.value() == '0':
                return queryset.filter(is_active=False)
            return queryset

        def expected_parameters(self):
            return [self.parameter_name]

    class AuditStatusFilter(admin.SimpleListFilter):
        title = '审核状态'
        parameter_name = 'audit_status'

        def lookups(self, request, model_admin):
            return (
                ('0', '待审核'),
                ('1', '已通过'),
                ('2', '已拒绝'),
            )

        def queryset(self, request, queryset):
            if self.value():
                return queryset.filter(audit_status=self.value())
            return queryset

        def expected_parameters(self):
            return [self.parameter_name]
    
    def owner_name(self, obj):
        try:
            user = CustomUser.objects.get(user_id=obj.owner_id)
            return user.nickname
        except CustomUser.DoesNotExist:
            return f"未知用户({obj.owner_id})"
    owner_name.short_description = '所有者'

    def audit_status_display(self, obj):
        status_map = {
            0: '待审核',
            1: '已通过',
            2: '已拒绝'
        }
        return status_map.get(obj.audit_status, '未知状态')
    audit_status_display.short_description = '审核状态'

    def is_active_display(self, obj):
        return '已激活' if obj.is_active else '未激活'
    is_active_display.short_description = '状态'

    def get_list_display_links(self, request, list_display):
        return ('id', 'title')

    def get_list_filter(self, request):
        return [
            self.IsActiveFilter,
            self.AuditStatusFilter,
            'category',
            'city',
            'owner_id'
        ]
    
    fieldsets = (
        ('基本信息', {
            'fields': (
                'title',
                'title_en',
                'title_cn',
                'category',
                'city',
                'location',
                'owner_id',
                'is_active',
                'currency',
                'country',
                'region',
                'landmark_image',
                'external_url',
                'telegram_url',
                'believe_id',
                'pcn_url',
                'whatsapp_url',
                'wechat',
                'description',
                'description_en',
                'description_cn',
                'like_count',
                'comment_count',
            ),
            'classes': ('wide',)
        }),
        ('审核信息', {
            'fields': (
                'audit_status',
                'believe_url',
            ),
            'classes': ('wide',)
        }),
        ('位置信息', {
            'fields': (
                'latitude',
                'longitude',
            ),
            'classes': ('wide',)
        }),
        ('时间信息', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
    ordering = ('-created_at',)

#
# @admin.register(SpotLevelConfig)
# class SpotLevelConfigAdmin(admin.ModelAdmin):
#     list_filter = ['id', 'level', 'currency', 'amount']
#     list_display = ('id', 'level', 'currency', 'amount', 'value', 'check_in_distance', 'check_in_commission')
#
#
# @admin.register(SpotCategory)
# class SpotCategoryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'type', 'label', 'label_zh', 'label_zh_tw', 'image_url', 'display', 'sort_index')
#
#
# @admin.register(Banner)
# class BannerAdmin(admin.ModelAdmin):
#     list_display = ('id', 'image_url', 'link_type', 'link_url', 'show_start_at', 'show_end_at', 'created_at', 'activity_short_id')
#
#
# @admin.register(UserTransferRecord)
# class UserTransferRecordAdmin(admin.ModelAdmin):
#     list_filter = ['id', 'sender_id', 'sender_name', 'receive_id', 'receive_name']
#     list_display = ('id', 'sender_id', 'sender_name', 'receive_id', 'receive_name', 'amount', 'fee', 'created_at')
#
#
# @admin.register(SpotBoostConfig)
# class SpotBoostConfigAdmin(admin.ModelAdmin):
#     list_filter = ['id', 'match_type', 'ratio']
#     list_display = ('id', 'match_type', 'spots', 'start_time', 'end_time', 'ratio', 'remark')
#
#     actions = ['generate_or_update']
#
#     def generate_or_update(self, request, object_id, form_url='', extra_context=None):
#         SpotService.generate_or_update_boost(object_id)
#
# @admin.register(SpotBoost)
# class SpotBoostAdmin(admin.ModelAdmin):
#     list_filter = ['boost', 'ratio']
#     list_display = ('id', 'boost', 'ratio', 'start_time', 'end_time', 'spot_id')
#
#     search_fields = ('ratio', 'spot_id')
#
#
#
# admin.site.register(CustomUser, UserAdmin)
# admin.site.register(UserInviteRecord, UserInviteRecordAdmin)

#
#
# admin.site.register(CheckInPoint)
# admin.site.register(UserCheckRecord, UserCheckRecordAdmin)
#
#

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ('category', 'level', 'check_in_point_id')
    list_display = ('id', 'name', 'original_price', 'amount', 'amount_usd', 'amount_currency', 'level', 'level_tag', 'category', 'check_in_point_id',  'back_to_checkinpoint',
                    'tags', 'visited_count', 'comment_count', 'favorite_count', 'is_active', 'audit_status', 'created_at')
    search_fields = ('name', 'description', 'check_in_point_id')
    readonly_fields = ('created_at', 'updated_at')


    def back_to_checkinpoint(self, obj):
        return format_html(
            '<a class="button default" style="text-decoration: none;" href="{}">返回地标</a>',
            '/admin/supermap/checkinpoint/'
        )
    back_to_checkinpoint.short_description = '返回地标'
    
    fieldsets = (
        ('基本信息', {
            'fields': (
                'name',
                'original_price',
                'amount',
                'amount_usd',
                'amount_currency',
                'description',
                'check_code_num',
                'level',
                'level_tag',
                'category',
                'check_in_point_id',
                'image',
                'tags',
                'audit_status',
                'is_active'
            ),
            'classes': ('wide',)
        }),
        ('时间信息', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
    ordering = ('-created_at',)


@admin.register(ShopAdminEventConfig)
class ShopAdminEventConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'contract', 'event_name', 'signature', 'memo', 'is_active', 'scan_speed', 'create_block', 'scan_block', 'created_time', 'updated_time')
    search_fields = ('contract', 'event_name', 'signature', 'memo')
    list_filter = ('is_active',)
    readonly_fields = ('created_time', 'updated_time')
    fieldsets = (
        ('基本信息', {
            'fields': ('contract', 'event_name', 'signature', 'memo', 'is_active')
        }),
        ('区块信息', {
            'fields': ('scan_speed', 'create_block', 'scan_block')
        }),
        ('时间信息', {
            'fields': ('created_time', 'updated_time')
        }),
    )

@admin.register(PaymentOrder)
class PaymentOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'chain', 'currency', 'amount', 'status', 'from_address', 'to_address', 'created_at', 'paid_at', 'expired_at', 'is_callback')
    search_fields = ('order_id', 'from_address', 'to_address', 'tx_hash', 'pay_order_id')
    list_filter = ('status', 'chain', 'currency', 'is_callback')
    readonly_fields = ('created_at', 'paid_at', 'expired_at')
    fieldsets = (
        ('基本信息', {
            'fields': ('order_id', 'chain', 'currency', 'amount', 'status', 'from_address', 'to_address', 'block_number', 'is_callback')
        }),
        ('交易信息', {
            'fields': ('tx_hash', 'tx_data', 'pay_order_id')
        }),
        ('描述与元数据', {
            'fields': ('description', 'metadata')
        }),
        ('时间信息', {
            'fields': ('created_at', 'paid_at', 'expired_at')
        }),
    )

@admin.register(AddressCheckpoint)
class AddressCheckpointAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'chain', 'currency', 'last_check_block', 'last_check_time', 'is_active', 'error_count', 'contract_address', 'token_decimals')
    search_fields = ('address', 'chain', 'currency', 'contract_address')
    list_filter = ('is_active', 'chain', 'currency')
    readonly_fields = ('last_check_time',)
    fieldsets = (
        ('基本信息', {
            'fields': ('address', 'chain', 'currency', 'is_active', 'contract_address', 'token_decimals')
        }),
        ('检查信息', {
            'fields': ('last_check_block', 'last_check_time', 'error_count', 'last_error')
        }),
        ('描述与元数据', {
            'fields': ('description', 'metadata')
        }),
    )


@admin.register(ProductTagConfig)
class ProductTagConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag_cn', 'tag_en', 'sort_index', 'mark')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_id', 'image_url', 'sort_index', 'status', 'image_type', 'created_at', 'updated_at')


@admin.register(CheckInPointImage)
class CheckInPointImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'check_in_point', 'image_url', 'sort_index', 'status', 'created_at', 'updated_at')


@admin.register(UserAsset)
class UserAssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'currency', 'balance', 'created_at', 'updated_at')


@admin.register(UserAssetDetail)
class UserAssetDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'currency', 'rewards', 'invitee_id', 'related_id', 'created_at', 'updated_at')


@admin.register(ProductOrder)
class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'spot_id', 'ue_order_id', 'user_id', 'seller_id', 'product_id', 'product_name', 'product_num',
                    'amount', 'product_price', 'pay_type', 'unit', 'status', 'refund_status', 'is_commented', 'is_deleted', 'deleted_at',
                    'cancel_reason', 'cancel_by_buyer', 'cancel_at', 'contact_name', 'contact_phone', 'contact_address', 'created_at', 'updated_at')


@admin.register(VerificationCodeOrder)
class VerificationCodeOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'user_id', 'product_id', 'product_name', 'code_num', 'product_num', 'amount', 'product_price',
                    'pay_type', 'unit', 'status', 'created_at', 'updated_at')

@admin.register(CheckInMemberConfig)
class CheckInMemberConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'period', 'fec_price', 'fec_origin_price', 'usdt_price', 'usdt_origin_price', 'description', 'sort_index', 'created_at', 'updated_at')


@admin.register(CheckInComment)
class CheckInCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'check_in_id', 'parent_id', 'reply_to_id', 'reply_to_user_id', 'user_id', 'content', 'status', 'city', 'like_count', 'created_at', 'updated_at')


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ('id', 'check_in_point', 'user_id', 'content', 'status', 'private', 'comment_count', 'like_count', 'visit_count', 'created_at', 'updated_at')


@admin.register(CheckInMemberOrder)
class CheckInMemberOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'user_id', 'ue_order_id', 'period', 'amount', 'product_price', 'pay_type', 'unit', 'status', 'created_at', 'updated_at')


@admin.register(CheckInMember)
class CheckInMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'expired_timestamp', 'created_at', 'updated_at')


@admin.register(CheckInImage)
class CheckInImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'check_in_id', 'image_url', 'sort_index', 'status', 'created_at', 'updated_at')