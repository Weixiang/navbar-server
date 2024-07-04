from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Item, Record, Environment, Threshold
from .signals import mqtt_received
from .device import MQHandler
import logging
from .crypto import MQTTSafe
import json
import base64

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .qywxbot import sendwx

logger = logging.getLogger('MQTT')
loggerdb = logging.getLogger('DB')

@receiver(post_save, sender=Item)
def create_record(sender, instance, created, **kwargs):
    if created:
        method = 'in'
        remark = f"物品 {instance.name} 被创建，数量: {instance.quantity}, 位置: {instance.location.name}, 状态: {instance.get_status_display()}."
    else:
        method = instance.status
        remark = f"物品 {instance.name} 被更新，数量: {instance.quantity}, 位置: {instance.location.name}, 状态: {instance.get_status_display()}."
    loggerdb.debug(remark)
    Record.objects.create(
        operator=instance.operator,
        item=instance,
        method=method,
        remark=remark
    )

@receiver(mqtt_received)
def handle_mqtt_message(sender, topic, payload, sn, **kwargs):

    if settings.ENCRYPT == "BASE64":
        try:
            payload = base64.b64decode(payload)
            payload = payload.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError) as e:
            logger.error(f'Error in BASE64 decoding: {e}')
            return

    try:
        payload_dict = json.loads(payload)
    except json.JSONDecodeError as e:
        logger.error(f'Error in decoding JSON: {e}')
        return

    if payload_dict.get("sender") == "server":
        logger.debug('Message from server, no further processing required.')
        return

    logger.info(f'[RAW] Topic: {topic} , Payload: {payload_dict}')

    if settings.ENCRYPT == "AES":
        try:
            payload_dict = MQTTSafe.decrypt(payload_dict)
        except ValueError as ve:
            logger.error(f'ValueError in decrypt_message: {ve}')
            return
        except Exception as e:
            logger.error(f'Unexpected error in decrypt_message: {e}')
            return
    
    logger.info(f'[解码完毕] Payload: {payload_dict} {type(payload_dict)}')

    # Handle the decrypted payload based on topic
    topic_handlers = {
        'config': MQHandler.config,
        'ping': MQHandler.ping,
        'sensor': MQHandler.sensor,
        'reader': MQHandler.rfid
    }

    handler = topic_handlers.get(topic)
    if handler:
        handler(sn, payload_dict)
    else:
        logger.warning(f'No handler for topic: {topic}')


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Environment)
def check_threshold(sender, instance, **kwargs):
    try:
        threshold = Threshold.objects.get(device=instance.device)
        if instance.temperature is not None and threshold.max_temperature is not None and instance.temperature > threshold.max_temperature:
            msg = f"设备 {instance.device.name} 的温度 {instance.temperature} 超过了阈值 {threshold.max_temperature}"
            logger.info(msg)
            sendwx(msg)

        if instance.humidity is not None and threshold.max_humidity is not None and instance.humidity > threshold.max_humidity:
            msg = f"设备 {instance.device.name} 的湿度 {instance.humidity} 超过了阈值 {threshold.max_humidity}"
            logger.info(msg)
            sendwx(msg)

        if instance.light is not None and threshold.max_light is not None and instance.light > threshold.max_light:
            msg = f"设备 {instance.device.name} 的光照 {instance.light} 超过了阈值 {threshold.max_light}"
            logger.info(msg)
            sendwx(msg)
            
    except Threshold.DoesNotExist:
        logger.debug(f"设备 {instance.device.name} 没有设置阈值")