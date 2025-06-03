from aiortc import RTCPeerConnection, RTCSessionDescription, RTCIceCandidate
import json

def create_peer_connection():
    pc = RTCPeerConnection()
    return pc

async def handle_sdp_offer(pc, offer):
    await pc.setRemoteDescription(RTCSessionDescription(sdp=offer["sdp"], type=offer["type"]))
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    return {
        "sdp": pc.localDescription.sdp,
        "type": pc.localDescription.type
    }

async def handle_sdp_answer(pc, answer):
    await pc.setRemoteDescription(RTCSessionDescription(sdp=answer["sdp"], type=answer["type"]))
