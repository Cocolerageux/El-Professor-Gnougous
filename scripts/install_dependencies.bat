@echo off
title Installation des dépendances pour le service Windows
echo 📦 Installation des dépendances pour le service Windows...
echo.

:: Vérifier que Python existe
if not exist "%~dp0.venv\Scripts\python.exe" (
    echo ❌ Environnement virtuel Python non trouvé !
    echo Assurez-vous d'avoir exécuté le script d'installation initial.
    pause
    exit /b 1
)

echo 🔄 Mise à jour de pip...
"%~dp0.venv\Scripts\python.exe" -m pip install --upgrade pip

echo.
echo 📦 Installation de pywin32 pour les services Windows...
"%~dp0.venv\Scripts\python.exe" -m pip install pywin32

if %errorLevel% == 0 (
    echo.
    echo ✅ Dépendances installées avec succès !
    echo.
    echo 📋 Vous pouvez maintenant :
    echo   • Utiliser install_service.bat pour installer le service Windows
    echo   • Ou continuer à utiliser les fichiers .bat pour gérer le bot
    echo.
) else (
    echo.
    echo ❌ Erreur lors de l'installation des dépendances
    echo Vérifiez votre connexion internet et réessayez.
    echo.
)

pause
