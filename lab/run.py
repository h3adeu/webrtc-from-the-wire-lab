"""使い方: python run.py <scenario> <duration_sec>"""
import asyncio
import sys

from scenarios import SCENARIOS


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] not in SCENARIOS:
        print(f"usage: python run.py [{'|'.join(SCENARIOS)}] <seconds>", file=sys.stderr)
        raise SystemExit(2)
    name, duration = sys.argv[1], float(sys.argv[2])
    asyncio.run(SCENARIOS[name](duration))
    print(f"DONE {name} {duration}s")


if __name__ == "__main__":
    main()
