"""Probe API readiness without requiring curl or shell expressions."""

import json
import os
import sys
from urllib.request import urlopen


def main() -> int:
    try:
        port = int(os.getenv("PORT", "8000"))
        with urlopen(f"http://127.0.0.1:{port}/ready", timeout=10) as response:
            if response.status == 200 and json.load(response)["status"] == "ready":
                return 0
    except Exception:
        pass
    print("API not ready", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
