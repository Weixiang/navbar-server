from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import json
import logging
from django.conf import settings
from .mqtt import client as mqtt_client
from datetime import datetime, timezone, timedelta

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
        return encrypted_payload

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
    def _encrypt_base64(data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        if isinstance(data, bytes):
            encoded_data = base64.b64encode(data)
            encoded_data = encoded_data.decode('utf-8')
            return encoded_data
        else:
            raise TypeError("Input must be a string or bytes")

    @staticmethod
    def _decode_base64(data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        if isinstance(data, bytes):
            decoded_data = base64.b64decode(data)
            decoded_data = decoded_data.decode('utf-8')
            return decoded_data
        else:
            raise TypeError("Input must be a string or bytes")

    @staticmethod
    def publish(topic, msg):
        msg["sender"] = "server"

        beijing_tz = timezone(timedelta(hours=8))
        current_time_beijing = datetime.now(beijing_tz)
        msg["timestamp"] = current_time_beijing.isoformat()

        payload = json.dumps(msg)
        try:
            if settings.ENCRYPT == "AES":
                logger.debug(f'[AES] Original SEND payload: {payload} {type(payload)}')
                encrypted_raw = MQTTSafe._encrypt_payload(payload)
                encrypted_payload = json.dumps({'data': encrypted_raw})
                logger.debug(f'[AES] Encrypted SEND payload: {encrypted_payload}')
                mqtt_client.publish(topic, encrypted_payload)
                return True
            elif settings.ENCRYPT == "BASE64":
                logger.debug(f'[BASE64] Original SEND payload: {payload} {type(payload)}')
                result = MQTTSafe._encrypt_base64(payload)
                logger.debug(f'[BASE64] Encrypted SEND payload: {result} {type(result)}')
                mqtt_client.publish(topic, result)
                return True
            else:
                mqtt_client.publish(topic, payload)
            return True
        except Exception as e:
            logger.error(f'[PUBLISH] Error in publish: {e}')
            return False

    @staticmethod
    def decrypt(payload):
        try:
            if settings.ENCRYPT == "AES":
                encrypted_payload = payload['data']
                result = MQTTSafe._decrypt_payload(encrypted_payload)
                result_dict = json.loads(result)
                return result_dict
            elif settings.ENCRYPT == "BASE64":
                result = MQTTSafe._decrypt_payload(encrypted_payload)
                result_dict = json.loads(result)
                return result_dict
            else:
                return payload
        except KeyError as ke:
            logger.error(f'Missing key in payload: {ke}')
            raise
        except Exception as e:
            logger.error(f'Error in decrypt: {e}')
            raise

