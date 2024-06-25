from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Item, Record
from .signals import mqtt_received
from .device import handle_config, handle_ping, handle_rfid, handle_sensor
import logging
from .crypto import MQTTSafe

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
    logger.info(f'[RAW] Topic: {topic} , Payload:{payload} {type(payload)}')

    try:
        payload = MQTTSafe.decrypt(payload)
    except Exception as e:
        logger.error(f'Error in decrypt_message: {e}')
        return

    if topic == 'config':
        handle_config(payload)
    elif topic == 'ping':
        handle_ping(sn, payload)
    elif topic == 'sensor':
        handle_sensor(sn, payload)
    elif topic == 'reader':
        handle_rfid(payload)


