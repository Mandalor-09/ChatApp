from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.exceptions import StopConsumer
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async,async_to_sync
from django.db import models
from app.models import Group,Messages
import json


class Myconsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user1 = self.scope['url_route']['kwargs']['user1']
        user2 = self.scope['url_route']['kwargs']['user2']
        print(user1, user2, 'Users are ::')

        # Use sync_to_async to retrieve users from the database
        user1_obj = await sync_to_async(User.objects.get)(username=user1)
        user1 = user1_obj.id
        name1 = user1_obj.username
        # print(user1_obj,user1,name1,'<<<<<<<>>>')
        user2_obj = await sync_to_async(User.objects.get)(id=user2)
        user2 = user2_obj.id
        name2 = user2_obj.username

        # Generate the group name based on the user names
        name = f"{name1}{name2}"
        name1 = f"{name2}{name1}"
        # print(name, '<<>>>>>><<>>><<<<<<<>')
        group = None
        try:
            group = await sync_to_async(Group.objects.get)(
                models.Q(name=name,user1=user1_obj, user2=user2_obj) | models.Q(name=name1,user1=user2_obj, user2=user1_obj))
        except Exception as e:
            print(e)

        # print(group,'<<<<<<<<<<<<<>>>>>>')
        # If the group doesn't exist, create a new one
        if group is None:
            group = await sync_to_async(Group.objects.create)(
                name=name, user1=user1_obj, user2=user2_obj
            )
            print('created group',group)
            self.group_name = group.name
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.channel_layer.group_add(self.group_name, name1)
            await self.channel_layer.group_add(self.group_name, name2)
            await self.accept()

        else:
            group = await sync_to_async(Group.objects.get)(
                models.Q(name=name,user1=user1_obj, user2=user2_obj) | models.Q(name=name1,user1=user2_obj, user2=user1_obj))
            print('retrive group',group)
            # Add the user and the group to the channel layer
            self.group_name = group.name
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.channel_layer.group_add(self.group_name, name1)
            await self.channel_layer.group_add(self.group_name, name2)
            await self.accept()


        

    async def receive_json(self, content, **kwargs):
        print(content, content['message'])
        # print(self.group_name,'<<<<<<<<<<<<>>>>>>>>>>>>>')
        user1 = self.scope['url_route']['kwargs']['user1']
        # print('recive user1 in recieve',user1)
        sender = await sync_to_async(User.objects.get)(username=user1)
        # print('sender',sender)
        group = await sync_to_async(Group.objects.get)(name=self.group_name)
        # print('group',group)
        store_msg = await sync_to_async(Messages.objects.create)(group=group,content=content['message'],user=sender)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "message": content['message'],
            }
        )

    
    async def chat_message(self, event):
        
        await self.send_json({
            "message":  event['message'],
        })
        print('send2')

    async def disconnect(self, code):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        raise StopConsumer()
