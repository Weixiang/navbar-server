default_app_config = 'Navsysmain.apps.NavsysmainConfig'

from . import mqtt
mqtt.client.loop_start()
