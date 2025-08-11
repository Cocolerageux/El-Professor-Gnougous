"""
Point d'entrée principal du bot Discord avec système d'expérience
"""
import asyncio
import json
import logging
import os
from bot.bot import DiscordBot
from web.app import create_web_app
import threading

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def load_config():
    """Charge la configuration depuis config.json ou variables d'environnement"""
    try:
        # Priorité aux variables d'environnement (pour le cloud)
        if os.environ.get('BOT_TOKEN'):
            return {
                "bot_token": os.environ.get('BOT_TOKEN'),
                "guild_id": os.environ.get('GUILD_ID'),
                "database_url": os.environ.get('DATABASE_URL', 'sqlite:///bot_data.db'),
                "web_secret_key": os.environ.get('WEB_SECRET_KEY', 'default_secret'),
                "web_port": int(os.environ.get('WEB_PORT', 5000)),
                "xp_settings": {
                    "text_xp_min": int(os.environ.get('TEXT_XP_MIN', 15)),
                    "text_xp_max": int(os.environ.get('TEXT_XP_MAX', 25)),
                    "voice_xp_per_minute": int(os.environ.get('VOICE_XP_PER_MINUTE', 10)),
                    "cooldown_text": int(os.environ.get('COOLDOWN_TEXT', 60)),
                    "level_multiplier": int(os.environ.get('LEVEL_MULTIPLIER', 100))
                },
                "coin_settings": {
                    "coins_per_message": int(os.environ.get('COINS_PER_MESSAGE', 2)),
                    "coins_per_voice_minute": int(os.environ.get('COINS_PER_VOICE_MINUTE', 5)),
                    "daily_bonus": int(os.environ.get('DAILY_BONUS', 100))
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
        
        # Sinon, charger depuis config.json
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("Fichier config.json non trouvé et variables d'environnement manquantes.")
        return None
    except json.JSONDecodeError:
        logger.error("Erreur dans le format JSON du fichier config.json")
        return None

def run_web_app(config):
    """Lance l'application web Flask dans un thread séparé"""
    try:
        app = create_web_app(config)
        # Port pour l'hébergement cloud (Railway, Heroku, etc.)
        port = int(os.environ.get('PORT', config.get('web_port', 5000)))
        app.run(
            host='0.0.0.0',
            port=port,
            debug=False,
            use_reloader=False
        )
    except Exception as e:
        logger.error(f"Erreur lors du lancement de l'application web : {e}")

async def main():
    """Fonction principale"""
    config = load_config()
    if not config:
        return
    
    # Validation de la configuration
    if not config.get('bot_token'):
        logger.error("Token du bot manquant dans config.json")
        return
    
    logger.info("Démarrage du système...")
    
    # Démarrage de l'application web dans un thread séparé
    web_thread = threading.Thread(
        target=run_web_app,
        args=(config,),
        daemon=True
    )
    web_thread.start()
    logger.info(f"Interface web démarrée sur http://localhost:{config.get('web_port', 5000)}")
    
    # Création et démarrage du bot
    bot = DiscordBot(config)
    
    try:
        await bot.start(config['bot_token'])
    except KeyboardInterrupt:
        logger.info("Arrêt du bot demandé par l'utilisateur")
    except Exception as e:
        logger.error(f"Erreur lors du démarrage du bot : {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Arrêt du programme")
    except Exception as e:
        logger.error(f"Erreur fatale : {e}")
