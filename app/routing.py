from django.urls import path
from .consumer import Myconsumer


websocket_urlpatterns=[
    path('chat/<user1>/<user2>/',Myconsumer.as_asgi()),
]