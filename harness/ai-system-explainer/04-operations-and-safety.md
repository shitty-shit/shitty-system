# How to operate it safely

## Start the normal stack

```powershell
Start-Process 'D:\Docker\Docker\Docker Desktop.exe'
Set-Location D:\Docker\stack
docker compose up -d
docker compose ps
```

Open WebUI at `http://127.0.0.1:8080`. The other useful local endpoints are:

- Ollama: `http://127.0.0.1:11434`
- LiteLLM: `http://127.0.0.1:4000`
- AnythingLLM: `http://127.0.0.1:3001`
- n8n: `http://127.0.0.1:5678`

## Start the native Unsloth fallback

Do this only when the Docker Unsloth profile is not running:

```powershell
$u = 'D:\AI\data\Unsloth\studio\bin\unsloth.exe'
Start-Process $u -ArgumentList 'studio','-H','127.0.0.1','-p','8888' -WorkingDirectory 'D:\AI\data\Unsloth\studio'
```

Check `http://127.0.0.1:8888/api/health`. Stop it with:

```powershell
& 'D:\AI\data\Unsloth\studio\bin\unsloth.exe' studio stop
```

The native fallback and the Docker Unsloth profile cannot both use port 8888.

## Safety rules

- Keep service bindings on `127.0.0.1` unless LAN access has authentication and
  Windows Firewall rules.
- Do not start a second native Ollama on port 11434.
- Keep secrets in `.env` or a local secret store; never put them in receipts,
  screenshots, graphs, or slides.
- Keep rollback copies until the Docker model list and inference test pass.
- Treat AnythingLLM as a user interface/workspace until its memory round trip is
  independently verified.
- A green web page is not enough: perform one real model request.
