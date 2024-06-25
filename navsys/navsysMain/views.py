from django.shortcuts import render

# Create your views here.

import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .mqtt import client as mqtt_client
from .device import callDevice, callItem
from .serializers import ItemSerializer
from .models import Item

def publish_message(request):
    request_data = json.loads(request.body)
    rc, mid = mqtt_client.publish(request_data['topic'], request_data['msg'])
    return JsonResponse({'code': rc})

@api_view(['POST'])
def call_device_api(request):
    if request.method == 'POST':
        sn = request.data.get('sn')
        en = request.data.get('en', True)
        delay = request.data.get('delay', 3)
        
        try:
            success, error = callDevice(sn, en, delay)
            if success:
                return Response({'success': True, 'message': f'Successfully called device {sn}'})
            else:
                return Response({'success': False, 'error': error}, status=400)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)
    else:
        return Response({'error': 'Method not allowed'}, status=405)
    
@api_view(['POST'])
def call_items_api(request):
    if request.method == 'POST':
        rfid_list = request.data.get('rfid', [])
        en = request.data.get('en', True)
        delay = request.data.get('delay', 3)
        
        try:
            success, result_message = callItem(rfid_list, en, delay)
            if success:
                return Response({'success': True, 'message': result_message})
            else:
                return Response({'success': False, 'error': result_message}, status=400)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)
    else:
        return Response({'error': 'Method not allowed'}, status=405)
    
@api_view(['GET'])
def get_item_by_rfid(request):
    rfid = request.query_params.get('rfid')
    if not rfid:
        return Response({'error': 'RFID parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        item = Item.objects.get(rfid=rfid)
        serializer = ItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Item.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)