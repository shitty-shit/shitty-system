@echo off
rem keys — budget cards for your AI providers. Double-click for the menu.
setlocal
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Python not found on PATH.
  pause
  exit /b 1
)
if "%~1"=="" (
  python keys.py
  echo.
  pause
) else (
  python keys.py %*
)
