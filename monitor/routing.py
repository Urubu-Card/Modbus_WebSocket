from django.urls import re_path
from . import cosumers

websocket_urlpatterns = [
    re_path(r"ws/plant/$",cosumers.PlantMonitorCosumer.as_asgi()),
]