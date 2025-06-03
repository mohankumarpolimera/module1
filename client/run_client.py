import asyncio
import websockets
import json
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer
from shared.rtc_utils import create_peer_connection, handle_sdp_offer
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


async def run_client():
    session_id = input("Enter session ID: ")
    SIGNALING_SERVER = f"ws://localhost:8000/ws/{session_id}/client"

    pc = create_peer_connection()

    player = MediaPlayer(None)  # Uses default webcam and mic
    if player.audio:
        pc.addTrack(player.audio)
    if player.video:
        pc.addTrack(player.video)

    async with websockets.connect(SIGNALING_SERVER) as ws:
        print("Client connected to signaling server.")

        async def receive():
            async for message in ws:
                data = json.loads(message)
                if data["type"] == "offer":
                    print("Received offer.")
                    answer = await handle_sdp_offer(pc, data)
                    await ws.send(json.dumps(answer))
                elif data["type"] == "control":
                    print(f"[CONTROL] {data['action']} received.")

        await receive()

if __name__ == "__main__":
    asyncio.run(run_client())
