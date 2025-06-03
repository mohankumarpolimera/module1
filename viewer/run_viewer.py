import asyncio
import websockets
import json
from aiortc.contrib.media import MediaRecorder
from shared.rtc_utils import create_peer_connection
from aiortc import RTCSessionDescription
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

async def run_viewer():
    session_id = input("Enter session ID: ")
    SIGNALING_SERVER = f"ws://localhost:8000/ws/{session_id}/viewer"

    pc = create_peer_connection()

    recorder = MediaRecorder("viewer_output.mp4")
    pc.on("track", recorder.addTrack)

    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)

    async with websockets.connect(SIGNALING_SERVER) as ws:
        print("Viewer connected to signaling server.")

        # Send offer
        await ws.send(json.dumps({
            "sdp": pc.localDescription.sdp,
            "type": pc.localDescription.type
        }))

        async def receive():
            async for message in ws:
                data = json.loads(message)
                if data["type"] == "answer":
                    await pc.setRemoteDescription(
                        RTCSessionDescription(sdp=data["sdp"], type=data["type"])
                    )
                    print("Received answer. Connection established.")

        async def send_controls():
            while True:
                cmd = input("Send control (mute_cam / mute_mic / mute_speaker): ")
                await ws.send(json.dumps({"type": "control", "action": cmd}))

        await asyncio.gather(receive(), send_controls())

if __name__ == "__main__":
    asyncio.run(run_viewer())
