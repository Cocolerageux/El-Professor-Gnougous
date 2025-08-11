"""
Événements liés à l'expérience
"""
import discord
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class XPEvents(commands.Cog):
    """Gestionnaire des événements d'expérience"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Événement quand un membre rejoint le serveur"""
        try:
            if member.bot:
                return
            
            # Créer l'entrée utilisateur
            user_id = str(member.id)
            user = await self.bot.db.get_user(user_id)
            
            if not user:
                await self.bot.db.create_user(
                    user_id,
                    member.name,
                    "0"  # Discord a supprimé les discriminateurs
                )
                logger.info(f"Nouvel utilisateur créé : {member.name}")
            
            # Message de bienvenue optionnel
            if hasattr(self.bot.config, 'welcome_channel_id'):
                channel = member.guild.get_channel(int(self.bot.config['welcome_channel_id']))
                if channel:
                    embed = discord.Embed(
                        title="👋 Bienvenue !",
                        description=f"Bienvenue sur le serveur, {member.mention} !\n"
                                   f"Gagne de l'expérience en discutant et en rejoignant les canaux vocaux.",
                        color=discord.Color.green()
                    )
                    await channel.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Erreur lors de l'événement member_join : {e}")
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Événement quand un membre quitte le serveur"""
        try:
            if member.bot:
                return
            
            user_id = str(member.id)
            
            # Retirer l'utilisateur du tracking vocal s'il était présent
            if user_id in self.bot.voice_users:
                del self.bot.voice_users[user_id]
                logger.debug(f"Utilisateur {member.name} retiré du tracking vocal")
            
            # Optionnel : archiver ou supprimer les données
            # Pour l'instant on garde les données au cas où il reviendrait
            
        except Exception as e:
            logger.error(f"Erreur lors de l'événement member_remove : {e}")

async def setup(bot):
    """Charge le cog"""
    await bot.add_cog(XPEvents(bot))
