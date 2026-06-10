from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Safely replace text in a UTF-8 file without relying on shell codepages."
    )
    parser.add_argument("file", help="Target file path")
    parser.add_argument("old", help="Text to replace")
    parser.add_argument("new", help="Replacement text")
    parser.add_argument(
        "--count",
        type=int,
        default=-1,
        help="Maximum replacements; default replaces all",
    )
    args = parser.parse_args()

    path = Path(args.file)
    text = path.read_text(encoding="utf-8", errors="strict")
    if args.old not in text:
        raise SystemExit(f"Pattern not found: {args.old!r}")

    replaced = text.replace(args.old, args.new, args.count if args.count >= 0 else text.count(args.old))
    path.write_text(replaced, encoding="utf-8", newline="\n")
    print(f"Updated {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
