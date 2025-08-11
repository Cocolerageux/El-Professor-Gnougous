# Guide de Déploiement sur Heroku

## Installation d'Heroku CLI
1. Téléchargez et installez Heroku CLI : https://devcenter.heroku.com/articles/heroku-cli
2. Redémarrez votre terminal

## Déploiement
```bash
# Se connecter à Heroku
heroku login

# Créer une nouvelle app
heroku create votre-bot-discord

# Ajouter les variables d'environnement
heroku config:set BOT_TOKEN="votre_token_discord"
heroku config:set GUILD_ID="votre_guild_id"
heroku config:set WEB_SECRET_KEY="votre_cle_secrete"

# Déployer
git add .
git commit -m "Déploiement initial"
git push heroku main
```

## Limitations Heroku Gratuit
- ⚠️ Se met en veille après 30 minutes d'inactivité
- ⚠️ 550 heures/mois maximum
- ⚠️ Redémarre toutes les 24h

## Solution Anti-Veille
Utilisez un service comme "Uptime Robot" pour ping votre bot toutes les 25 minutes.
