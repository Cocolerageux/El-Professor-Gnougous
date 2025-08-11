@echo off
title Installation Service Discord Bot XP
echo 🔧 Installation du service Discord Bot XP...
echo.

:: Vérifier les privilèges administrateur
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Privilèges administrateur détectés.
) else (
    echo ❌ ERREUR: Ce script doit être exécuté en tant qu'administrateur!
    echo.
    echo 📋 Instructions :
    echo 1. Clic droit sur ce fichier .bat
    echo 2. Sélectionnez "Exécuter en tant qu'administrateur"
    echo.
    pause
    exit /b 1
)

:: Vérifier que Python existe
if not exist "%~dp0.venv\Scripts\python.exe" (
    echo ❌ Environnement virtuel Python non trouvé !
    echo Assurez-vous que le dossier .venv existe et contient Python.
    pause
    exit /b 1
)

echo.
echo 📦 Installation des dépendances pour le service Windows...
"%~dp0.venv\Scripts\python.exe" -m pip install pywin32
if %errorLevel% neq 0 (
    echo ❌ Erreur lors de l'installation de pywin32
    pause
    exit /b 1
)

echo.
echo 🔧 Installation du service Windows...
"%~dp0.venv\Scripts\python.exe" "%~dp0bot_service.py" install
if %errorLevel% neq 0 (
    echo ❌ Erreur lors de l'installation du service
    echo Vérifiez que vous avez les privilèges administrateur
    pause
    exit /b 1
)

echo.
echo 🚀 Démarrage du service...
"%~dp0.venv\Scripts\python.exe" "%~dp0bot_service.py" start
if %errorLevel% neq 0 (
    echo ❌ Erreur lors du démarrage du service
    pause
    exit /b 1
)

echo.
echo ✅ Service installé et démarré avec succès!
echo 🤖 Le bot Discord fonctionne maintenant en arrière-plan 24h/24.
echo.
echo 📋 Commandes utiles pour gérer le service :
echo   • Arrêter    : python bot_service.py stop
echo   • Redémarrer : python bot_service.py restart  
echo   • Désinstaller : python bot_service.py remove
echo   • Statut     : python bot_service.py status
echo.
echo 📁 Logs du service : service.log
echo.
pause
