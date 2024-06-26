from .models import Device, Environment, Item
from django.core.exceptions import ObjectDoesNotExist
from .mqtt import client as mqtt_client
from django.conf import settings
import json
from django.utils import timezone
import logging

from .crypto import MQTTSafe

logger = logging.getLogger('MQTT')


class DevCtrl:
    @staticmethod
    def publish(topic: str, msg: dict):
        try:
            message = json.dumps(msg)
            MQTTSafe.publish(topic, message)
            logger.info(f'Sent message to topic {topic}: {message}')
            return True, None
        except Exception as e:
            error_message = f"Failed to publish message to topic {topic}: {str(e)}"
            logger.error(error_message)
            return False, error_message

    @staticmethod
    def callDevice(sn: str, enable: bool, delay: int = 3):
        topic = f'{settings.MQTT_PERFIX}/call/{sn}'
        message = {'en': enable, 'delay': delay}
        return DevCtrl.publish(topic, message)

    @staticmethod
    def led(sn: str, red: int, green: int, blue: int):
        topic = f'{settings.MQTT_PERFIX}/led/{sn}'
        message = {'r': red, 'g': green, 'b': blue}
        DevCtrl.publish(topic, message)

    @staticmethod
    def beep(sn: str, song: str):
        topic = f'{settings.MQTT_PERFIX}/beep/{sn}'
        message = {'song': song}
        DevCtrl.publish(topic, message)

    @staticmethod
    def pong(sn: str):
        topic = f'{settings.MQTT_PERFIX}/ping/{sn}'
        message = {'msg': 'pong'}
        DevCtrl.publish(topic, message)

    @staticmethod
    def callItem(rfid_list: list, enable: bool, delay: int = 3):
        try:
            items = Item.objects.filter(rfid__in=rfid_list)

            if not items.exists():
                error_message = "No items found for the given RFID list"
                logger.warning(error_message)
                return False, error_message

            locations = set(items.values_list('location', flat=True))
            devices = Device.objects.filter(location__in=locations)

            if not devices.exists():
                error_message = "No devices found for the locations associated with the RFID list"
                logger.warning(error_message)
                return False, error_message

            success_devices = []
            failed_devices = []

            for device in devices:
                success, error = DevCtrl.call_device(device.sn, enable, delay)
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

class MQHandler:
    @staticmethod
    def config(payload: str):
        try:
            data = json.loads(payload)
            name = data.get('name')
            sn = data.get('sn')
            ip_address = data.get('ip')
            mac_address = data.get('mac')

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

    @staticmethod
    def ping(sn: str, payload: str):
        try:
            data = json.loads(payload)
            msg = data.get('msg')
            if msg != 'ping':
                return
            try:
                device = Device.objects.get(sn=sn)
                device.last_connection_time = timezone.now()
                device.save()
                DevCtrl.pong(sn)
                logger.info(f'Updated last_connection_time for device {sn}')
            except Device.DoesNotExist:
                logger.error(f'Device with sn {sn} not found')
        except json.JSONDecodeError as e:
            logger.error(f'Failed to decode JSON: {e}')
        except Exception as e:
            logger.error(f'Error processing message: {e}')

    @staticmethod
    def sensor(sn: str, payload: str):
        try:
            data = json.loads(payload)
            temp = data.get('temp')
            humi = data.get('humi')
            light = data.get('light')

            if not any([temp, humi, light]):
                logger.error('Missing fields in payload')
                return

            try:
                device = Device.objects.get(sn=sn)
                Environment.objects.create(
                    device=device,
                    location=device.location,
                    temperature=temp,
                    humidity=humi,
                    light=light
                )
                logger.info('New environment record added')
            except Device.DoesNotExist:
                logger.error(f'Device with sn {sn} not found')
        except json.JSONDecodeError as e:
            logger.error(f'Failed to decode JSON: {e}')
        except Exception as e:
            logger.error(f'Error processing message: {e}')

    @staticmethod
    def rfid(payload: str):
        try:
            data = json.loads(payload)
            rfid = data.get('rfid')
            delay = data.get('delay', 3)
            if not rfid:
                logger.error('Missing field in payload: rfid')
                return
            try:
                item = Item.objects.get(rfid=rfid)
                device = Device.objects.get(location=item.location)
                DevCtrl.call_device(device.sn, True, delay)
                logger.info(f'RFID Call Device with sn: {device.sn}')
            except Item.DoesNotExist:
                logger.error(f'Item with RFID {rfid} not found')
            except Device.DoesNotExist:
                logger.error(f'Device with location {item.location} not found')
        except json.JSONDecodeError as e:
            logger.error(f'Failed to decode JSON: {e}')
        except Exception as e:
            logger.error(f'Error processing message: {e}')
