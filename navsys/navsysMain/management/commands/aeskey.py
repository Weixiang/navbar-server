from django.core.management.base import BaseCommand
import os
class Command(BaseCommand):
    help = 'generate_aes_key'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS(f'Successfully [{os.urandom(32)}]'))

