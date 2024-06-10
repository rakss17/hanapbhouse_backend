import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from channels.exceptions import DenyConnection

class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        

        # Send previous messages to WebSocket
        messages =  await self.get_messages(self.room_name)
        for message in messages:
            await self.send(text_data=json.dumps({
                'message': message.content,
                'sender': message.sender,
                'send_timestamp': message.send_timestamp.isoformat(),
                'receiver': message.receiver,
                'read_timestamp': message.read_timestamp.isoformat(),
                'is_read_by_receiver': message.is_read_by_receiver
            }))
    
    @sync_to_async
    def get_messages(self, room_name):
        try:
            return Message.objects.filter(room_name=room_name).order_by('send_timestamp')
        except Message.DoesNotExist:
            raise DenyConnection("Invalid Message")

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        receiver = text_data_json['receiver']

        # Save message to database
        sender_obj = User.objects.get(id=sender)
        receiver_obj = User.objects.get(id=receiver)
        message_obj = Message.objects.create(room_name=self.room_name, content=message, sender=sender_obj, receiver=receiver_obj)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'send_timestamp': message_obj.send_timestamp.isoformat(),
                'receiver': receiver,
                'read_timestamp': message_obj.read_timestamp.isoformat(),
                'is_read_by_receiver': message_obj.is_read_by_receiver
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        send_timestamp = event['send_timestamp']
        receiver = event['receiver']
        read_timestamp = event['read_timestamp']
        is_read_by_receiver = event['is_read_by_receiver']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'send_timestamp': send_timestamp,
            'receiver': receiver,
            'read_timestamp': read_timestamp,
            'is_read_by_receiver': is_read_by_receiver
        }))
