from django.contrib import admin
from .models import *
from .device import DevCtrl

# Register your models here.
import logging
logger = logging.getLogger('WEB')

admin.site.site_header = '仓储导航控制台'
admin.site.site_title = '仓储导航控制台'
admin.site.index_title = '欢迎使用仓储导航系统'
admin.site.site_icon = '/static/icon/favicon.ico'

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'rfid', 'price', 'quantity', 'location', 'status', 'add_time', 'operator')
    search_fields = ('name', 'rfid')
    ordering = ('-add_time', 'name')
    list_filter = ('status', 'location', 'add_time', 'operator')
    list_editable = ('quantity', 'status')
    list_per_page = 20
    fieldsets = (
        (None, {
            'fields': ('name', 'rfid', 'price', 'quantity', 'location', 'status', 'remark', 'operator')
        }),
    )
    # 增加自定义按钮
    actions = ['call_button']

    @admin.action(description='呼叫所有对应物品位置的设备')
    def call_button(self, request, queryset):
        try:
            rfid_list = list(queryset.values_list('rfid', flat=True))
            success, result_message = DevCtrl.callItem(rfid_list, en=True, delay=3)
            if success:
                self.message_user(request, result_message, level='success')
            else:
                self.message_user(request, result_message, level='error')
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            self.message_user(request, error_message, level='error')
    call_button.short_description = "呼叫"
    call_button.icon = 'fa-light fa-phone'
    call_button.type = 'primary'

admin.site.register(Item, ItemAdmin)

class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'rfid', 'remark')
    search_fields = ('name', 'rfid', 'remark')
    list_per_page = 20
admin.site.register(Warehouse,WarehouseAdmin )

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'sn', 'ip_address', 'mac_address', 'last_connection_time', 'add_time')
    search_fields = ('name', 'sn', 'ip_address', 'mac_address', 'location__name')
    ordering = ('-add_time', 'name')
    list_filter = ('location', 'last_connection_time', 'add_time')
    list_per_page = 20
    fieldsets = (
        (None, {
            'fields': ('name', 'location', 'sn', 'ip_address', 'mac_address')
        }),
    )

    actions = ['call_button']

    @admin.action(description='呼叫所选设备')
    def call_button(self, request, queryset):
        try:
            selected_devices = list(queryset)
            for device in selected_devices:
                success, error = DevCtrl.callDevice(device.sn, en=True, delay=3)
                if success:
                    self.message_user(request, f"成功呼叫设备 {device.sn}", level='success')
                else:
                    self.message_user(request, f"呼叫设备 {device.sn} 时发生错误: {error}", level='error')
        except Exception as e:
            self.message_user(request, f"呼叫设备时发生异常: {str(e)}", level='error')
    call_button.short_description = "呼叫"
    call_button.icon = 'fa-light fa-phone'
    call_button.type = 'primary'

admin.site.register(Device, DeviceAdmin)

class EnvironmentAdmin(admin.ModelAdmin):
    list_display = ('device', 'location', 'temperature', 'humidity', 'light', 'add_time')
    search_fields = ('device__name', 'location__name')
    list_per_page = 20
    def get_readonly_fields(self, request, obj=None):
        if obj:  # 编辑现有对象时，所有字段都不可编辑
            return [field.name for field in obj._meta.fields]
        return []  # 创建新对象时，所有字段可编辑
admin.site.register(Environment, EnvironmentAdmin)

class RecordAdmin(admin.ModelAdmin):
    list_display = ('operator', 'item', 'method', 'remark', 'add_time')
    search_fields = ('operator__username', 'item__name')
    list_per_page = 20
    def get_readonly_fields(self, request, obj=None):
        if obj:  # 编辑现有对象时，所有字段都不可编辑
            return [field.name for field in obj._meta.fields]
        return []  # 创建新对象时，所有字段可编辑
admin.site.register(Record, RecordAdmin)

class ThresholdAdmin(admin.ModelAdmin):
    list_display = ('device', 'max_temperature', 'max_humidity', 'max_light')
    search_fields = ('device__name',)
    list_filter = ('device',)
admin.site.register(Threshold, ThresholdAdmin)