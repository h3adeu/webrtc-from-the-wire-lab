"""キャプチャ用の合成メディア。外部ファイル不要で実 RTP を生成する。
ToneTrack: 440Hz の正弦波(48kHz mono)、ColorVideoTrack: 320x240 の色面。"""
import asyncio
import fractions

import numpy as np
from av import AudioFrame, VideoFrame
from aiortc import MediaStreamTrack


class ToneTrack(MediaStreamTrack):
    kind = "audio"

    def __init__(self, freq: int = 440) -> None:
        super().__init__()
        self.freq = freq
        self.sample_rate = 48000
        self.samples_per_frame = 960  # 20ms
        self._n = 0

    async def recv(self) -> AudioFrame:
        await asyncio.sleep(0.02)
        t = (np.arange(self.samples_per_frame) + self._n) / self.sample_rate
        data = (0.2 * np.sin(2 * np.pi * self.freq * t) * 32767).astype(np.int16)
        frame = AudioFrame.from_ndarray(data.reshape(1, -1), format="s16", layout="mono")
        frame.sample_rate = self.sample_rate
        frame.pts = self._n
        frame.time_base = fractions.Fraction(1, self.sample_rate)
        self._n += self.samples_per_frame
        return frame


class ColorVideoTrack(MediaStreamTrack):
    kind = "video"

    def __init__(self) -> None:
        super().__init__()
        self._n = 0

    async def recv(self) -> VideoFrame:
        await asyncio.sleep(1 / 30)
        arr = np.zeros((240, 320, 3), dtype=np.uint8)
        arr[:, :, self._n % 3] = 255  # R→G→B を巡回
        frame = VideoFrame.from_ndarray(arr, format="rgb24")
        frame.pts = self._n
        frame.time_base = fractions.Fraction(1, 30)
        self._n += 1
        return frame
