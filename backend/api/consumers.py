# api/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MatchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """當使用者連接 WebSocket 時執行"""
        self.username = self.scope['query_string'].decode('utf-8').split('=')[1]
        await self.channel_layer.group_add("matching_pool", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """當使用者斷開 WebSocket 時執行"""
        await self.channel_layer.group_discard("matching_pool", self.channel_name)

    async def receive(self, text_data):
        """當 WebSocket 接收到訊息時執行"""
        data = json.loads(text_data)

        if data.get('action') == 'match':
            await self.channel_layer.group_send(
                "matching_pool",
                {
                    'type': 'match.message',
                    'message': f"{self.username} is looking for a match!",
                }
            )

    async def match_message(self, event):
        """當配對訊息被傳送時執行"""
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))
