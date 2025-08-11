@echo off
title Bot Discord XP - Restart
echo 🔄 Redémarrage du Bot Discord...

:: Arrêter le bot s'il est en cours d'exécution
echo Arrêt du bot en cours...
taskkill /f /im python.exe >nul 2>&1

:: Attendre 3 secondes
echo Attente de 3 secondes...
timeout /t 3 >nul

:: Redémarrer le bot
echo 🚀 Redémarrage du bot...
cd /d "%~dp0"
start "Bot Discord XP" "%~dp0.venv\Scripts\python.exe" main.py

echo ✅ Bot redémarré !
echo Le bot fonctionne maintenant dans une nouvelle fenêtre.
echo.
pause
