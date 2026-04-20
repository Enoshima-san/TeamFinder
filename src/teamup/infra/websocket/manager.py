from uuid import UUID

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self._connections: dict[UUID, list[WebSocket]] = {}

    async def add_connection(self, websocket: WebSocket, conversation_id: UUID):
        """Подключаем сокет к комнате диалога."""
        if conversation_id not in self._connections:
            self._connections[conversation_id] = []
        self._connections[conversation_id].append(websocket)

    def remove_connection(self, websocket: WebSocket, conversation_id: UUID):
        """Отключаем сокет от комнаты. Если комната пуста — удаляем её."""
        if conversation_id not in self._connections:
            return
        if websocket in self._connections[conversation_id]:
            self._connections[conversation_id].remove(websocket)
        # Читстка пустых подключений
        if not self._connections[conversation_id]:
            del self._connections[conversation_id]

    async def broadcast(self, conversation_id: UUID, message: dict):
        if conversation_id not in self._connections:
            return
        connections = self._connections[conversation_id].copy()
        for ws in connections:
            try:
                await ws.send_json(message)
            except Exception:
                self.remove_connection(ws, conversation_id)


manager = ConnectionManager()
