from dataclasses import dataclass, field

from fastapi import WebSocket


@dataclass
class WebSocketManager:
    clients: list[WebSocket] = field(default_factory=list)

    async def broadcast_number(self, number: int):
        for client in self.clients:
            await client.send_text(str(number))

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.clients.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.clients.remove(websocket)
