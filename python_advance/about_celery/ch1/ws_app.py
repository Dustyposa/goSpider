from fastapi import WebSocket, FastAPI
import uvicorn

from tasks import send_ws, add

app = FastAPI()


@app.websocket("/ws")
async def ws_t(websocket: WebSocket) -> None:
    await websocket.accept()
    for i in range(4):
        send_ws.delay(websocket, f"this is {i} msg")

if __name__ == '__main__':
    uvicorn.run(app, reload=True)
