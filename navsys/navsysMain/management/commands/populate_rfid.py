from django.core.management.base import BaseCommand
from navsysMain.models import Item
from navsysMain.utils import generate_random_rfid

class Command(BaseCommand):
    help = 'Populate RFID values for existing items'

    def handle(self, *args, **kwargs):
        items = Item.objects.all()
        for item in items:
            if not item.rfid:
                unique_rfid = False
                while not unique_rfid:
                    rfid = generate_random_rfid()
                    if not Item.objects.filter(rfid=rfid).exists():
                        unique_rfid = True
                        item.rfid = rfid
                        item.save()
                        self.stdout.write(self.style.SUCCESS(f'Successfully set RFID for item {item.id}'))
            else:
                self.stdout.write(self.style.WARNING(f'Item {item.id} already has an RFID'))
