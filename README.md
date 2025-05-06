Chat Server
Overview
Chat Server is a Python-based application that runs an HTTP server to serve a web interface and a WebSocket server for real-time chat. It supports multiple clients, stores chat history, and logs messages to a file.
Features

HTTP Server: Serves Proje.html at http://localhost:8000.
WebSocket Server: Handles real-time chat at ws://localhost:8765.
Chat History: Stores messages in memory and chat_history.txt.
Multi-Client: Broadcasts messages to all connected clients.
Timestamps: Adds timestamps to messages.

Requirements

Python 3.9+
Libraries:
websockets


Install dependencies: pip install websockets


Ensure Proje.html exists in the project directory.

Usage

Run the server:py PartB.py


Access the web interface:
Open http://localhost:8000 in a browser.


Connect to the WebSocket server:
Use a WebSocket client or the provided Proje.html interface.
Send messages in JSON format: {"username": "user", "message": "hello"}.


View chat history:
Messages are displayed in real-time and saved to chat_history.txt.



Notes

Firewall: Allow TCP port 8000 and 8765.netsh advfirewall firewall add rule name="Chat Server" dir=in action=allow protocol=TCP localport=8000,8765


Client Implementation: Ensure Proje.html includes WebSocket logic to connect to ws://localhost:8765.
Logs: Messages are appended to chat_history.txt in JSON format.

Troubleshooting

Port Conflicts: Check ports with netstat -ano | findstr 8000 or 8765.
Connection Issues: Verify Proje.html is in the correct directory.
WebSocket Errors: Ensure client sends valid JSON.

