@echo off
echo Configuration du bot pour démarrage automatique avec le Planificateur de Tâches...

:: Créer une tâche planifiée
schtasks /create /tn "Discord Bot XP" /tr "\"%~dp0.venv\Scripts\python.exe\" \"%~dp0main.py\"" /sc onstart /ru "SYSTEM" /rl highest /f

if %errorLevel% == 0 (
    echo ✅ Tâche planifiée créée avec succès!
    echo Le bot se lancera automatiquement au démarrage de Windows.
    echo.
    echo Pour gérer la tâche:
    echo - Ouvrir le Planificateur de tâches Windows
    echo - Aller dans "Bibliothèque du Planificateur de tâches"
    echo - Chercher "Discord Bot XP"
    echo.
    echo Pour démarrer maintenant:
    schtasks /run /tn "Discord Bot XP"
    echo Tâche démarrée!
) else (
    echo ❌ Erreur lors de la création de la tâche planifiée.
    echo Assurez-vous d'exécuter ce script en tant qu'administrateur.
)

echo.
pause
