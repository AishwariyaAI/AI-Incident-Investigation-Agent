from fastapi import WebSocket

class ConnectionManager:

    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()

        self.active_connections.append(websocket)

        print("✅ Client connected")
        print("Connections:", len(self.active_connections))

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

        print("❌ Client disconnected")

    async def send_alert(self, message):

        print("🔥 SEND_ALERT CALLED")
        print(message)

        print("Connections:", len(self.active_connections))

        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()