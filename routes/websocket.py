from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.notifier import manager

router = APIRouter()

@router.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):

    print("🔥 WEBSOCKET ROUTE HIT")

    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            print("Received:", data)

    except WebSocketDisconnect:
        print("❌ WebSocket disconnected")
        manager.disconnect(websocket)