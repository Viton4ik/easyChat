# consumers.py will handle web socket traffic

import json

from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser

from asgiref.sync import sync_to_async

from .models import Chat, Message

from django.contrib.auth.models import User

from datetime import datetime

# Create a consumer class
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join room based on name in the URL
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_id = 'chat_%s' % self.room_id

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_id,
            self.channel_name
        )

        await self.accept()

    # async def disconnect(self, close_code):
    #     await self.channel_layer.group_discard(
    #         self.room_group_id,
    #         self.channel_name
    #     )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']

        await self.save_message(username, message, room)

        await self.channel_layer.group_send(
            self.room_group_id,
            {
            'type': 'chat_message',
            'message': message,
            'username': username,
            'room': room,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event['room']
        
        now = datetime.now()
        timestamp = now.strftime("%B %d, %Y, %I:%M %p")

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'room': room,
            'timestamp': timestamp,
        }))

    @sync_to_async
    def save_message(self, username, message, room):
        user = User.objects.get(username=username)
        room = Chat.objects.get(id=room)

        Message.objects.create(user=user, chat=room, content=message)
