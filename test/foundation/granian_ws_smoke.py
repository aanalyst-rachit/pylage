import asyncio
import websockets

async def main():
    async with websockets.connect("ws://127.0.0.1:8766/"):
        print("WS CONNECTED")

asyncio.run(main())
