"""
Événements liés aux canaux vocaux
"""
import discord
from discord.ext import commands
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class VoiceEvents(commands.Cog):
    """Gestionnaire des événements vocaux"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Événement de changement d'état vocal (déjà géré dans bot.py)"""
        # Cette fonction est déjà implémentée dans bot.py
        # On peut l'utiliser pour des fonctionnalités supplémentaires si nécessaire
        pass
    
    @commands.Cog.listener()
    async def on_ready(self):
        """Initialise le tracking vocal pour les utilisateurs déjà connectés"""
        try:
            # Vérifier tous les utilisateurs déjà en vocal au démarrage
            for guild in self.bot.guilds:
                for voice_channel in guild.voice_channels:
                    for member in voice_channel.members:
                        if not member.bot:
                            user_id = str(member.id)
                            if user_id not in self.bot.voice_users:
                                self.bot.voice_users[user_id] = datetime.utcnow()
                                logger.debug(f"Tracking vocal initialisé pour {member.name}")
            
            logger.info(f"Tracking vocal initialisé pour {len(self.bot.voice_users)} utilisateurs")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du tracking vocal : {e}")

async def setup(bot):
    """Charge le cog"""
    await bot.add_cog(VoiceEvents(bot))
