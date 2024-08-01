import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from django.apps import apps

logger = logging.getLogger('web')

class BotResourcesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        logger.info("WebSocket connection accepted")

    async def disconnect(self, close_code):
        logger.info(f"WebSocket connection closed with code {close_code}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            logger.info(f"Received data: {data}")

            Bot_Resources = apps.get_model('web', 'Bot_Resources')
            instance, created = Bot_Resources.objects.get_or_create(id=1)
            command_count_increment = int(data.get('command_count', 0))

            logger.debug(f"Current command_count: {instance.command_count}")
            logger.debug(f"Received command_count increment: {command_count_increment}")

            instance.cpu_usage = data.get('cpu_usage', instance.cpu_usage)
            instance.memory_usage = data.get('memory_usage', instance.memory_usage)
            instance.latency = data.get('latency', instance.latency)
            instance.uptime = data.get('uptime', instance.uptime)
            instance.command_count += command_count_increment

            instance.save()
            logger.debug(f"Updated command_count: {instance.command_count}")

            await self.send(text_data=json.dumps({
                'cpu_usage': instance.cpu_usage,
                'memory_usage': instance.memory_usage,
                'latency': instance.latency,
                'uptime': instance.uptime,
                'command_count': instance.command_count,
            }))
            logger.info("Data sent to frontend")
        except Exception as e:
            logger.error(f"Error in receive_bot_resources: {str(e)}")
            await self.send(text_data=json.dumps({
                'error': str(e)
            }))
