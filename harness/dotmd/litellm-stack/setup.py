#!/usr/bin/env python3
"""
setup.py — bring the whole LiteLLM stack up with zero decisions.

What it does:
  1. Creates .env from .env.example with FRESH random master + salt keys
     (skipped if .env already exists — your keys stay yours).
  2. Starts the containers: docker compose up -d
  3. Waits for the gateway to answer, prints your login, opens the Admin UI.

Run it by double-clicking setup.cmd (Windows) or `bash setup.sh`.
"""

import os
import secrets
import shutil
import subprocess
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(ROOT, ".env")
EXAMPLE = os.path.join(ROOT, ".env.example")
UI_URL = "http://localhost:4000/ui"


def banner(msg):
    print("\n=== " + msg + " ===")


def check_docker():
    if shutil.which("docker") is None:
        sys.exit("Docker not found on PATH. Install Docker Desktop, start it, then re-run setup.")
    try:
        subprocess.run(["docker", "info"], capture_output=True, check=True, timeout=15)
    except (subprocess.CalledProcessError, OSError):
        sys.exit("Docker is installed but not running. Start Docker Desktop, wait for it to be ready, then re-run setup.")
    try:
        subprocess.run(["docker", "compose", "version"], capture_output=True, check=True, timeout=15)
    except (subprocess.CalledProcessError, OSError):
        sys.exit("`docker compose` not available. Update Docker Desktop (Compose v2 is built in).")


def make_env():
    if not os.path.exists(EXAMPLE):
        sys.exit("Missing .env.example next to this script.")
    if os.path.exists(ENV_FILE):
        banner("Found existing .env — keeping it (and your keys)")
        return
    banner("Creating .env with fresh random keys")
    with open(EXAMPLE, encoding="utf-8") as fh:
        content = fh.read()
    content = content.replace("LITELLM_MASTER_KEY=sk-1234",
                              "LITELLM_MASTER_KEY=sk-" + secrets.token_hex(32))
    content = content.replace("LITELLM_SALT_KEY=sk-XXXXXXXXXXXXXXXX",
                              "LITELLM_SALT_KEY=sk-" + secrets.token_hex(32))
    with open(ENV_FILE, "w", encoding="utf-8") as fh:
        fh.write(content)
    print("Wrote %s" % ENV_FILE)
    print("  LITELLM_MASTER_KEY is your Admin UI password and your admin API key.")
    print("  LITELLM_SALT_KEY encrypts provider keys in the DB. Never change it.")


def master_key_from_env():
    with open(ENV_FILE, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line.startswith("LITELLM_MASTER_KEY="):
                return line.split("=", 1)[1].strip().strip("\"'")
    return ""


def start_stack():
    banner("Starting containers (first run pulls images — takes a few minutes)")
    subprocess.run(["docker", "compose", "up", "-d"], cwd=ROOT, check=True)


def wait_for_gateway(timeout=120):
    print("Waiting for gateway at http://localhost:4000 ...", flush=True)
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen("http://localhost:4000/health/liveliness", timeout=3) as resp:
                if resp.status == 200:
                    print("Gateway is up.")
                    return True
        except Exception:
            pass
        time.sleep(2)
    return False


def main():
    banner("LiteLLM stack setup")
    check_docker()
    make_env()
    start_stack()

    if wait_for_gateway():
        key = master_key_from_env()
        print()
        print("Admin UI : " + UI_URL)
        print("Login    : admin / %s" % (key or "(see LITELLM_MASTER_KEY in .env)"))
        print("Endpoint : http://localhost:4000  (OpenAI-compatible /v1)")
        print("Keys     : python keys.py list | create <alias> <budget_usd> | spend")
        print()
        print("Next: mint your first virtual key in the UI, or:")
        print("  python keys.py create test 5")
        if sys.platform.startswith("win"):
            try:
                os.startfile(UI_URL)  # noqa: S606 — user ran this script on purpose
            except Exception:
                pass
    else:
        print("Gateway not healthy yet. Check logs:  docker compose logs litellm")


if __name__ == "__main__":
    main()
