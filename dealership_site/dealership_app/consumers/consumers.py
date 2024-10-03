import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class CarPostConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            'car_notifications',
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            'car_notifications',
            self.channel_name
        )

    def car_posted(self, event):
        car_data = event['car_data']
        self.send(text_data=json.dumps({
            'car_data': car_data
        }))
