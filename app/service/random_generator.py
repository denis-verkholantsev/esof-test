from dataclasses import dataclass
from app.service.websocket_manager import WebSocketManager
import random
import asyncio

@dataclass
class RandomNumberGenerator:
    websocket_manager: WebSocketManager
    number: int = 0

    async def generate_numbers(self):
        while True:
            self.number = random.randint(1, 100)
            await self.websocket_manager.broadcast_number(self.number)
            await asyncio.sleep(5)

    def get_number(self) -> int:
        return self.number
