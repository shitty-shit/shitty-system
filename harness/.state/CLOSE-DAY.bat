@echo off
setlocal
rem ============================================================
rem  LACES_CASES day-close butler — double-click when done.
rem  Runs the EOD pass, then opens the dashboard in your browser.
rem  Pass "--scheduled" as arg 1 to skip the pause (used by the
rem  Windows Task Scheduler entry).
rem ============================================================
set "PY=C:\Python314\python.exe"
if not exist "%PY%" set "PY=python"
cd /d "%~dp0"

echo [butler] Running end-of-day pass...
"%PY%" butler.py --eod
if errorlevel 1 goto :fail

echo [butler] Opening dashboard...
start "" "%~dp0dash.html"
if /I not "%~1"=="--scheduled" pause
exit /b 0

:fail
echo [butler] FAILED - see butler.log
pause
exit /b 1
