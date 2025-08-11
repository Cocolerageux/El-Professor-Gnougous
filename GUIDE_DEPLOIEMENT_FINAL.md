# 🚀 GUIDE DE DÉPLOIEMENT COMPLET - BOT DISCORD 24/7

## ✅ ÉTAPES RÉALISÉES

Votre bot est maintenant prêt pour l'hébergement cloud ! Tous les fichiers nécessaires ont été créés :

- ✅ `Procfile` - Configuration pour l'hébergement
- ✅ `runtime.txt` - Version de Python 
- ✅ `requirements.txt` - Dépendances à jour
- ✅ `.gitignore` - Fichiers à exclure de Git
- ✅ Configuration cloud dans `main.py`

---

## 🎯 DÉPLOIEMENT SUR RENDER.COM (RECOMMANDÉ)

### 1. Créer un Repository GitHub

1. Allez sur [github.com](https://github.com) et créez un compte si nécessaire
2. Cliquez sur "New repository"
3. Nommez-le `bot-discord-orphelins` 
4. Laissez-le **PUBLIC** (requis pour le plan gratuit)
5. NE cochez PAS "Initialize with README"
6. Cliquez "Create repository"

### 2. Pousser votre Code sur GitHub

Ouvrez PowerShell dans votre dossier bot et exécutez :

```powershell
# Initialiser Git
git init

# Ajouter tous les fichiers
git add .

# Premier commit
git commit -m "Premier déploiement du bot Discord"

# Connecter à votre repository GitHub (remplacez VOTRE_USERNAME)
git remote add origin https://github.com/VOTRE_USERNAME/bot-discord-orphelins.git

# Pousser le code
git push -u origin main
```

### 3. Créer un Compte Render

1. Allez sur [render.com](https://render.com)
2. Cliquez "Get Started for Free"
3. Connectez-vous avec votre compte GitHub

### 4. Déployer le Bot

1. Dans le dashboard Render, cliquez "New +"
2. Sélectionnez "Web Service"
3. Connectez votre repository `bot-discord-orphelins`
4. Configurez :
   - **Name** : `bot-discord-orphelins`
   - **Environment** : `Python 3`
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `python main.py`
   - **Instance Type** : `Free`

### 5. Variables d'Environnement

Dans la section "Environment Variables", ajoutez :

```
BOT_TOKEN = votre_token_discord_ici
GUILD_ID = 1403538949359796274
WEB_SECRET_KEY = une_cle_secrete_aleatoire_ici
```

**🔑 Pour générer WEB_SECRET_KEY :**
```python
import secrets
print(secrets.token_hex(32))
```

### 6. Déployer !

1. Cliquez "Create Web Service"
2. Attendez 2-5 minutes pour le déploiement
3. Votre bot sera en ligne 24/7 !

---

## 🔧 ALTERNATIVES GRATUITES

### Option 2 : Railway.app
- **Avantage** : Interface simple, $5 de crédit gratuit/mois
- **Durée** : ~500 heures gratuites/mois
- **Process** : Similaire à Render, connecter GitHub et déployer

### Option 3 : Heroku (Alternatives)
- **Glitch.com** : Gratuit mais dort après inactivité
- **PythonAnywhere** : 1 app gratuite, 100 secondes CPU/jour

---

## 📊 SURVEILLANCE

### Interface Web
Votre bot incluera une interface web accessible à :
`https://votre-app-name.onrender.com`

### Logs
Surveillez les logs dans le dashboard Render pour déboguer.

---

## 🚨 PROBLÈMES COURANTS

### Bot ne se connecte pas
- Vérifiez que `BOT_TOKEN` est correct
- Assurez-vous que le bot a les permissions nécessaires

### Commandes ne marchent pas
- Vérifiez que `GUILD_ID` est correct
- Les permissions du bot dans Discord

### Application se ferme
- Vérifiez les logs dans Render
- Souvent lié aux variables d'environnement manquantes

---

## ✨ FÉLICITATIONS !

Une fois déployé, votre bot Discord fonctionnera 24/7 sans que votre PC soit allumé !

**🎮 Fonctionnalités disponibles :**
- ✅ Système d'expérience et de niveaux
- ✅ Bonus quotidien avec `/daily`
- ✅ Boutique virtuelle avec inventaire
- ✅ Interface web de gestion
- ✅ Tracking vocal automatique
- ✅ Commandes admin complètes

**Votre bot est maintenant professionnel et prêt pour une utilisation 24/7 !** 🎉
