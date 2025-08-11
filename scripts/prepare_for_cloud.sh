#!/bin/bash
# Script de déploiement automatique pour l'hébergement cloud

echo "🚀 PRÉPARATION POUR L'HÉBERGEMENT CLOUD"
echo "======================================="

# Copier les fichiers de déploiement à la racine
echo "📁 Copie des fichiers de déploiement..."
cp deployment/Procfile ./Procfile
cp deployment/runtime.txt ./runtime.txt

# Mettre à jour requirements.txt
echo "📦 Mise à jour des dépendances..."
pip freeze > requirements.txt

# Créer .gitignore pour le cloud
echo "🔒 Création du .gitignore..."
cat > .gitignore << EOL
# Secrets et configuration locale
config.json
bot.log
*.log

# Base de données locale
bot_data.db
*.db

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
.venv/
venv/
ENV/

# VS Code
.vscode/

# OS
.DS_Store
Thumbs.db

# Fichiers temporaires
*.tmp
*.temp
EOL

# Créer un README pour GitHub
echo "📖 Création du README GitHub..."
cat > README_GITHUB.md << EOL
# 🤖 Discord Bot XP - Bot complet avec système d'expérience

Bot Discord professionnel avec système d'XP double (vocal/textuel), boutique, et interface web.

## 🚀 Déploiement sur Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

### Variables d'environnement requises :
- \`BOT_TOKEN\` : Token de votre bot Discord
- \`GUILD_ID\` : ID de votre serveur Discord
- \`WEB_SECRET_KEY\` : Clé secrète pour l'interface web

## ✨ Fonctionnalités

- 🎯 Système XP double (vocal + textuel)
- 🏆 Attribution automatique de rôles
- 💰 Système de monnaie et boutique
- 🌐 Interface web de gestion
- 📊 Statistiques en temps réel
- 🎁 Bonus quotidien

## 🛠️ Technologies

- Python 3.11+
- discord.py 2.3+
- Flask
- SQLite
- Bootstrap 5
EOL

echo "✅ Préparation terminée !"
echo ""
echo "📋 PROCHAINES ÉTAPES :"
echo "1. Créez un repository GitHub"
echo "2. Poussez ce code sur GitHub"
echo "3. Allez sur render.com"
echo "4. Connectez votre repository"
echo "5. Ajoutez les variables d'environnement"
echo "6. Déployez !"
echo ""
echo "🔑 Variables d'environnement nécessaires :"
echo "   BOT_TOKEN=votre_token_discord"
echo "   GUILD_ID=1403538949359796274"
echo "   WEB_SECRET_KEY=une_cle_secrete_aleatoire"
