# consumers.py will handle web socket traffic

import json

from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser

from asgiref.sync import sync_to_async #???

from .models import Chat
from .utils import get_live_score_for_gameclass 

# Create a consumer class
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join room based on name in the URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # self.room_group_name = f'chat_{self.room_name}'

        if self.scope['user'] == AnonymousUser():
            raise DenyConnection("The user does not exist")

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # await self.accept()

        # If invalid chat id then deny the connection.
        try:
            self.game = Chat.objects.get(pk=self.room_name)
        except ObjectDoesNotExist:
            raise DenyConnection("Wrong chat ID")

        await self.accept()

    # async def receive(self, text_data):
    #    game_city = json.loads(text_data).get('game_city')

    #    await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'live_score',
    #             'game_id': self.room_name,
    #             'game_city': game_city
    #         }
    #     )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )