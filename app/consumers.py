import json, asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, PublicChat, PokerRoom, RoomUser
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'public_chat'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        await self.send(text_data=json.dumps({
            'message': 'Connected to the chat room'
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        user = await self.get_user(sender)

        public_chat, created = await self.get_or_create_public_chat()
        message_record = await self.create_message(public_chat, user, message)

        timestamp = message_record.timestamp.strftime('%b-%d-%Y %H:%M:%S')

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'timestamp': timestamp
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        timestamp = event["timestamp"]

        await self.send(text_data=json.dumps({
            'sender': sender,
            'message': message,
            'timestamp': timestamp
        }))

    @database_sync_to_async
    def get_or_create_public_chat(self):
        return PublicChat.objects.get_or_create(id=1)

    @database_sync_to_async
    def get_user(self, username):
        return User.objects.get(username=username)

    @database_sync_to_async
    def create_message(self, public_chat, sender, message):
        return Message.objects.create(public_chat=public_chat, sender=sender, message=message,)


connected_users = []
loop_running = False
class PokerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = f'poker_{self.room_name}'
        self.user_response = False
        global loop_running
        global connected_users


        await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
        )

        connected_users.append(self)
        print(connected_users)

        await self.accept()

        await self.send(text_data=json.dumps({
            'message': 'Connected to the poker room'
        }))
        await self.add_user_to_room()

        if len(connected_users) > 1 and not loop_running:
            loop_running = True
            asyncio.create_task(self.loop_messages())

        self.timeout_task = asyncio.create_task(self.handle_timeout())


    async def handle_timeout(self):
        try:
           await asyncio.sleep(30)
           if not self.user_response:
               await self.send(text_data=json.dumps({
                     'message': '30 seconds have passed without a response'
               }))
               await self.remove_user_from_room()
               await self.disconnect(1000)
        except asyncio.CancelledError:
            pass

    async def loop_messages(self):
        while len(connected_users) > 1:
            for user in connected_users:
                user.user_response = False
                await user.send(text_data=json.dumps({
                    'message': 'loop'
                }))
                await asyncio.sleep(10)
        global loop_running
        loop_running = False

    async def disconnect(self, code):
        self.timeout_task.cancel()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        if self in connected_users:
            connected_users.remove(self)
        print(connected_users)

        await self.close()

    async def receive(self, text_data):
        self.user_response = True
        self.timeout_task.cancel()
        data = json.loads(text_data)
        if data['message'] == 'leave_room':
            await self.remove_user_from_room()
            await self.disconnect(1000)
            return
        counter = data['counter']
        user = self.scope['user']

        await self.send(text_data=json.dumps({
            'message': f"Button clicked {counter} times",
        }))

    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
        }))

    @database_sync_to_async
    def remove_user_from_room(self):
        print('Removing user from room')
        room = PokerRoom.objects.get(id=self.room_name)
        user_to_del = RoomUser.objects.get(user=self.scope['user'], room=room)
        asyncio.run(self.send_remove_user_front(user_to_del.position))
        user_to_del.delete()

    @database_sync_to_async
    def add_user_to_room(self):
        room = PokerRoom.objects.get(id=self.room_name)
        user_to_add = RoomUser.objects.get(user=self.scope['user'], room=room)
        asyncio.run(self.send_add_user_front(user_to_add.position, user_to_add.user.username))

    async def send_remove_user_front(self, position):
        print('remove signal sent')
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'remove_user',
                'exclude_leaver': self.channel_name,
                'position': position
            })

    async def remove_user(self, event):
        leaver = event['exclude_leaver']
        if leaver == self.channel_name:
            await self.send(text_data=json.dumps({
                'message': 'refresh'
            }))
        else:
            await self.send(text_data=json.dumps({
                'message': 'remove_user',
                'position': event['position']
            }))

    async def send_add_user_front(self, position, username):
        print('add signal sent')
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'add_user',
                'position': position,
                'username': username
            })

    async def add_user(self, event):
        await self.send(text_data=json.dumps({
            'message': 'add_user',
            'position': event['position'],
            'username': event['username']
        }))