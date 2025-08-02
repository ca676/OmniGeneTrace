from fastapi import FastAPI, WebSocket
import cv2, numpy as np, asyncio, base64
from ai_engine import process_8k_frame

app = FastAPI()
clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            image_bytes = base64.b64decode(data)
            nparr = np.frombuffer(image_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            processed_frame = process_8k_frame(frame)
            _, buffer = cv2.imencode('.jpg', processed_frame)
            img_str = base64.b64encode(buffer).decode('utf-8')
            await asyncio.gather(*[client.send_text(img_str) for client in clients])
    except:
        clients.remove(websocket)
