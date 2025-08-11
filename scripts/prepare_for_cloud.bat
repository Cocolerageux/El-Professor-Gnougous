@echo off
echo 🚀 PRÉPARATION POUR L'HÉBERGEMENT CLOUD
echo =======================================

REM Copier les fichiers de déploiement
echo 📁 Copie des fichiers de déploiement...
copy "deployment\Procfile" ".\Procfile" >nul
copy "deployment\runtime.txt" ".\runtime.txt" >nul

REM Mettre à jour requirements.txt
echo 📦 Mise à jour des dépendances...
.\.venv\Scripts\pip.exe freeze > requirements.txt

REM Créer .gitignore
echo 🔒 Création du .gitignore...
(
echo # Secrets et configuration locale
echo config.json
echo bot.log
echo *.log
echo.
echo # Base de données locale
echo bot_data.db
echo *.db
echo.
echo # Python
echo __pycache__/
echo *.pyc
echo *.pyo
echo *.pyd
echo .Python
echo env/
echo .venv/
echo venv/
echo ENV/
echo.
echo # VS Code
echo .vscode/
echo.
echo # OS
echo .DS_Store
echo Thumbs.db
echo.
echo # Fichiers temporaires
echo *.tmp
echo *.temp
) > .gitignore

echo ✅ Préparation terminée !
echo.
echo 📋 PROCHAINES ÉTAPES :
echo 1. Créez un repository GitHub
echo 2. Poussez ce code sur GitHub  
echo 3. Allez sur render.com
echo 4. Connectez votre repository
echo 5. Ajoutez les variables d'environnement
echo 6. Déployez !
echo.
echo 🔑 Variables d'environnement nécessaires :
echo    BOT_TOKEN=votre_token_discord
echo    GUILD_ID=1403538949359796274  
echo    WEB_SECRET_KEY=une_cle_secrete_aleatoire
echo.
pause
