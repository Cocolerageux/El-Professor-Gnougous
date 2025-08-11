# Guide VPS pour Bot Discord 24h/24

## Fournisseurs Recommandés (3-5€/mois)

### Contabo (Le moins cher)
- **Prix:** 3.99€/mois
- **Specs:** 4 vCPU, 8GB RAM, 50GB SSD
- **Site:** https://contabo.com

### OVH VPS
- **Prix:** 3.50€/mois  
- **Specs:** 1 vCPU, 2GB RAM, 20GB SSD
- **Site:** https://www.ovhcloud.com

### Hetzner Cloud
- **Prix:** 3.29€/mois
- **Specs:** 1 vCPU, 2GB RAM, 20GB SSD
- **Site:** https://www.hetzner.com/cloud

## Installation sur Ubuntu Server

### 1. Connexion SSH
```bash
ssh root@votre_ip_serveur
```

### 2. Installation des Dépendances
```bash
# Mise à jour du système
apt update && apt upgrade -y

# Installation de Python et Git
apt install python3 python3-pip python3-venv git nano htop -y

# Création d'un utilisateur non-root
adduser botuser
usermod -aG sudo botuser
su - botuser
```

### 3. Installation du Bot
```bash
# Cloner le projet (ou uploader via SCP)
git clone https://github.com/votre-username/votre-bot.git
cd votre-bot

# Créer l'environnement virtuel
python3 -m venv .venv
source .venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer le bot
nano config.json
```

### 4. Service Systemd (Démarrage Auto)
```bash
# Créer le fichier service
sudo nano /etc/systemd/system/discord-bot.service
```

Contenu:
```ini
[Unit]
Description=Discord Bot XP Service
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/home/botuser/votre-bot
ExecStart=/home/botuser/votre-bot/.venv/bin/python main.py
Restart=always
RestartSec=10
Environment=PATH=/home/botuser/votre-bot/.venv/bin

[Install]
WantedBy=multi-user.target
```

Activer le service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable discord-bot
sudo systemctl start discord-bot
sudo systemctl status discord-bot
```

### 5. Gestion du Bot
```bash
# Voir les logs
sudo journalctl -u discord-bot -f

# Redémarrer
sudo systemctl restart discord-bot

# Arrêter
sudo systemctl stop discord-bot

# Voir le statut
sudo systemctl status discord-bot
```

## Avantages VPS
- ✅ Contrôle total
- ✅ Pas de limitations
- ✅ Très économique à long terme
- ✅ Peut héberger plusieurs bots
- ✅ Accès SSH complet

## Inconvénients VPS
- ❌ Plus technique à configurer
- ❌ Gestion de la sécurité
- ❌ Maintenance système requise
