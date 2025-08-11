@echo off
title Bot Discord XP - Arrêt
echo 🛑 Arrêt du Bot Discord XP...
echo.

:: Rechercher et arrêter le processus Python du bot
echo 🔍 Recherche du processus du bot...

:: Arrêter tous les processus Python qui exécutent main.py
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq python.exe" /fo csv ^| findstr "python.exe"') do (
    echo Vérification du processus %%i...
    wmic process where "ProcessId=%%i and CommandLine like '%%main.py%%'" delete 2>nul
)

:: Arrêter aussi les processus depuis l'environnement virtuel
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq python.exe" /fo csv ^| findstr "python.exe"') do (
    echo Vérification du processus %%i...
    wmic process where "ProcessId=%%i and CommandLine like '%%.venv\\Scripts\\python.exe%%'" delete 2>nul
)

:: Méthode alternative avec taskkill
echo 🔄 Arrêt des processus Python liés au bot...
taskkill /f /im python.exe /fi "WINDOWTITLE eq Bot Discord XP*" 2>nul

echo.
echo ✅ Tentative d'arrêt terminée.
echo.
echo 📋 Processus Python actuellement en cours :
tasklist /fi "imagename eq python.exe" 2>nul
echo.

:: Proposer d'arrêter tous les processus Python si nécessaire
echo ⚠️  Si le bot est encore actif, voulez-vous arrêter TOUS les processus Python ? (O/N)
set /p choice="Votre choix : "
if /i "%choice%"=="O" (
    echo 🛑 Arrêt de tous les processus Python...
    taskkill /f /im python.exe 2>nul
    echo ✅ Tous les processus Python ont été arrêtés.
) else (
    echo ℹ️  Arrêt annulé. Le bot pourrait encore être actif.
)

echo.
echo Appuyez sur une touche pour fermer cette fenêtre...
pause >nul
