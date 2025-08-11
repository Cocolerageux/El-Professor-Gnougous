# 🤖 Configuration du Bot Discord

## Étapes de Configuration Initiale

### 1. Créer une Application Discord

1. Allez sur https://discord.com/developers/applications
2. Cliquez sur "New Application"
3. Donnez un nom à votre bot
4. Allez dans l'onglet "Bot"
5. Cliquez sur "Add Bot"
6. Copiez le token (gardez-le secret !)

### 2. Inviter le Bot sur votre Serveur

1. Dans l'onglet "OAuth2" > "URL Generator"
2. Sélectionnez "bot" dans les scopes
3. Sélectionnez ces permissions :
   - Send Messages
   - Use Slash Commands
   - Manage Roles
   - View Channels
   - Connect (pour les canaux vocaux)
   - Speak (pour les canaux vocaux)
4. Copiez l'URL générée et ouvrez-la dans votre navigateur
5. Sélectionnez votre serveur et autorisez

### 3. Configurer le Bot

1. Ouvrez le fichier `config.json`
2. Remplacez `"VOTRE_TOKEN_BOT_DISCORD"` par votre token
3. Remplacez `"ID_DE_VOTRE_SERVEUR"` par l'ID de votre serveur Discord

Pour obtenir l'ID du serveur :
- Activez le mode développeur dans Discord (Paramètres > Avancé > Mode développeur)
- Clic droit sur votre serveur > Copier l'ID

### 4. Lancer le Bot

#### Option 1 : Via Terminal
```bash
cd "c:\Users\COCOLERAGEUX\Desktop\BOT POUR LES ORPHELINS"
.\.venv\Scripts\python.exe main.py
```

#### Option 2 : Via VS Code
- Ouvrez le projet dans VS Code
- Utilisez Ctrl+Shift+P et tapez "Tasks: Run Task"
- Sélectionnez "Lancer le Bot Discord"

### 5. Accéder à l'Interface Web

Une fois le bot lancé, ouvrez votre navigateur et allez sur :
http://localhost:5000

## Commandes Disponibles

### Pour les Utilisateurs
- `/niveau` - Affiche votre niveau et expérience
- `/niveau @utilisateur` - Affiche le niveau d'un autre utilisateur
- `/classement` - Top 10 des utilisateurs (textuel)
- `/classement voice` - Top 10 des utilisateurs (vocal)
- `/coins` - Affiche vos pièces
- `/boutique` - Affiche les objets disponibles
- `/acheter <id>` - Achète un objet
- `/inventaire` - Affiche votre inventaire

### Pour les Administrateurs
- `/admin_give_xp` - Donne de l'XP à un utilisateur
- `/admin_give_coins` - Donne des pièces à un utilisateur
- `/admin_reset_user` - Remet à zéro un utilisateur
- `/admin_sync_roles` - Synchronise les rôles d'un utilisateur

## Système d'Expérience

### XP Textuel
- Gagné en envoyant des messages
- Cooldown configurable (par défaut 60 secondes)
- Quantité aléatoire entre min et max configurables

### XP Vocal
- Gagné en restant dans un canal vocal
- XP attribué par minute passée en vocal
- Bonus pour les longues sessions

### Niveaux et Rôles
- Le bot crée automatiquement les rôles selon la configuration
- Les rôles sont attribués automatiquement lors des montées de niveau
- Formule de niveau personnalisable

## Système de Monnaie

### Gains de Pièces
- Par message envoyé
- Par minute en canal vocal
- Bonus quotidien (futur)

### Boutique
- Objets déblocables selon le niveau
- Rôles achetables
- Objets consommables
- Privilèges spéciaux

## Dépannage

### Le bot ne se lance pas
- Vérifiez que le token est correct
- Vérifiez que les dépendances sont installées
- Vérifiez les permissions du bot sur Discord

### Les commandes ne fonctionnent pas
- Assurez-vous que le bot a les bonnes permissions
- Vérifiez que les commandes slash sont synchronisées
- Redémarrez le bot si nécessaire

### L'interface web ne fonctionne pas
- Vérifiez que le port 5000 n'est pas occupé
- Changez le port dans config.json si nécessaire
- Vérifiez les logs pour les erreurs

## Support

Pour plus d'aide, consultez :
- La documentation Discord.py : https://discordpy.readthedocs.io/
- Le Discord Developer Portal : https://discord.com/developers/docs/
- Les logs du bot dans le terminal

Profitez de votre bot Discord ! 🎉
