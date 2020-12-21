from typing import Any

from celery import Celery
from fastapi import WebSocket

app = Celery('tasks', broker='pyamqp://guest:guest@127.0.0.1')


@app.anyio_task
async def send_ws(ws: WebSocket, msg: Any):
    print("send msg.....")
    await ws.send_text(msg)
    print("send msg success!!!!")


@app.anyio_task
def add(a, b):
    return a + b
