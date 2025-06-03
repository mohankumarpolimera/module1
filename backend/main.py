from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from .uuid_pairing import create_session
from .signaling import signaling_handler

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/create_session")
def api_create_session():
    session_id = create_session()
    return {"session_id": session_id}

@app.websocket("/ws/{session_id}/{role}")
async def websocket_endpoint(websocket: WebSocket, session_id: str, role: str):
    await signaling_handler(websocket, session_id, role)
