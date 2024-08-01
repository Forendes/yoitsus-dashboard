from rest_framework import serializers
from .models import Bot_Data, Bot_Resources, BotLog

class BotDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot_Data
        fields = '__all__'

class BotResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot_Resources
        fields = '__all__'

class BotLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotLog
        fields = ['log', 'timestamp']