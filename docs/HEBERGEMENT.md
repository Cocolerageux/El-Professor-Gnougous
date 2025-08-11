# 🌐 Guide d'Hébergement Cloud pour Bot Discord 24h/24

## Plateformes Recommandées

### 1. **Heroku** (Gratuit avec limitations)
- ✅ Gratuit jusqu'à 550h/mois
- ✅ Très facile à configurer
- ❌ Se met en veille après 30min d'inactivité

### 2. **Railway** (Recommandé)
- ✅ 5$ de crédit gratuit/mois
- ✅ Très simple à utiliser
- ✅ Pas de veille automatique

### 3. **VPS Contabo/OVH** (Le moins cher)
- ✅ Environ 3-5€/mois
- ✅ Contrôle total
- ❌ Plus technique à configurer

### 4. **DigitalOcean/Linode**
- ✅ Fiable et performant
- ✅ 5-10$/mois
- ❌ Plus cher

## Configuration pour Railway (Recommandé)

### Étape 1: Préparer le Code
```bash
# Créer un fichier requirements.txt
pip freeze > requirements.txt

# Créer un Procfile
echo "web: python main.py" > Procfile

# Créer un runtime.txt
echo "python-3.11.0" > runtime.txt
```

### Étape 2: Railway
1. Allez sur https://railway.app
2. Connectez-vous avec GitHub
3. Créez un nouveau projet
4. Connectez votre repository
5. Ajoutez vos variables d'environnement:
   - `BOT_TOKEN`: Votre token Discord
   - `GUILD_ID`: ID de votre serveur
   - `WEB_SECRET_KEY`: Votre clé secrète

### Étape 3: Configuration des Variables
```env
BOT_TOKEN=votre_token_ici
GUILD_ID=votre_guild_id_ici
WEB_SECRET_KEY=votre_cle_secrete
DATABASE_URL=sqlite:///bot_data.db
WEB_PORT=8000
```

## Configuration pour VPS Ubuntu

### Installation
```bash
# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer Python et Git
sudo apt install python3 python3-pip python3-venv git -y

# Cloner votre bot
git clone https://github.com/votre-username/votre-bot.git
cd votre-bot

# Créer l'environnement virtuel
python3 -m venv .venv
source .venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### Service Systemd
```bash
# Créer le fichier service
sudo nano /etc/systemd/system/discord-bot.service
```

Contenu du fichier:
```ini
[Unit]
Description=Discord Bot XP
After=network.target

[Service]
Type=simple
User=votre-utilisateur
WorkingDirectory=/home/votre-utilisateur/votre-bot
ExecStart=/home/votre-utilisateur/votre-bot/.venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Activer le service:
```bash
sudo systemctl enable discord-bot
sudo systemctl start discord-bot
sudo systemctl status discord-bot
```

## Avantages/Inconvénients

| Solution | Coût | Simplicité | Fiabilité | Contrôle |
|----------|------|------------|-----------|----------|
| PC Windows 24h/24 | Électricité | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Railway | 5$/mois | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| VPS | 3-5€/mois | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Heroku | Gratuit | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |

## Recommandation

Pour débuter: **PC Windows avec moniteur** (gratuit, simple)
Pour production: **Railway** (fiable, simple, pas cher)
Pour avancé: **VPS** (contrôle total, économique à long terme)
