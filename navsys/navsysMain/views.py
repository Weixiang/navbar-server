from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.views import View

from .mqtt import client as mqtt_client
from .device import DevCtrl
from .serializers import ItemSerializer
from .models import Item
from .crypto import MQTTSafe
from .forms import RFIDQueryForm, DataForm

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from django.conf import settings
import base64

import logging
logger = logging.getLogger('WEB')

# 网页
def index(request):
    context = {
        'project_name': 'MyProject',  # 项目名称
        'about': '这里是项目的简要说明。',  # 项目说明
    }
    logger.info("Project homepage accessed")
    return render(request, 'index.html', context)

@login_required
def crypt(request):
    encrypted_data = None
    decrypted_data = None

    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['data']
            if 'encrypt' in request.POST:
                if settings.ENCRYPT == "AES":
                    encrypted_data = MQTTSafe._encrypt_payload(data)
                else:
                    encrypted_data = MQTTSafe._encrypt_base64(data)
            elif 'decrypt' in request.POST:
                if settings.ENCRYPT == "AES":
                    decrypted_data = MQTTSafe._decrypt_payload(data)
                else:
                    decrypted_data = MQTTSafe._decode_base64(data)

    else:
        form = DataForm()

    return render(request, 'crypt.html', {
        'form': form,
        'encrypted_data': encrypted_data,
        'decrypted_data': decrypted_data
    })

@login_required
def query_item_by_rfid(request):
    item = None
    error_message = None

    if request.method == 'POST':
        if 'call_item' in request.POST:
            rfid = request.POST.get('rfid')
            if rfid:
                try:
                    success, result_message = DevCtrl.callItem([rfid], True, 10)
                    return JsonResponse({'success': success, 'message': result_message})
                except Exception as e:
                    return JsonResponse({'success': False, 'message': str(e)})
        else:
            form = RFIDQueryForm(request.POST)
            if form.is_valid():
                rfid = form.cleaned_data['rfid']
                try:
                    item = get_object_or_404(Item, rfid=rfid)
                except Http404:
                    error_message = "未找到匹配的物品。"
    else:
        form = RFIDQueryForm()

    return render(request, 'rfid.html', {'form': form, 'item': item, 'error_message': error_message})

# API
def common_decorators(view_func):
    def wrapper(self, request, *args, **kwargs):
        try:
            return view_func(self, request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error occurred in view {view_func.__name__}: {str(e)}", exc_info=True)
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper

class PublishMessageView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = (IsAuthenticated,)

    @common_decorators
    def post(self, request):
        try:
            request_data = request.data
            topic = request_data.get('topic')
            msg = request_data.get('msg')

            if not topic or not msg:
                logger.warning("Publish message failed: topic or msg missing")
                return Response({'error': 'Both topic and msg are required'}, status=status.HTTP_400_BAD_REQUEST)

            rc, mid = mqtt_client.publish(topic, msg)
            logger.info(f"Published message to topic '{topic}' with rc={rc}")

            if rc == 0:
                return Response({'code': rc, 'message': 'Message published successfully'})
            else:
                logger.error(f"Failed to publish message to topic '{topic}' with rc={rc}")
                return Response({'code': rc, 'message': 'Failed to publish message'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Exception in PublishMessageView: {str(e)}", exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CallDeviceAPIView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = (IsAuthenticated,)

    @common_decorators
    def post(self, request):
        try:
            sn = request.data.get('sn')
            en = request.data.get('en', True)
            delay = request.data.get('delay', 3)

            logger.info(f"Calling device with SN: {sn}, EN: {en}, Delay: {delay}")
            success, error = DevCtrl.callDevice(sn, en, delay)
            if success:
                return Response({'success': True, 'message': f'Successfully called device {sn}'})
            else:
                logger.warning(f"Failed to call device {sn}: {error}")
                return Response({'success': False, 'error': error}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Exception in CallDeviceAPIView: {str(e)}", exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CallItemsAPIView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = (IsAuthenticated,)

    @common_decorators
    def post(self, request):
        try:
            rfid_list = request.data.get('rfid', [])
            en = request.data.get('en', True)
            delay = request.data.get('delay', 3)

            logger.info(f"Calling items with RFID list: {rfid_list}, EN: {en}, Delay: {delay}")
            success, result_message = DevCtrl.callItem(rfid_list, en, delay)
            if success:
                return Response({'success': True, 'message': result_message})
            else:
                logger.warning(f"Failed to call items: {result_message}")
                return Response({'success': False, 'error': result_message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Exception in CallItemsAPIView: {str(e)}", exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetItemByRFIDAPIView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = (IsAuthenticated,)

    @common_decorators
    def get(self, request):
        try:
            rfid = request.query_params.get('rfid')
            if not rfid:
                logger.warning("Get item by RFID failed: RFID parameter missing")
                return Response({'error': 'RFID parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

            logger.info(f"Fetching item with RFID: {rfid}")
            item = Item.objects.get(rfid=rfid)
            serializer = ItemSerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            logger.warning(f"Item with RFID {rfid} not found")
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Exception in GetItemByRFIDAPIView: {str(e)}", exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EncryptAPIView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            payload = request.data.get('payload')

            if not payload:
                logger.warning("Encrypt failed: payload missing")
                return Response({'error': 'Payload is required'}, status=status.HTTP_400_BAD_REQUEST)

            logger.info("Performing encrypt action on payload")
            result = MQTTSafe._encrypt_payload(payload)

            return Response({'result': result}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Exception in EncryptAPIView: {str(e)}", exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DecryptAPIView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            payload = request.data.get('payload')

            if not payload:
                logger.warning("Decrypt failed: payload missing")
                return Response({'error': 'Payload is required'}, status=status.HTTP_400_BAD_REQUEST)

            logger.info("Performing decrypt action on payload")
            result = MQTTSafe._decrypt_payload(payload)

            return Response({'result': result}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Exception in DecryptAPIView: {str(e)}", exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)