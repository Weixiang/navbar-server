
# inventory/utils.py

import string
import random

def generate_random_rfid(length=12):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
