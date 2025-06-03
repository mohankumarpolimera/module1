from fastapi import WebSocket, WebSocketDisconnect
from .uuid_pairing import join_session, leave_session, get_peer, is_valid_session

async def signaling_handler(websocket: WebSocket, session_id: str, role: str):
    await websocket.accept()

    if not is_valid_session(session_id) or not join_session(session_id, role, websocket):
        await websocket.close()
        return

    try:
        while True:
            message = await websocket.receive_text()
            peer_ws = get_peer(session_id, role)
            if peer_ws:
                await peer_ws.send_text(message)
    except WebSocketDisconnect:
        leave_session(session_id, role)
