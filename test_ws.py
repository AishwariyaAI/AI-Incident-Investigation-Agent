import asyncio
import websockets

async def test():
    uri = "ws://127.0.0.1:8001/api/v1/ws/alerts"

    async with websockets.connect(uri) as websocket:
        print("✅ Connected")

        while True:
            message = await websocket.recv()
            print("📩", message)

asyncio.run(test())