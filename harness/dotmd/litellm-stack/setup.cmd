@echo off
rem LiteLLM stack setup — double-click me.
setlocal
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Python not found on PATH. Install from https://www.python.org/downloads/ and re-run.
  pause
  exit /b 1
)
python setup.py
pause
