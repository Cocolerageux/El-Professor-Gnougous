"""
Configuration pour l'hébergement cloud
Utilise les variables d'environnement pour la sécurité
"""
import os
import json

def get_config():
    """Récupère la configuration depuis les variables d'environnement ou le fichier local"""
    
    # Priorité aux variables d'environnement (pour le cloud)
    if os.environ.get('BOT_TOKEN'):
        return {
            "bot_token": os.environ.get('BOT_TOKEN'),
            "guild_id": os.environ.get('GUILD_ID'),
            "database_url": os.environ.get('DATABASE_URL', 'sqlite:///bot_data.db'),
            "web_secret_key": os.environ.get('WEB_SECRET_KEY', 'default-secret-key'),
            "web_port": int(os.environ.get('PORT', 5000)),
            "xp_settings": {
                "text_xp_min": 15,
                "text_xp_max": 25,
                "voice_xp_per_minute": 10,
                "cooldown_text": 60,
                "level_multiplier": 100
            },
            "coin_settings": {
                "coins_per_message": 2,
                "coins_per_voice_minute": 5,
                "daily_bonus": 100
            },
            "level_roles": {
                "text_levels": {
                    "5": "Débutant Textuel",
                    "10": "Expert Textuel",
                    "20": "Maître Textuel",
                    "50": "Légende Textuelle"
                },
                "voice_levels": {
                    "5": "Débutant Vocal",
                    "10": "Expert Vocal",
                    "20": "Maître Vocal",
                    "50": "Légende Vocale"
                }
            }
        }
    
    # Fallback vers le fichier local
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        
        # Assurer que le port est défini pour l'hébergement
        if 'web_port' not in config:
            config['web_port'] = int(os.environ.get('PORT', 5000))
        
        return config
    except FileNotFoundError:
        raise Exception("Aucune configuration trouvée ! Définissez les variables d'environnement ou créez config.json")

if __name__ == "__main__":
    config = get_config()
    print("Configuration chargée :")
    print(f"- Bot token: {'✅ Défini' if config.get('bot_token') else '❌ Manquant'}")
    print(f"- Guild ID: {config.get('guild_id', '❌ Manquant')}")
    print(f"- Web port: {config.get('web_port', 5000)}")
    print(f"- Database: {config.get('database_url', 'Non définie')}")
