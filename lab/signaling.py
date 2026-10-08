"""2 つの RTCPeerConnection を、シグナリングサーバなしに直結する。
aiortc は setLocalDescription で ICE 収集完了まで待ち、候補を SDP に
同梱する（非Trickle）ので、localDescription をそのまま相手に渡せばよい。"""
from aiortc import RTCPeerConnection


async def connect(pc1: RTCPeerConnection, pc2: RTCPeerConnection) -> None:
    await pc1.setLocalDescription(await pc1.createOffer())
    await pc2.setRemoteDescription(pc1.localDescription)
    await pc2.setLocalDescription(await pc2.createAnswer())
    await pc1.setRemoteDescription(pc2.localDescription)
