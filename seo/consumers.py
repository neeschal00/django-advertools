from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache

import json

class TaskCompletionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.random_id = self.scope['url_route']['kwargs']['random_id']
        self.task_group_name = f'group_{self.random_id}'

        # Join task group
        await self.channel_layer.group_add(
            self.task_group_name,
            self.channel_name
        )
        # cache.set(self.random_id, self.task_group_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave task group
        await self.channel_layer.group_discard(
            self.task_group_name,
            self.channel_name
        )

    # Receive message from task worker
    async def task_completed(self, event):
        result = event['result']

        # Send task completion notification to the client
        await self.send(text_data=json.dumps({
            'result': result
        }))
    
    async def task_started(self, event):
        start = event['start']

        # Send task completion notification to the client
        await self.send(text_data=json.dumps({
            'start': start
        }))

    async def data_converted(self, event):
        result = event['result']

        # Send task completion notification to the client
        await self.send(text_data=json.dumps({
            'result': result
        }))
    
    async def conversion_failed(self, event):
        # result = event['result']

        # Send task completion notification to the client
        await self.send(text_data=json.dumps({
            'result': "Unable to process the dataset"
        }))