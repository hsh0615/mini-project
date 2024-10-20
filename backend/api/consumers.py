# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Attempting to connect...")
        print(f"[DEBUG] Scope: {self.scope}")  # 输出 scope
        self.match_id = self.scope['url_route']['kwargs']['match_id']  # 确保使用 match_id
        self.room_group_name = f"chat_{self.match_id}"

        # 加入房间组
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print("WebSocket connection established.")


    async def disconnect(self, close_code):
        # 离开房间组
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print(f"[DEBUG] Received message: {text_data}")
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        username = text_data_json.get('username')  # 获取用户名

        # 检查用户名是否获取成功
        if username is None:
            username = 'Unknown'  # 或者设置为其他默认值

        # 发送消息到房间组
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event.get('username', 'Unknown')

        # 发送消息到 WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))
