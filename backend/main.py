# backend/main.py
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from .ai_logic import generate_response

app = FastAPI()

# Разрешим доступ с фронта
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # для dev-режима
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        user_msg = await websocket.receive_text()
        reply = generate_response(user_msg)
        await websocket.send_text(reply)
