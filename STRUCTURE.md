# 📁 STRUCTURE DU PROJET ORGANISÉE

## 🗂️ Organisation des Dossiers

```
BOT POUR LES ORPHELINS/
├── 📁 .github/                 # Configuration GitHub
├── 📁 .venv/                   # Environnement virtuel Python
├── 📁 .vscode/                 # Configuration VS Code
├── 📁 bot/                     # 🤖 Code principal du bot Discord
│   ├── __init__.py
│   ├── bot.py                  # Logique principale du bot
│   ├── commands/               # Commandes Discord
│   ├── events/                 # Gestionnaires d'événements
│   └── utils/                  # Utilitaires (XP, niveaux)
├── 📁 database/                # 💾 Gestion base de données
│   ├── __init__.py
│   ├── database.py             # Connexion et opérations DB
│   └── models.py               # Modèles de données
├── 📁 web/                     # 🌐 Interface web
│   ├── __init__.py
│   ├── app.py                  # Application Flask
│   ├── routes/                 # Routes API
│   └── templates/              # Templates HTML
├── 📁 scripts/                 # 🔧 Scripts utilitaires
│   ├── *.bat                   # Scripts de gestion Windows
│   ├── bot_monitor.py          # Surveillance du bot
│   ├── bot_service.py          # Service Windows
│   ├── demo_shop_management.py # Démo gestion boutique
│   └── finalize.py             # Script de finalisation
├── 📁 tests/                   # 🧪 Tests du projet
│   ├── test_*.py               # Tous les fichiers de test
│   └── test_final.py           # Test de validation finale
├── 📁 docs/                    # 📚 Documentation
│   ├── README.md               # Guide principal
│   ├── GUIDE_GESTION_BOUTIQUE.md
│   ├── CONFIGURATION.md
│   ├── SERVICE_GUIDE.md
│   ├── HEBERGEMENT.md
│   ├── HEROKU_GUIDE.md
│   ├── RAILWAY_GUIDE.md
│   ├── VPS_GUIDE.md
│   └── PROJET_TERMINE.md       # Résumé final
├── 📁 deployment/              # 🚀 Fichiers de déploiement
│   ├── Procfile                # Configuration Heroku
│   └── runtime.txt             # Version Python
├── 📁 logs/                    # 📋 Fichiers de logs
│   └── bot.log                 # Logs du bot
├── 🔧 main.py                  # Point d'entrée principal
├── ⚙️ config.json              # Configuration
├── 💾 bot_data.db              # Base de données SQLite
├── 📋 requirements.txt         # Dépendances Python
└── 📁 STRUCTURE.md             # Ce fichier
```

## 🚀 Utilisation Rapide

### Démarrage
```bash
# Depuis la racine du projet
python main.py
# Ou
.\scripts\start_bot.bat
```

### Interface Web
- URL: http://localhost:5000
- Dashboard, gestion utilisateurs, boutique

### Tests
```bash
# Test complet
python tests\test_final.py

# Tests spécifiques
python tests\test_db.py
python tests\test_shop.py
python tests\test_web.py
```

### Scripts Utilitaires
- `scripts\start_bot.bat` - Démarrer le bot
- `scripts\stop_bot.bat` - Arrêter le bot
- `scripts\restart_bot.bat` - Redémarrer le bot
- `scripts\install_dependencies.bat` - Installer dépendances
- `scripts\bot_service.py` - Service Windows

## 📚 Documentation
Toute la documentation est dans le dossier `docs/` :
- Guide principal : `docs\README.md`
- Configuration : `docs\CONFIGURATION.md`
- Gestion boutique : `docs\GUIDE_GESTION_BOUTIQUE.md`
- Hébergement : `docs\HEBERGEMENT.md`

## 🎯 Fichiers Principaux
- `main.py` - Point d'entrée du projet
- `config.json` - Configuration du bot
- `bot_data.db` - Base de données
- `requirements.txt` - Dépendances

---
✅ **Projet organisé et prêt à l'emploi !**
