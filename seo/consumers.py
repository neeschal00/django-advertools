from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache

import json


class TaskCompletionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.random_id = self.scope["url_route"]["kwargs"]["random_id"]
        self.task_group_name = f"group_{self.random_id}"

        # Join task group
        await self.channel_layer.group_add(self.task_group_name, self.channel_name)
        # cache.set(self.random_id, self.task_group_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave task group
        await self.channel_layer.group_discard(self.task_group_name, self.channel_name)

    # Receive message from task worker
    async def task_completed(self, event):
        result = event["result"]

        # Send task completion notification to the client
        await self.send(
            text_data=json.dumps({"type": "task_completed", "result": result})
        )

    async def task_started(self, event):
        start = event["start"]

        # Send task completion notification to the client
        await self.send(text_data=json.dumps({"type": "task_started", "start": start}))

    async def data_converted(self, event):
        result = event["result"]

        # Send task completion notification to the client
        await self.send(
            text_data=json.dumps({"type": "data_converted", "result": result})
        )

    async def conversion_failed(self, event):
        # result = event['result']

        # Send task completion notification to the client
        await self.send(
            text_data=json.dumps(
                {"type": "conversion_failed", "result": "Unable to process the dataset"}
            )
        )

    async def report_failed(self, event):
        # result = event['result']

        # Send task completion notification to the client
        await self.send(
            text_data=json.dumps(
                {"type": "report_failed", "result": "Unable to create report"}
            )
        )

    async def crawlRead(self, event):
        task_id = event["task_id"]

        # Send task completion notification to the client
        await self.send(
            text_data=json.dumps(
                {"type": "crawlRead", "result": "Read crawled file", "task_id": task_id}
            )
        )

    async def analysisComplete(self, event):
        task_id = event["task_id"]
        task_name = event["task_name"]
        

        await self.send(
            text_data=json.dumps(
                {
                    "type": "analysisComplete",
                    "result": "Sub analysis complete",
                    "task_id": task_id,
                    "task_name": task_name,
                }
            )
        )
    
    async def getKeywords(self, event):
        task_id = event["task_id"]

        # Send task completion notification to the client
        await self.send(
            text_data=json.dumps(
                {"type": "getKeywords", "result": "Keywords completed", "task_id": task_id}
            )
        )
