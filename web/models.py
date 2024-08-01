from django.db import models

class Bot_Data(models.Model):
    message = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Bot_Resources(models.Model):
    cpu_usage = models.CharField(max_length=255)
    memory_usage = models.CharField(max_length=255)
    latency = models.CharField(max_length=255)
    uptime = models.CharField(max_length=255)
    command_count = models.IntegerField()

class BotLog(models.Model):
    log = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)