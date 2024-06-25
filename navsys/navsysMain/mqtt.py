import paho.mqtt.client as mqtt
from django.conf import settings
from .signals import mqtt_received
import logging
logger = logging.getLogger('MQTT')

def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        logger.info(f'Connected successfully')
        logger.debug(f'{mqtt_client}, {userdata}, {flags}')
        mqtt_client.subscribe(f'{settings.MQTT_PERFIX}/#')  # 使用 QoS 0
    else:
        logger.error(f'Bad connection. Code: {rc}')

def on_disconnect(mqtt_client, userdata, rc):
    if rc != 0:
        logger.warning("Unexpected disconnection.")
    else:
        logger.info("Disconnected successfully.")

# 定义全局变量用来存储上一条处理过的消息的内容和主题
last_message = {
    'topic': None,
    'payload': None
}

def on_message(mqtt_client, userdata, msg):
    global last_message
    logger.debug(f'Received message on topic: {msg.topic} with payload: {msg.payload} in client {mqtt_client}')

    # 检查是否与上一条消息相同
    if last_message['topic'] == {msg.topic} and last_message['payload'] == {msg.payload}:
        logger.debug('Received duplicate message. Skipping processing.')
        return
    
    # 更新上一条消息的内容和主题
    last_message['topic'] = {msg.topic}
    last_message['payload'] = {msg.payload}

    topic = msg.topic.split('/')[1]
    sn = msg.topic.split('/')[-1]
    payload = msg.payload

    logger.debug({type(payload)})
    
    # 发送信号，处理消息
    mqtt_received.send(sender=None, topic=topic, sn=sn, payload=payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(
    host=settings.MQTT_SERVER,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEPALIVE
)
