from django.urls import path
from . import views

urlpatterns = [
    path('bot-data/', views.receive_bot_data, name='receive_bot_data'),
    path('bot-resources/', views.receive_bot_resources, name='receive_bot_resources'),
    path('test-api/', views.test_api, name='test_api'),
    path('', views.dashboard_view, name='dashboard'),
    path('get_latest_data/', views.get_latest_data, name='get_latest_data'),
    path('bot-log/', views.receive_bot_log, name='receive_bot_log'),
    path('get_latest_logs/', views.get_latest_logs, name='get_latest_logs'),

]
