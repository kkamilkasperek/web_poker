from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/public-chat', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/poker-room/(?P<pk>\w+)', consumers.PokerConsumer.as_asgi())
]