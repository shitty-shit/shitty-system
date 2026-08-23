# KISS Mini Me — Android build notes

The Mini Me is a plain static web app (`.state/kiss/index.html` + `manifest.json` +
`sw.js` + icons). It is already an installable PWA; wrapping it into a native
Android app is a packaging step, not a rewrite.

## Quick path (PWA — zero build)

1. Serve `.state/kiss/` over HTTPS (or on the same LAN via the Mothership).
2. Open `index.html` in Chrome on the phone → menu → **Add to Home screen**.
3. It installs as a standalone, offline-first app (`sw.js` caches the shell).

## Native path (Capacitor)

```bash
npm create @capacitor/app mini-me
cd mini-me
npm i @capacitor/core @capacitor/android
npx cap add android
# copy .state/kiss/* into the webDir (default: www/)
npx cap sync android
npx cap open android   # → Android Studio → Build APK / App Bundle
```

Point the `webDir` at `.state/kiss/` in `capacitor.config.json`:

```json
{
  "appId": "com.kiss.minime",
  "appName": "KISS Mini Me",
  "webDir": "../.state/kiss",
  "server": { "androidScheme": "https" }
}
```

## Connecting to the Mothership bridge

The deck talks to the inbox bridge (`.state/kiss/bridge.py`, port 8765). On a
phone, `127.0.0.1` is the phone itself, so pass the Mothership's LAN IP:

```
http://<phone>/index.html?bridge=192.168.1.50:8765
```

(or set `localStorage.kiss.bridge` once, inside the app). Bridge CORS is already
open (`Access-Control-Allow-Origin: *`), so the phone can read/write briefs and
critiques against the Mothership. The dock/sync handshake (Phase 2) layers on
top of this; the web app already degrades gracefully to "inbox: local" when the
bridge is unreachable.

## Touch contract

- **Tap** a cube = select/inspect.
- **Drag** the header = move (snaps to grid; `touch-action:none` on the header).
- **Long-press** the header (550ms) = "make this cube a…" menu (rename, resize,
  duplicate, delete) — this is the Android touch path since right-click doesn't
  exist; it's jitter-safe and cancels if the finger moves >8px.
- **Corner** handle = resize (works with touch via pointer capture).
