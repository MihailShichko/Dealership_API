from django.urls import re_path

from dealership_app.consumers.consumers import CarPostConsumer

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', CarPostConsumer.as_asgi()),
]
