import asyncio
import threading
import http.server
import socketserver
import websockets
import json
from datetime import datetime

# ----- HTTP SERVER (runs in separate thread) -----
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.path = "/Proje.html"  # Redirect to Proje.html
        return super().do_GET()

def start_http_server():
    PORT = 8000
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"HTTP server running at http://localhost:{PORT}")  # Start HTTP server
        httpd.serve_forever()

# ----- WEBSOCKET SERVER -----
connected = set()  # Track connected clients
chat_log = []  # Store chat history in memory

async def ws_handler(websocket):
    connected.add(websocket)  # Add new client
    print(f"New client connected - Total: {len(connected)}")  # Log connection

    try:
        # Send chat history to new client
        for msg in chat_log:
            await websocket.send(json.dumps(msg))

        async for message in websocket:
            data = json.loads(message)
            if 'username' in data and 'message' in data:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get timestamp
                message_data = {
                    'username': data['username'],
                    'message': data['message'],
                    'time': timestamp
                }

                # Save to memory and file
                chat_log.append(message_data)
                with open("chat_history.txt", "a", encoding="utf-8") as f:
                    f.write(json.dumps(message_data) + "\n")  # Write to file

                # Broadcast to all clients
                for conn in list(connected):
                    try:
                        await conn.send(json.dumps(message_data))  # Send message
                    except websockets.exceptions.ConnectionClosed:
                        connected.remove(conn)  # Remove disconnected client

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected.remove(websocket)  # Remove client
        print(f"Client disconnected - Remaining: {len(connected)}")  # Log disconnection

async def start_ws_server():
    async with websockets.serve(lambda ws: ws_handler(ws), "localhost", 8765):
        print("WebSocket server running at ws://localhost:8765")
        await asyncio.Future()  # run forever


# ----- START BOTH -----
if __name__ == "__main__":
    # Start HTTP server in background thread
    threading.Thread(target=start_http_server, daemon=True).start()
    
    # Start WebSocket server in main asyncio loop
    asyncio.run(start_ws_server())