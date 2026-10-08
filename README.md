# webrtc-from-the-wire-lab

書籍『WebRTCをワイヤから読む』（艶雨）の実測ラボです。
本書に載せたバイト列やコマンドの出力は、ここにあるキャプチャから起こしています。

## 入っているもの

| パス | 内容 |
|---|---|
| `lab/captures/datachannel.pcap` | データチャネル1本の接続（STUN、DTLS、DTLS に包まれた SCTP） |
| `lab/captures/media.pcap` | 音声と映像の接続（STUN、DTLS、SRTP、SRTCP） |
| `lab/*.py`・`lab/capture.sh` | 上の2つを採り直すためのスクリプト |

本書の「`lab/captures/media.pcap` で確かめる」といった記述は、このリポジトリを clone した直下からのパスです。

```sh
git clone https://github.com/h3adeu/webrtc-from-the-wire-lab.git
cd webrtc-from-the-wire-lab
tshark -r lab/captures/datachannel.pcap      # Wireshark で開いてもよい
```

## キャプチャの採り方

aiortc 1.14.0 の2つのピアを1つのプロセスで直結し、ICE の候補を 127.0.0.1 だけに絞って、すべての通信をループバックに流しています。
そのため、キャプチャに写っているアドレスは 127.0.0.1 だけです。

採り直すには、次のものが要ります。

- [uv](https://docs.astral.sh/uv/)（Python と依存パッケージを自動で用意する）
- `tcpdump` と `tshark`（Wireshark に含まれる）

```sh
bash lab/capture.sh datachannel 4   # → lab/captures/datachannel.pcap
bash lab/capture.sh media 5         # → lab/captures/media.pcap
```

`capture.sh` は macOS のループバック（`lo0`）を前提にしています。
Linux では、`capture.sh` の `-i lo0` を `-i lo` に変えてください。
ループバックのキャプチャに管理者権限が要る環境では、`sudo` を付けて実行します。

採り直したキャプチャに、期待するパケットが入っているかは次で確かめられます。

```sh
uv run --no-project --with-requirements lab/requirements.txt \
  python lab/verify.py lab/captures/datachannel.pcap stun=2 dtls=2
```

採り直すと、ポート番号、SSRC、乱数などは本書の値と変わります。
本書と同じ値で読みたいときは、同梱のキャプチャを使ってください。

## 暗号化された中身について

SRTP（メディア）と、DTLS に包まれた SCTP（データチャネル）は暗号化されています。
aiortc 1.14.0 は環境変数 `SSLKEYLOGFILE` を読まないので、同梱のキャプチャは鍵なしで、暗号化された部分は復号できません。
鍵なしで何が読めて何が読めないかは、本書の各章で扱っています。

## ファイル

| ファイル | 役割 |
|---|---|
| `lab/loopback.py` | aioice の候補収集を 127.0.0.1 だけに絞る（import するだけで効く） |
| `lab/signaling.py` | 2つのピアを同じプロセスの中で Offer/Answer 直結する |
| `lab/tracks.py` | 外部ファイルを使わない合成の音声（正弦波）と映像（単色） |
| `lab/scenarios.py` | 採取シナリオ（`datachannel` と `media`） |
| `lab/run.py` | シナリオを指定秒数だけ動かす |
| `lab/capture.sh` | tcpdump を起動してからシナリオを動かし、pcap に保存する |
| `lab/verify.py` | pcap に STUN・DTLS・メディアが何件あるかを確かめる |

## ライセンス

MIT License（`LICENSE`）。キャプチャ（`.pcap`）も同じ条件で使えます。
