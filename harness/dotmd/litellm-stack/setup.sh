#!/usr/bin/env bash
# LiteLLM stack setup — bash/Mac/Linux/WSL.
cd "$(dirname "$0")" || exit 1
PY="$(command -v python3 || command -v python)"
if [ -z "$PY" ]; then
  echo "Python not found on PATH. Install it, then re-run."
  exit 1
fi
exec "$PY" setup.py
