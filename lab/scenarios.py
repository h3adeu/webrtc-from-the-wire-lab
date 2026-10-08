"""採取シナリオ。各々が aiortc 接続を確立し、指定秒トラフィックを流す。
loopback を最初に import して 127.0.0.1 限定を効かせること。"""
import asyncio

import loopback  # noqa: F401  # import 副作用で 127.0.0.1 限定を適用
from aiortc import RTCPeerConnection

from signaling import connect
from tracks import ColorVideoTrack, ToneTrack


async def scenario_datachannel(duration: float) -> None:
    """STUN/DTLS/SCTP(DCEP+データ) を生む。"""
    pc1, pc2 = RTCPeerConnection(), RTCPeerConnection()
    ch = pc1.createDataChannel("chat")

    @ch.on("open")
    def _() -> None:
        ch.send("hello from lab")

    await connect(pc1, pc2)
    await asyncio.sleep(duration)
    await pc1.close()
    await pc2.close()


async def scenario_media(duration: float) -> None:
    """STUN/DTLS/SRTP/RTCP を生む（音声+映像）。"""
    pc1, pc2 = RTCPeerConnection(), RTCPeerConnection()
    pc1.addTrack(ToneTrack())
    pc1.addTrack(ColorVideoTrack())

    @pc2.on("track")
    def on_track(track) -> None:
        async def drain() -> None:
            try:
                while True:
                    await track.recv()
            except Exception:
                pass
        asyncio.ensure_future(drain())

    await connect(pc1, pc2)
    await asyncio.sleep(duration)
    await pc1.close()
    await pc2.close()


SCENARIOS = {
    "datachannel": scenario_datachannel,
    "media": scenario_media,
}
