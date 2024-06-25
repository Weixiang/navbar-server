from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import json
import logging
from django.conf import settings
from .mqtt import client as mqtt_client

logger = logging.getLogger('AES')

class MQTTSafe:
    @staticmethod
    def _encrypt_payload(payload):
        """
        Encrypts the payload using AES ECB mode with settings.AES_KEY.
        Returns the encrypted payload as a JSON string.
        """
        cipher = AES.new(settings.AES_KEY.encode(), AES.MODE_ECB)  # Use ECB mode
        padded_data = pad(payload.encode('utf-8'), AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        encrypted_payload = base64.b64encode(encrypted_data).decode('utf-8')
        return json.dumps({'data': encrypted_payload})

    @staticmethod
    def publish(topic, payload):
        try:
            if settings.USE_AES:
                logger.debug(f'Original payload: {payload}')
                encrypted_payload = MQTTSafe._encrypt_payload(payload)
                logger.debug(f'Encrypted payload: {encrypted_payload}')
                mqtt_client.publish(topic, encrypted_payload)
            else:
                mqtt_client.publish(topic, payload)
            return True
        except Exception as e:
            logger.error(f'Error in publish: {e}')
            return False

    @staticmethod
    def _decrypt_payload(encrypted_payload):
        """
        Decrypts the payload using AES ECB mode with settings.AES_KEY.
        Accepts base64 encoded payload as input.
        Returns the decrypted payload as a string.
        """
        encrypted_data = base64.b64decode(encrypted_payload)
        cipher = AES.new(settings.AES_KEY.encode(), AES.MODE_ECB)  # Use ECB mode
        decrypted_data = cipher.decrypt(encrypted_data)
        decrypted_data = unpad(decrypted_data, AES.block_size)
        decrypted_payload = decrypted_data.decode('utf-8')
        logger.debug(f'Decrypted payload: {decrypted_payload}')
        return decrypted_payload

    @staticmethod
    def decrypt(payload):
        try:
            if settings.USE_AES:
                payload_json = json.loads(payload)
                encrypted_payload = payload_json['data']
                return MQTTSafe._decrypt_payload(encrypted_payload)
            else:
                return payload
        except Exception as e:
            logger.error(f'Error in decrypt: {e}')
            raise
