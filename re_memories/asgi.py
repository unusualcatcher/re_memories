import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import re_path
from chat.consumers import ChatRoomConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 're_memories.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatRoomConsumer.as_asgi()), 
            ])
        )
    ),
})
