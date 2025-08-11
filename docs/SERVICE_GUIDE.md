# Service Windows pour Bot Discord XP

## 📋 Vue d'ensemble

Le fichier `bot_service.py` permet d'installer votre bot Discord comme un service Windows qui fonctionne 24h/24 en arrière-plan, même sans être connecté.

## 🔧 Installation

### Étape 1 : Installer les dépendances
```bat
# Exécutez en tant qu'administrateur :
install_dependencies.bat
```

### Étape 2 : Installer le service
```bat
# Exécutez en tant qu'administrateur :
install_service.bat
```

## 📋 Gestion du service

### Commandes disponibles

```bash
# Installer le service
python bot_service.py install

# Démarrer le service
python bot_service.py start

# Arrêter le service
python bot_service.py stop

# Redémarrer le service
python bot_service.py restart

# Voir le statut
python bot_service.py status

# Désinstaller le service
python bot_service.py remove
```

## 🔍 Surveillance

### Logs du service
- **Fichier** : `service.log`
- **Contenu** : Démarrage, arrêts, erreurs, redémarrages automatiques
- **Format** : `YYYY-MM-DD HH:MM:SS - LEVEL - MESSAGE`

### Gestionnaire de services Windows
1. Ouvrir `services.msc`
2. Chercher "Discord Bot XP Service"
3. Voir le statut et gérer le service

## ⚙️ Fonctionnalités

### Redémarrage automatique
- Le service surveille le processus du bot
- En cas d'arrêt inattendu, redémarrage automatique après 10 secondes
- Logging de tous les événements

### Gestion des erreurs
- Capture des erreurs et logging
- Attente de 30 secondes avant nouvelle tentative en cas d'erreur
- Arrêt propre du service

## 🚫 Dépannage

### Le service ne s'installe pas
- Vérifiez que vous exécutez en tant qu'administrateur
- Assurez-vous que `pywin32` est installé : `pip install pywin32`
- Vérifiez que Python et le script principal existent

### Le service ne démarre pas
- Vérifiez le fichier `service.log`
- Assurez-vous que `config.json` est configuré correctement
- Testez le bot manuellement avec `start_bot.bat`

### Le bot se redémarre en boucle
- Vérifiez les logs pour identifier l'erreur
- Problème probable : token Discord invalide ou configuration incorrecte

## 🔄 Alternatives

Si le service Windows pose problème, utilisez les alternatives :

### Scripts batch
- `start_bot.bat` - Démarrer manuellement
- `stop_bot.bat` - Arrêter le bot
- `restart_bot.bat` - Redémarrer le bot

### Tâche planifiée
1. Ouvrir "Planificateur de tâches"
2. Créer une tâche de base
3. Déclencher "Au démarrage"
4. Action : Démarrer `start_bot.bat`

## 📁 Structure des fichiers

```
├── bot_service.py          # Service Windows principal
├── install_service.bat     # Installation automatique du service
├── install_dependencies.bat # Installation des dépendances
├── service.log            # Logs du service (créé automatiquement)
└── main.py               # Script principal du bot
```

## ⚠️ Important

- **Privilèges** : L'installation nécessite des droits administrateur
- **Sécurité** : Le service s'exécute avec le compte système
- **Maintenance** : Vérifiez régulièrement les logs
- **Sauvegarde** : Sauvegardez `config.json` et `bot_data.db`
