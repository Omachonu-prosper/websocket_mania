from fastapi import FastAPI, WebSocket, WebSocketDisconnect


app = FastAPI()


class WSManager():
    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket, client_id: int) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)
        await self.broadcast(f"{client_id}, joined", websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket) -> None:
        await websocket.send_text(message)

    async def broadcast(self, message: str, websocket: WebSocket):
        for connection in self.active_connections:
            if connection != websocket:
                await connection.send_text(message)
    

ws_manager = WSManager()


@app.websocket('/ws/{client_id}')
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await ws_manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            await ws_manager.send_personal_message(f"you: {data}", websocket)
            await ws_manager.broadcast(f"{client_id}: {data}", websocket)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        ws_manager.broadcast(f"Client {client_id} left the chat", websocket)