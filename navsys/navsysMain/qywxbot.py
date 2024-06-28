import requests
import json
from django.conf import settings
import logging
logger = logging.getLogger('WEB')

def sendwx(content):
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=" + settings.QYWXBOT_KEY
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()
