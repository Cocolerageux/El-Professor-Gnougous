@echo off
title Bot Discord XP - Moniteur 24h/24
echo 🤖 Démarrage du moniteur du Bot Discord...
echo Le bot va redémarrer automatiquement en cas d'arrêt.
echo Appuyez sur Ctrl+C pour arrêter complètement.
echo.

cd /d "%~dp0"
"%~dp0.venv\Scripts\python.exe" bot_monitor.py

pause
