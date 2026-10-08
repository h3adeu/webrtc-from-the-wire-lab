#!/bin/bash
# 使い方: bash capture.sh <scenario> <seconds>
# lo0 を tcpdump で包んで lab/captures/<scenario>.pcap を出力する。
set -e
SCEN="${1:?scenario}"; SECS="${2:-5}"
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/captures/${SCEN}.pcap"
mkdir -p "$HERE/captures"

# 採取（127.0.0.1 のみ。tcpdump を先に起こしてから走らせる）
tcpdump -i lo0 -w "$OUT" 'udp and host 127.0.0.1' >/dev/null 2>&1 &
CAP=$!
sleep 1
( cd "$HERE" && uv run --no-project --isolated --with-requirements requirements.txt \
    python run.py "$SCEN" "$SECS" )
sleep 1
kill "$CAP" 2>/dev/null || true
wait "$CAP" 2>/dev/null || true
echo "captured -> $OUT"
