"""使い方: python verify.py <pcap> <type>=<min_count> [...]
type は stun / dtls / media（=STUN/DTLSでない127.0.0.1のUDP）。
各 type の出現数が min_count 以上なら PASS、足りなければ非0終了。"""
import subprocess
import sys


def count(pcap: str, kind: str) -> int:
    base = ["tshark", "-r", pcap, "-Y"]
    if kind == "stun":
        flt = "stun && ip.addr==127.0.0.1"
    elif kind == "dtls":
        flt = "dtls && ip.addr==127.0.0.1"
    elif kind == "media":
        flt = "udp && ip.addr==127.0.0.1 && !stun && !dtls"
    else:
        raise SystemExit(f"unknown type: {kind}")
    out = subprocess.run(base + [flt], capture_output=True, text=True)
    return sum(1 for line in out.stdout.splitlines() if line.strip())


def main() -> None:
    pcap, checks = sys.argv[1], sys.argv[2:]
    ok = True
    for chk in checks:
        kind, _, mn = chk.partition("=")
        got, need = count(pcap, kind), int(mn)
        mark = "OK" if got >= need else "NG"
        if got < need:
            ok = False
        print(f"  [{mark}] {kind}: {got} (>= {need})")
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
