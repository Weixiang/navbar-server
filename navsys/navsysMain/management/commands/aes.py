# 文件路径: your_app/management/commands/encrypt_decrypt.py

from django.core.management.base import BaseCommand
from navsysMain.crypto import MQTTSafe  # 请根据实际情况调整导入路径

class Command(BaseCommand):
    help = 'Encrypts or decrypts a payload using AES'

    def add_arguments(self, parser):
        parser.add_argument('action', choices=['encrypt', 'decrypt'], help='Action to perform: encrypt or decrypt')
        parser.add_argument('payload', help='Payload to process')

    def handle(self, *args, **options):
        action = options['action']
        payload = options['payload']

        if action == 'encrypt':
            encrypted_payload = MQTTSafe._encrypt_payload(payload)
            self.stdout.write(self.style.SUCCESS(f'Encrypted payload: {encrypted_payload}'))
        elif action == 'decrypt':
            decrypted_payload = MQTTSafe._decrypt_payload(payload)
            self.stdout.write(self.style.SUCCESS(f'Decrypted payload: {decrypted_payload}'))
