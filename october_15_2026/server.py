import asyncio
import websockets
import sys

connected_clients = set()

async def handler(websocket):
    connected_clients.add(websocket)
    print("New client connected", flush=True)

    try:
        await websocket.send("Welcome to the Distributed Systems WebSocket server in Python!")

        async for message in websocket:
            print(f"Message received: {message}", flush=True)

            disconnected = set()
            for client in connected_clients:
                try:
                    await client.send(f"Server says: {message}")
                except websockets.ConnectionClosed:
                    disconnected.add(client)

            connected_clients.difference_update(disconnected)

    except websockets.ConnectionClosed:
        print("Client disconnected", flush=True)

    finally:
        connected_clients.discard(websocket)

async def main():
    print("Starting Distributed Systems WebSocket server at ws://0.0.0.0:8080", flush=True)
    async with websockets.serve(handler, "0.0.0.0", 8080):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
