from channels.generic.websocket import AsyncWebsocketConsumer
import json

class TaskCompletionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.task_group_name = f'task_{self.task_id}'

        # Join task group
        await self.channel_layer.group_add(
            self.task_group_name,
            self.channel_name
        )

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
