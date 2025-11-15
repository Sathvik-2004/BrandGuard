from typing import List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        # send to all clients (ignore send errors)
        to_remove = []
        for conn in list(self.active_connections):
            try:
                await conn.send_text(message)
            except Exception:
                # mark to remove if connection broken
                to_remove.append(conn)
        for c in to_remove:
            self.disconnect(c)