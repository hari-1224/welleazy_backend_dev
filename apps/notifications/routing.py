from django.urls import path
from .consumers import NotificationConsumer

ws_urlpatterns = [
    path("ws/notifications/", NotificationConsumer.as_asgi()),
]
