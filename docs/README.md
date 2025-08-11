# Discord Bot avec Système d'Expérience et Points

Un bot Discord complet avec système d'expérience, niveaux (vocal et textuel), système de monnaie et interface web de gestion.

## Fonctionnalités

- **Système d'expérience à deux niveaux** :
  - Niveau vocal (gain d'XP en canal vocal)
  - Niveau textuel (gain d'XP par messages)
- **Attribution automatique de rôles** selon les niveaux
- **Système de monnaie** pour acheter des objets/privilèges
- **Boutique** avec déblocage d'objets selon le niveau
- **Interface web** pour la gestion administrative

## Installation

1. Clonez le repository
2. Installez les dépendances : `pip install -r requirements.txt`
3. Configurez le fichier `config.json` avec vos tokens
4. Lancez le bot : `python main.py`
5. Accédez à l'interface web : http://localhost:5000

## Configuration

Créez un fichier `config.json` avec :
```json
{
  "bot_token": "VOTRE_TOKEN_BOT",
  "guild_id": "ID_DE_VOTRE_SERVEUR",
  "database_url": "sqlite:///bot_data.db",
  "web_secret_key": "votre_clé_secrète",
  "xp_settings": {
    "text_xp_min": 15,
    "text_xp_max": 25,
    "voice_xp_per_minute": 10,
    "cooldown_text": 60,
    "level_multiplier": 100
  }
}
```

## Utilisation

### Commandes du bot
- `/niveau` - Affiche votre niveau et XP
- `/classement` - Top 10 des utilisateurs
- `/boutique` - Affiche la boutique
- `/acheter <item>` - Achète un objet
- `/inventaire` - Affiche votre inventaire
- `/coins` - Affiche vos pièces

### Interface Web
Accédez à http://localhost:5000 pour :
- Gérer les utilisateurs
- Configurer les niveaux et rôles
- Gérer la boutique
- Voir les statistiques

## Structure du projet

```
├── main.py              # Point d'entrée principal
├── bot/                 # Code du bot Discord
│   ├── __init__.py
│   ├── bot.py          # Instance du bot
│   ├── commands/       # Commandes slash
│   ├── events/         # Événements Discord
│   └── utils/          # Utilitaires
├── database/           # Gestion base de données
│   ├── __init__.py
│   ├── models.py       # Modèles SQLAlchemy
│   └── database.py     # Configuration DB
├── web/               # Interface web Flask
│   ├── __init__.py
│   ├── app.py         # Application Flask
│   ├── routes/        # Routes web
│   └── templates/     # Templates HTML
├── config.json        # Configuration
└── requirements.txt   # Dépendances
```
