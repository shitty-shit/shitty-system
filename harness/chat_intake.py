#!/usr/bin/env python3
"""
Harness wrapper for chat_intake.py located in D:\SHITTYSHIT\00_MASTER\conversations\chat_intake.py
"""
import sys
from pathlib import Path

TARGET = Path(r"D:\SHITTYSHIT\00_MASTER\conversations\chat_intake.py")

if __name__ == "__main__":
    if TARGET.exists():
        import runpy
        sys.path.insert(0, str(TARGET.parent))
        runpy.run_path(str(TARGET), run_name="__main__")
    else:
        print(f"[!] Target not found: {TARGET}", file=sys.stderr)
        sys.exit(1)
