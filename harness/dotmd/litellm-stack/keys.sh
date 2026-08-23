#!/usr/bin/env bash
# keys — virtual key + budget management.  Try: keys list
cd "$(dirname "$0")" || exit 1
PY="$(command -v python3 || command -v python)"
if [ -z "$PY" ]; then
  echo "Python not found on PATH."
  exit 1
fi
exec "$PY" keys.py "$@"
