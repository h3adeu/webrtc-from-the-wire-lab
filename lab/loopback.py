"""aioice の host アドレス収集を 127.0.0.1 のみに固定する。
これで STUN/DTLS/SRTP/SCTP の全層が lo0・127.0.0.1 に集約され、
実IPを露出せず再現的に採取できる。import するだけで適用される。"""
import aioice.ice

# aioice は get_host_addresses(use_ipv4=..., use_ipv6=...) をキーワードで呼ぶ
aioice.ice.get_host_addresses = lambda **kw: ["127.0.0.1"]
