@echo off
title Bot Discord XP - Démarrage
echo 🤖 Démarrage du Bot Discord XP...
echo.

:: Vérifier si Python est disponible
if not exist "%~dp0.venv\Scripts\python.exe" (
    echo ❌ Environnement virtuel Python non trouvé !
    echo Assurez-vous que le dossier .venv existe.
    pause
    exit /b 1
)

:: Vérifier si le fichier config.json existe
if not exist "%~dp0config.json" (
    echo ❌ Fichier config.json non trouvé !
    echo Créez d'abord votre fichier de configuration.
    pause
    exit /b 1
)

:: Afficher les informations
echo 📋 Informations du bot :
echo - Dossier : %~dp0
echo - Python : %~dp0.venv\Scripts\python.exe
echo - Config : %~dp0config.json
echo.

:: Démarrer le bot
echo 🚀 Lancement du bot...
cd /d "%~dp0"
"%~dp0.venv\Scripts\python.exe" main.py

echo.
echo ⚠️ Le bot s'est arrêté.
echo Appuyez sur une touche pour fermer cette fenêtre...
pause >nul
