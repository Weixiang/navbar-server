from .models import Device, Environment, Item
from django.core.exceptions import ObjectDoesNotExist
from .mqtt import client as mqtt_client
from django.conf import settings
import json
# from datetime import datetime
from django.utils import timezone
import time
import logging

from .crypto import MQTTSafe

logger = logging.getLogger('MQTT')

def callDevice(sn: str, en: bool, delay: int = 3):
    try:
        topic = f'{settings.MQTT_PERFIX}/call/{sn}'
        msg = json.dumps({'en': en, 'delay': delay})
        MQTTSafe.publish(topic, msg)
        logger.info(f'Sent callDevice to {sn} with en: {en} and delay: {delay}')
        return True, None  # 返回成功标志和无错误信息
    except Exception as e:
        error_message = f"Failed to send callDevice to {sn}: {str(e)}"
        logger.error(error_message)
        return False, error_message # 返回失败标志和错误信息

def callItem(rfid_list: list, en: bool, delay: int = 3):
    try:
        items = Item.objects.filter(rfid__in=rfid_list)

        if not items.exists():
            error_message = "No items found for the given RFID list"
            logger.warning(error_message)
            return False, error_message

        locations = set(items.values_list('location', flat=True))
        
        devices = Device.objects.filter(location__in=locations)
        
        if not devices.exists():
            # 如果没有找到任何设备，记录警告日志并返回失败
            error_message = "No devices found for the locations associated with the RFID list"
            logger.warning(error_message)
            return False, error_message
        
        success_devices = []
        failed_devices = []

        for device in devices:
            success, error = callDevice(device.sn, en, delay)
            if success:
                success_devices.append(device.sn)
            else:
                failed_devices.append((device.sn, error))

        if failed_devices:
            success_message = f"Successfully called devices: {', '.join(success_devices)}"
            failed_message = f"Failed to call devices: {', '.join([f'{sn} ({error})' for sn, error in failed_devices])}"
            logger.error(f"{success_message}. {failed_message}")
            return False, f"{success_message}. {failed_message}"
        else:
            logger.info(f"Successfully called all devices: {', '.join(success_devices)}")
            return True, f"Successfully called all devices: {', '.join(success_devices)}"

    except Exception as e:
        error_message = f"An error occurred while calling devices for the given RFID list: {str(e)}"
        logger.error(error_message)
        return False, error_message

def ledCtrl(sn: str, r: int, g: int, b: int):
    topic = f'{settings.MQTT_PERFIX}/led/{sn}'
    msg = json.dumps({'r': r, 'g': g, 'b': b})
    MQTTSafe.publish(topic, msg)
    logger.info(f'Sent ledCtrl to {sn} with r: {r}, g: {g}, b: {b}')

def beepCtrl(sn: str, song: str):
    topic = f'{settings.MQTT_PERFIX}/beep/{sn}'
    msg = json.dumps({'song': song})
    MQTTSafe.publish(topic, msg)
    logger.info(f'Sent beepCtrl to {sn} with song: {song}')

def pong(sn: str):
    topic = f'{settings.MQTT_PERFIX}/ping/{sn}'
    msg = json.dumps({'msg': 'pong'})
    MQTTSafe.publish(topic, msg)
    logger.info(f'Sent pong to {sn}')


# 消息处理

def handle_config(payload: str):
    try:
        data = json.loads(payload)
        name = data.get('name')
        sn = data.get('sn')
        ip_address = data.get('ip')
        mac_address = data.get('mac')

        # 检查哪些字段缺失
        missing_fields = [field for field, value in {
            'name': name,
            'sn': sn,
            'ip_address': ip_address,
            'mac_address': mac_address
        }.items() if not value]

        if missing_fields:
            logger.error(f'Missing fields in payload: {", ".join(missing_fields)}')
            return

        try:
            device = Device.objects.get(sn=sn)
            device.name = name
            device.ip_address = ip_address
            device.mac_address = mac_address
            device.save()
            logger.info(f'Device updated: {device}')
        except ObjectDoesNotExist:
            Device.objects.create(
                name=name,
                sn=sn,
                ip_address=ip_address,
                mac_address=mac_address,
                last_connection_time=timezone.now()
            )
            logger.info('New device added')
    except json.JSONDecodeError as e:
        logger.error(f'Failed to decode JSON: {e}')
    except Exception as e:
        logger.error(f'Error processing message: {e}')

def handle_ping(sn:str, payload:str):
    try:
        data = json.loads(payload)
        msg = data.get('msg')
        if not msg == 'ping':
            return
        device = Device.objects.get(sn=sn)
        device.last_connection_time = timezone.now()
        device.save()
        pong(sn)
        logger.info(f'Updated last_connection_time for device {sn}')
    except Device.DoesNotExist:
        logger.error(f'Device with sn {sn} not found')

def handle_sensor(sn: str, payload: str):
    try:
        data = json.loads(payload)
        temp = data.get('temp')
        humi = data.get('humi')
        light = data.get('light')
        # 确保至少有一个传感器数据
        if not any([temp, humi, light]):
            logger.error('Missing fields in payload')
            return
        try:
            # 获取设备
            device = Device.objects.get(sn=sn)
            # 创建环境记录
            Environment.objects.create(
                device=device,       # 使用设备对象
                location=device.location,  # 使用设备的位置
                temperature=temp,
                humidity=humi,
                light=light
            )
            logger.info('New environment record added')
        except ObjectDoesNotExist:
            logger.error(f'Device with sn {sn} not found')
    except json.JSONDecodeError as e:
        logger.error(f'Failed to decode JSON: {e}')
    except Exception as e:
        logger.error(f'Error processing message: {e}')


def handle_rfid(payload: str):
    try:
        data = json.loads(payload)
        rfid = data.get('rfid')
        delay = data.get('delay', 3)
        if not rfid:
            logger.error('Missing field in payload: rfid')
            return
        try:
            item = Item.objects.get(rfid=rfid)
            location = item.location
            device = Device.objects.get(location=location)
            sn = device.sn
            callDevice(sn, True, delay)
            logger.info(f'RFID Call Device with sn: {sn}')
        except Item.DoesNotExist:
            logger.error(f'Item with RFID {rfid} not found')
        except Device.DoesNotExist:
            logger.error(f'Device with location {location} not found')
    except json.JSONDecodeError as e:
        logger.error(f'Failed to decode JSON: {e}')
    except TypeError as e:
        logger.error(f'Error processing message, type error: {e}')
    except Exception as e:
        logger.error(f'Error processing message: {e}')