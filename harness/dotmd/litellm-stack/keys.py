#!/usr/bin/env python3
"""
keys.py — one command for all LiteLLM virtual keys + budgets.

  python keys.py list                        every key: budget, spent, remaining
  python keys.py create <alias> <budget_usd> [model ...]   mint a budget-capped key
  python keys.py info <sk-...>               one key's spend/budget/models
  python keys.py spend [n]                   last n spend-log rows (default 10)
  python keys.py block <sk-...>              hard-stop a key right now
  python keys.py unblock <sk-...>            un-stop it
  python keys.py delete <sk-...>             delete a key

Master key is read from .env (LITELLM_MASTER_KEY). Endpoint overridable via
env var LITELLM_BASE_URL (default http://localhost:4000).

Mental model: provider keys are your credit cards (entered once, in .env or
the Admin UI). Virtual keys are per-project budget cards minted here — every
one gets its own spend total in the Admin UI and auto-429s at its budget.
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("LITELLM_BASE_URL", "http://localhost:4000").rstrip("/")


def die(msg, code=1):
    print("ERROR: " + msg, file=sys.stderr)
    sys.exit(code)


def master_key():
    env = os.path.join(ROOT, ".env")
    if not os.path.exists(env):
        die("no .env here — run setup first (setup.cmd / setup.sh)")
    for line in open(env, encoding="utf-8"):
        line = line.strip()
        if line.startswith("LITELLM_MASTER_KEY="):
            val = line.split("=", 1)[1].strip().strip("\"'")
            if val:
                return val
    die("LITELLM_MASTER_KEY is empty in .env")


def api(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method)
    req.add_header("Authorization", "Bearer " + master_key())
    data = None
    if body is not None:
        req.add_header("Content-Type", "application/json")
        data = json.dumps(body).encode("utf-8")
    try:
        with urllib.request.urlopen(req, data=data, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace").strip()
        die("API %s %s -> HTTP %s: %s" % (method, path, e.code, detail[:500]))
    except Exception as e:
        die("cannot reach %s (%s) — is the stack running? Run setup." % (BASE, e))


def money(x):
    try:
        return "$%.4f" % float(x or 0)
    except (TypeError, ValueError):
        return "-"


def norm(key):
    """/key/list returns flat dicts in some versions, {'info': {...}} in others."""
    info = key.get("info") if isinstance(key, dict) else None
    return info if isinstance(info, dict) else key


def cmd_list():
    raw = api("GET", "/key/list")
    # Newer LiteLLM returns {"keys": [<token hashes>]} — resolve each via
    # /key/info. Older versions return the key objects directly.
    if isinstance(raw, dict) and isinstance(raw.get("keys"), list):
        rows = []
        for h in raw["keys"]:
            try:
                out = api("GET", "/key/info?key=" + urllib.parse.quote(h))
                rows.append(norm(out))
            except SystemExit:
                continue
    else:
        rows = [norm(k) for k in (raw if isinstance(raw, list) else raw.get("data", []))]
    if not rows:
        print("No virtual keys yet. Mint one:  python keys.py create <alias> <budget_usd>")
        return
    hdr = "%-22s %-28s %9s %9s %9s  %s" % ("ALIAS", "MODELS", "BUDGET", "SPENT", "LEFT", "STATE")
    print(hdr)
    print("-" * len(hdr))
    for k in rows:
        alias = (k.get("key_alias") or k.get("key_name") or (k.get("token") or "")[:22])[:22]
        models = ", ".join(k.get("models") or []) or "all"
        if len(models) > 28:
            models = models[:25] + "..."
        try:
            budget = float(k.get("max_budget") or 0)
            spent = float(k.get("spend") or 0)
        except (TypeError, ValueError):
            budget, spent = 0.0, 0.0
        left = max(0.0, budget - spent)
        state = "CAPPED" if budget and spent >= budget else ("OK" if budget else "no cap")
        print("%-22s %-28s %9s %9s %9s  %s" % (alias, models, money(budget), money(spent), money(left), state))
    print("\nCAPPED = budget hit, requests now return 429. Full detail in the Admin UI.")


def cmd_create(args):
    if len(args) < 2:
        die("usage: python keys.py create <alias> <budget_usd> [model ...]")
    alias, budget = args[0], args[1]
    try:
        budget = float(budget)
    except ValueError:
        die("budget must be a number in USD, got %r" % budget)
    body = {"key_alias": alias, "max_budget": budget, "metadata": {"name": alias}}
    if len(args) > 2:
        body["models"] = args[2:]
    out = api("POST", "/key/generate", body)
    token = out.get("key")
    if not token:
        die("no key in response: %s" % json.dumps(out)[:300])
    print("Created virtual key: %s" % alias)
    print("Token (shown ONCE — save it): %s" % token)
    print("Budget: $%.2f — auto-429 when spent. Base URL for apps: %s/v1" % (budget, BASE))


def cmd_info(args):
    if not args:
        die("usage: python keys.py info <sk-...>")
    token = args[0]
    out = api("GET", "/key/info?key=" + urllib.parse.quote(token))
    info = norm(out)
    print("Alias   :", info.get("key_alias") or "-")
    print("Models  :", ", ".join(info.get("models") or []) or "all")
    print("Spent   :", money(info.get("spend")))
    print("Budget  :", money(info.get("max_budget")))
    print("Expires :", info.get("expires") or "never")


def cmd_spend(args):
    n = 10
    if args and args[0].isdigit():
        n = int(args[0])
    raw = api("GET", "/spend/logs?limit=%d" % n)
    rows = raw if isinstance(raw, list) else raw.get("data", [])
    if not rows:
        print("No spend logged yet. Make a request first.")
        return
    print("%-30s %9s %11s  %s" % ("MODEL", "SPEND", "TOKENS", "WHEN"))
    print("-" * 66)
    for r in rows:
        model = (r.get("model") or "-")[:30]
        when = (r.get("startTime") or r.get("endTime") or "").replace("T", " ")[:16]
        tokens = r.get("total_tokens") or 0
        print("%-30s %9s %11s  %s" % (model, money(r.get("spend")), tokens, when))


def cmd_block(args, block):
    if not args:
        die("usage: python keys.py %s <sk-...>" % ("block" if block else "unblock"))
    api("POST", "/key/block" if block else "/key/unblock", {"key": args[0]})
    print("%s key %s" % ("Blocked" if block else "Unblocked", args[0]))


def cmd_delete(args):
    if not args:
        die("usage: python keys.py delete <sk-...>")
    api("DELETE", "/key/delete?key=" + urllib.parse.quote(args[0]))
    print("Deleted key " + args[0])


def main():
    cmd = (sys.argv[1] if len(sys.argv) > 1 else "").lower()
    args = sys.argv[2:]
    if cmd in ("list", "ls"):
        cmd_list()
    elif cmd == "create":
        cmd_create(args)
    elif cmd == "info":
        cmd_info(args)
    elif cmd == "spend":
        cmd_spend(args)
    elif cmd == "block":
        cmd_block(args, True)
    elif cmd == "unblock":
        cmd_block(args, False)
    elif cmd == "delete":
        cmd_delete(args)
    else:
        print(__doc__)
        if cmd and cmd not in ("help", "-h", "--help"):
            sys.exit(1)


if __name__ == "__main__":
    main()
