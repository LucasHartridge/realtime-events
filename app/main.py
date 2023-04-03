import time
from typing import List
import asyncio
from fastapi import (
    Depends,
    FastAPI,
    WebSocket,
    WebSocketDisconnect, 
    WebSocketException,
)
from fastapi.responses import HTMLResponse
from app.client import html
from app.settings import settings
from app.dependencies.authorization import authorize
from app.services.kafka_service import Kafka
import contextvars

app = FastAPI(
    debug=True,
    title="Realtime Insights",
    description="Real time websocket API",
    version="0.0.1",
    docs_url="/docs",
)


@app.get("/")
async def get():
    return HTMLResponse(html)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"Active connections {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_text_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_personal_json_message(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


managerEvents = ConnectionManager()
kafka = Kafka()

global_consumer = contextvars.ContextVar(
    "consumer", default=kafka.get_consumer()
)


@app.websocket("/getEvents/{channel}")
async def get_events(websocket: WebSocket, channel: str, organization_id: str = Depends(authorize)):
    await managerEvents.connect(websocket)
    await asyncio.wait_for(websocket.send_json({'type': 'ping'}), settings.HEART_BEAT_INTERVAL)

    START_TIME = time.time()

    try:
        print(f"Read events for organization id {organization_id} and channel {channel}")
        while True:
            if int(time.time() - START_TIME) >= settings.PING_INTERVAL:
                await asyncio.wait_for(websocket.send_json({'type': 'ping'}), settings.HEART_BEAT_INTERVAL)
                START_TIME = time.time()

            msg = global_consumer.get().poll(1.0)
            if msg is None:
                print("No message")
                continue
            elif msg.error():
                print(f'error: {msg.error}')
            else:
                # Check if the subscribed topic
                topic = msg.topic()
                print(f"Message from topic {topic}. Channel subscribed to {channel}")
                if topic == settings.TOPICS[channel]:
                    message = kafka.deserialize_key(topic, msg)
                    print(f"Message {message} from topic {topic}")
                    if message["organization_id"] == organization_id:
                        await managerEvents.send_personal_json_message({"type": "event", "channel": channel}, websocket)
    except (WebSocketDisconnect, WebSocketException, TimeoutError, Exception) as exception:
        managerEvents.disconnect(websocket)
        print(f"The following exception was raised: {str(exception)}")
