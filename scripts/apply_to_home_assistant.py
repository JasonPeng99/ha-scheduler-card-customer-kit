from __future__ import annotations

import gzip
import json
import shutil
import sys
import time
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/apply_to_home_assistant.py /homeassistant")
        return 1

    root = Path(sys.argv[1])
    card_js = root / "www" / "community" / "scheduler-card" / "scheduler-card.js"
    card_gz = root / "www" / "community" / "scheduler-card" / "scheduler-card.js.gz"
    resources = root / ".storage" / "lovelace_resources"

    source_js = Path(__file__).resolve().parents[1] / "assets" / "scheduler-card.js"

    if not source_js.exists():
        raise FileNotFoundError(source_js)
    if not card_js.exists():
        raise FileNotFoundError(card_js)
    if not resources.exists():
        raise FileNotFoundError(resources)

    shutil.copy2(source_js, card_js)

    with card_js.open("rb") as src, gzip.open(card_gz, "wb") as dst:
        shutil.copyfileobj(src, dst)

    data = json.loads(resources.read_text(encoding="utf-8"))
    items = data["data"]["items"]
    bumped = False
    version = f"cust{int(time.time())}"
    for item in items:
        url = item.get("url", "")
        if "/hacsfiles/scheduler-card/scheduler-card.js" in url:
            item["url"] = f"/hacsfiles/scheduler-card/scheduler-card.js?{version}"
            bumped = True
            break

    if not bumped:
        raise RuntimeError("scheduler-card resource entry not found in lovelace_resources")

    resources.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Applied patched scheduler-card bundle and bumped Lovelace resource version.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
