from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Bot_Resources, BotLog
from .serializers import BotDataSerializer, BotResourcesSerializer, BotLogSerializer
from django.shortcuts import render
import logging

logger = logging.getLogger('web')

def dashboard_view(request):
    latest_resources = Bot_Resources.objects.first()
    context = {
        'uptime': latest_resources.uptime if latest_resources else '0:00:00',
        'commands_received': latest_resources.command_count if latest_resources else '0',
        'most_requested_track': 'Test'
    }
    return render(request, 'web/dashboard.html', context)

@api_view(['POST'])
def receive_bot_data(request):
    if request.method == 'POST':
        serializer = BotDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def receive_bot_resources(request):
    try:
        instance, created = Bot_Resources.objects.get_or_create(id=1)
        command_count_increment = int(request.data.get('command_count', 0))

        instance.cpu_usage = request.data.get('cpu_usage', instance.cpu_usage)
        instance.memory_usage = request.data.get('memory_usage', instance.memory_usage)
        instance.latency = request.data.get('latency', instance.latency)
        instance.uptime = request.data.get('uptime', instance.uptime)

        instance.command_count += command_count_increment

        instance.save()

        logger.debug(f"Updated command_count: {instance.command_count}")

        return Response(BotResourcesSerializer(instance).data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error in receive_bot_resources: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def test_api(request):
    if request.method == 'GET':
        data = {
            'status': 'success',
            'message': 'GET request received.'
        }
        return JsonResponse(data, status=200)

@api_view(['GET'])
def get_latest_data(request):
    try:
        latest_data = Bot_Resources.objects.all().order_by('-id')[:1]
        if latest_data.exists():
            instance = latest_data[0]
            data = {
                'cpu_usage': instance.cpu_usage,
                'memory_usage': instance.memory_usage,
                'latency': instance.latency,
                'uptime': instance.uptime,
                'command_count': instance.command_count,
            }
        else:
            data = {
                'cpu_usage': 0,
                'memory_usage': 0,
                'latency': 0,
                'uptime': '0:00:00',
                'command_count': '0',
            }
        return JsonResponse(data)
    except Exception as e:
        logger.error(f"Error in get_latest_data: {str(e)}")
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def receive_bot_log(request):
    if request.method == 'POST':
        serializer = BotLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            if BotLog.objects.count() > 100:
                oldest_log = BotLog.objects.order_by('timestamp').first()
                oldest_log.delete()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_latest_logs(request):
    try:
        latest_logs = BotLog.objects.all().order_by('-timestamp')[:100]
        serializer = BotLogSerializer(latest_logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error in get_latest_logs: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
