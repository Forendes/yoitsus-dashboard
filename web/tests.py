from django.test import TestCase, Client
from django.urls import reverse
from .models import Bot_Resources, BotLog
from .serializers import BotResourcesSerializer, BotLogSerializer
from rest_framework import status
import json

class DashboardViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('dashboard')
        
        self.bot_resources = Bot_Resources.objects.create(
            cpu_usage="50%",
            memory_usage="1024MiB",
            latency="100ms",
            uptime="1:23:45",
            command_count=10
        )
    
    def test_dashboard_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Uptime')
        self.assertContains(response, 'Commands Received')

class APITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.get_latest_data_url = reverse('get_latest_data')
        self.get_latest_logs_url = reverse('get_latest_logs')
        self.receive_bot_resources_url = reverse('receive_bot_resources')
        
        self.bot_resources = Bot_Resources.objects.create(
            cpu_usage="50%",
            memory_usage="1024MiB",
            latency="100ms",
            uptime="1:23:45",
            command_count=10
        )
        self.bot_log = BotLog.objects.create(
            log="Test log",
            timestamp="1984-02-28T03:22:00Z"
        )
    
    def test_get_latest_data(self):
        response = self.client.get(self.get_latest_data_url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'cpu_usage': "50%",
            'memory_usage': "1024MiB",
            'latency': "100ms",
            'uptime': "1:23:45",
            'command_count': 10,
        })
    
    def test_get_latest_logs(self):
        response = self.client.get(self.get_latest_logs_url)
        self.assertEqual(response.status_code, 200)
        logs = json.loads(response.content)
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]['log'], 'Test log')
    
    def test_receive_bot_resources(self):
        data = {
            'cpu_usage': "60%",
            'memory_usage': "2048MiB",
            'latency': "150ms",
            'uptime': "2:34:56",
            'command_count': 5
        }
        response = self.client.post(
            self.receive_bot_resources_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        updated_resource = Bot_Resources.objects.get(id=1)
        self.assertEqual(updated_resource.cpu_usage, "60%")
        self.assertEqual(updated_resource.memory_usage, "2048MiB")
        self.assertEqual(updated_resource.latency, "150ms")
        self.assertEqual(updated_resource.uptime, "2:34:56")
        self.assertEqual(updated_resource.command_count, 15)

class BotLogTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.receive_bot_log_url = reverse('receive_bot_log')
    
    def test_receive_bot_log(self):
        data = {
            'log': 'New test log',
            'timestamp': '2024-07-28T07:32:56Z' # I should fix my sleep schedule
        }
        response = self.client.post(
            self.receive_bot_log_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BotLog.objects.count(), 1)
        self.assertEqual(BotLog.objects.first().log, 'New test log')
