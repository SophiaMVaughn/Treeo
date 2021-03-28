import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from ReqAppt.models import *

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print()
    async def websocket_recieve(self, event):
        print()
    async def websocket_disconnect(self, event):
        print()