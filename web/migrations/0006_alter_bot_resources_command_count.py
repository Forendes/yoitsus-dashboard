# Generated by Django 5.0.6 on 2024-07-24 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_bot_resources_command_count_bot_resources_uptime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot_resources',
            name='command_count',
            field=models.IntegerField(),
        ),
    ]
