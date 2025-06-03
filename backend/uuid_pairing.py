from uuid import uuid4

# In-memory session store: { session_id: {"viewer": WebSocket, "client": WebSocket} }
sessions = {}

def create_session():
    session_id = str(uuid4())
    sessions[session_id] = {"viewer": None, "client": None}
    return session_id

def join_session(session_id: str, role: str, websocket):
    if session_id not in sessions:
        return False
    sessions[session_id][role] = websocket
    return True

def get_peer(session_id: str, role: str):
    peer = "viewer" if role == "client" else "client"
    return sessions[session_id].get(peer)

def leave_session(session_id: str, role: str):
    if session_id in sessions:
        sessions[session_id][role] = None

def is_valid_session(session_id: str):
    return session_id in sessions
