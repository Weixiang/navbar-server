from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Item, Record
from .signals import mqtt_received
from .device import MQHandler
import logging
from .crypto import MQTTSafe
import json

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

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
    try:
        payload_dict = json.loads(payload)
    except json.JSONDecodeError as e:
        logger.error(f'Error in decoding JSON: {e}')
        return

    if payload_dict.get("sender") == "server":
        logger.debug('Message from server, no further processing required.')
        return

    logger.info(f'[RAW] Topic: {topic} , Payload:{payload_dict}')

    try:
        payload = MQTTSafe.decrypt(payload_dict)
    except Exception as e:
        logger.error(f'Error in decrypt_message: {e}')
        return

    if topic == 'config':
        MQHandler.config(payload)
    elif topic == 'ping':
        MQHandler.ping(sn, payload)
    elif topic == 'sensor':
        MQHandler.sensor(sn, payload)
    elif topic == 'reader':
        MQHandler.rfid(payload)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)