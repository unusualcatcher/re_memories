# consumers.py
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from django.utils import timezone

class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        from .models import GroupMessage, ChatGroup
        from users.models import Profile
        from django.contrib.auth.models import User

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

        chat_group = ChatGroup.objects.get(group_name=self.room_name)
        messages = GroupMessage.objects.filter(group=chat_group).order_by('-created')[:50]
        for message in reversed(messages):
            pfp_url = message.author.profile.pfp.url
            self.send(text_data=json.dumps({
                'username': message.author.username,
                'message': message.body,
                'created': message.created.strftime('%Y-%m-%d %H:%M:%S'),
                'pfp': pfp_url,  # Include profile picture URL
            }))

    def receive(self, text_data):
        from .models import GroupMessage, ChatGroup
        from users.models import Profile
        from django.contrib.auth.models import User

        data = json.loads(text_data)
        message = data['message']
        current_time = data['current_time']
        username = self.scope['user'].username

        chat_group = ChatGroup.objects.get(group_name=self.room_name)
        user = User.objects.get(username=username)
        GroupMessage.objects.create(
            group=chat_group,
            author=user,
            body=message,
            created=timezone.now()
        )

        pfp_url = user.profile.pfp.url

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'created': current_time,
                'pfp': pfp_url,  # Include profile picture URL
            }
        )

    def chat_message(self, event):
        message = event['message']
        username = event['username']
        created = event['created']
        pfp = event['pfp']

        self.send(text_data=json.dumps({
            'username': username,
            'message': message,
            'created': created,
            'pfp': pfp,  # Send profile picture URL to the frontend
        }))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
