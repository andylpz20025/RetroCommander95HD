@echo off
title Retro Commander 95 HD v2.2 (Dark Stable)
color 1f
echo ===========================================
echo     RETRO COMMANDER 95 HD v2.2 (Dark Stable)
echo ===========================================
echo.
echo Starte den Commander...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo Fehler: Python nicht gefunden.
    echo Bitte installiere Python 3.x und setze es in den PATH.
    pause
    exit /b
)

python main.py

echo.
echo ===========================================
echo Programm beendet.
pause
