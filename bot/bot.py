"""
Bot Discord principal avec système d'expérience
"""
import discord
from discord.ext import commands, tasks
import logging
import asyncio
from datetime import datetime, timedelta
import random
from database.database import DatabaseManager
from bot.utils.xp_calculator import XPCalculator
from bot.utils.level_manager import LevelManager

logger = logging.getLogger(__name__)

class DiscordBot(commands.Bot):
    """Bot Discord principal"""
    
    def __init__(self, config):
        # Configuration des intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        intents.members = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
        
        self.config = config
        self.db = DatabaseManager(config['database_url'])
        self.xp_calc = XPCalculator(config['xp_settings'])
        self.level_manager = LevelManager(config, self)
        
        # Tracking des utilisateurs en vocal
        self.voice_users = {}
        
        # Cooldowns pour éviter le spam
        self.text_cooldowns = {}
        
    async def setup_hook(self):
        """Initialisation du bot"""
        try:
            await self.db.initialize()
            
            # Charger les commandes
            await self.load_extension('bot.commands.experience')
            await self.load_extension('bot.commands.shop')
            await self.load_extension('bot.commands.admin')
            
            # Charger les événements
            await self.load_extension('bot.events.xp_events')
            await self.load_extension('bot.events.voice_events')
            
            # Démarrer les tâches en arrière-plan
            self.voice_xp_task.start()
            
            logger.info("Bot configuré avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors de la configuration du bot : {e}")
            raise
    
    async def on_ready(self):
        """Événement quand le bot est prêt"""
        logger.info(f'{self.user} est connecté et prêt!')
        
        # Synchroniser les commandes slash
        try:
            # Debug : Lister les commandes avant sync
            commands_list = self.tree.get_commands()
            logger.info(f'Commandes locales chargées : {len(commands_list)}')
            for cmd in commands_list:
                logger.info(f'  - /{cmd.name}: {cmd.description}')
            
            # Synchronisation spécifique au serveur (instantanée)
            if self.config.get('guild_id'):
                guild = discord.Object(id=int(self.config['guild_id']))
                # Copier toutes les commandes vers le serveur spécifique
                self.tree.copy_global_to(guild=guild)
                synced = await self.tree.sync(guild=guild)
                logger.info(f'{len(synced)} commandes slash synchronisées pour le serveur {self.config["guild_id"]} (instantané)')
            else:
                # Fallback synchronisation globale
                synced = await self.tree.sync()
                logger.info(f'{len(synced)} commandes slash synchronisées globalement (peut prendre 1h)')
            
            # Debug : Lister les commandes synchronisées
            for cmd in synced:
                logger.info(f'  Sync: /{cmd.name}')
                
        except Exception as e:
            logger.error(f'Erreur lors de la synchronisation des commandes : {e}')
        
        # Définir le statut du bot
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="votre progression | /help"
            )
        )
    
    async def on_interaction(self, interaction):
        """Événement sur réception d'une interaction"""
        logger.info(f"Interaction reçue: {interaction.type} de {interaction.user}")
    
    async def on_app_command_error(self, interaction, error):
        """Gestionnaire d'erreur pour les commandes slash"""
        logger.error(f"Erreur commande slash: {error}")
        logger.error(f"Commande: {interaction.command}")
        logger.error(f"Utilisateur: {interaction.user}")
        
        try:
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Une erreur est survenue: {str(error)}", 
                    ephemeral=True
                )
            else:
                await interaction.followup.send(
                    f"❌ Une erreur est survenue: {str(error)}", 
                    ephemeral=True
                )
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi du message d'erreur: {e}")

    async def on_message(self, message):
        """Événement sur réception d'un message"""
        # Ignorer les messages du bot
        if message.author.bot:
            return
        
        # Traiter les commandes normales
        await self.process_commands(message)
        
        # Système d'XP textuel
        await self.handle_text_xp(message)
    
    async def handle_text_xp(self, message):
        """Gère l'attribution d'XP textuel"""
        try:
            user_id = str(message.author.id)
            now = datetime.utcnow()
            
            # Vérifier le cooldown
            if user_id in self.text_cooldowns:
                last_xp = self.text_cooldowns[user_id]
                cooldown = self.config['xp_settings']['cooldown_text']
                if (now - last_xp).total_seconds() < cooldown:
                    return
            
            # Calculer l'XP à donner
            xp_gained = self.xp_calc.calculate_text_xp()
            coins_gained = self.config['coin_settings']['coins_per_message']
            
            # Récupérer ou créer l'utilisateur
            user = await self.db.get_user(user_id)
            if not user:
                user = await self.db.create_user(
                    user_id,
                    message.author.name,
                    "0"  # Discord a supprimé les discriminateurs
                )
            
            if user:
                old_level = user.text_level
                
                # Mettre à jour l'XP et les coins
                await self.db.update_user_xp(user_id, text_xp=xp_gained)
                await self.db.update_user_coins(user_id, coins_gained)
                
                # Recalculer le niveau
                new_level = self.xp_calc.xp_to_level(user.text_xp + xp_gained)
                
                # Vérifier si l'utilisateur a monté de niveau
                if new_level > old_level:
                    await self.level_manager.handle_level_up(
                        message.author,
                        message.channel,
                        old_level,
                        new_level,
                        'text'
                    )
                
                # Mettre à jour le cooldown
                self.text_cooldowns[user_id] = now
                
        except Exception as e:
            logger.error(f"Erreur lors du traitement de l'XP textuel : {e}")
    
    async def on_voice_state_update(self, member, before, after):
        """Événement de changement d'état vocal"""
        try:
            user_id = str(member.id)
            now = datetime.utcnow()
            
            # Utilisateur rejoint un canal vocal
            if before.channel is None and after.channel is not None:
                self.voice_users[user_id] = now
                logger.debug(f"{member.name} a rejoint le canal vocal {after.channel.name}")
            
            # Utilisateur quitte un canal vocal
            elif before.channel is not None and after.channel is None:
                if user_id in self.voice_users:
                    join_time = self.voice_users[user_id]
                    duration_minutes = (now - join_time).total_seconds() / 60
                    
                    if duration_minutes >= 1:  # Minimum 1 minute pour gagner de l'XP
                        await self.handle_voice_xp_gain(member, duration_minutes)
                    
                    del self.voice_users[user_id]
                    logger.debug(f"{member.name} a quitté le canal vocal après {duration_minutes:.1f} minutes")
            
            # Utilisateur change de canal (optionnel : reset le timer)
            elif before.channel != after.channel and before.channel is not None and after.channel is not None:
                self.voice_users[user_id] = now
                logger.debug(f"{member.name} a changé de canal vocal")
                
        except Exception as e:
            logger.error(f"Erreur lors du traitement de l'événement vocal : {e}")
    
    async def handle_voice_xp_gain(self, member, duration_minutes):
        """Traite le gain d'XP vocal"""
        try:
            user_id = str(member.id)
            
            # Calculer l'XP et les coins
            xp_gained = self.xp_calc.calculate_voice_xp(duration_minutes)
            coins_gained = int(duration_minutes * self.config['coin_settings']['coins_per_voice_minute'])
            
            # Récupérer ou créer l'utilisateur
            user = await self.db.get_user(user_id)
            if not user:
                user = await self.db.create_user(
                    user_id,
                    member.name,
                    "0"  # Discord a supprimé les discriminateurs
                )
            
            if user:
                old_level = user.voice_level
                
                # Mettre à jour l'XP et les coins
                await self.db.update_user_xp(user_id, voice_xp=xp_gained)
                await self.db.update_user_coins(user_id, coins_gained)
                
                # Recalculer le niveau
                new_level = self.xp_calc.xp_to_level(user.voice_xp + xp_gained)
                
                # Vérifier si l'utilisateur a monté de niveau
                if new_level > old_level:
                    # Envoyer notification dans un canal général ou par DM
                    channel = member.guild.system_channel
                    if channel:
                        await self.level_manager.handle_level_up(
                            member,
                            channel,
                            old_level,
                            new_level,
                            'voice'
                        )
                
        except Exception as e:
            logger.error(f"Erreur lors du traitement du gain d'XP vocal : {e}")
    
    @tasks.loop(minutes=5)
    async def voice_xp_task(self):
        """Tâche périodique pour donner de l'XP aux utilisateurs en vocal"""
        try:
            now = datetime.utcnow()
            
            for user_id, join_time in list(self.voice_users.items()):
                duration_minutes = (now - join_time).total_seconds() / 60
                
                # Donner de l'XP toutes les 5 minutes d'activité
                if duration_minutes >= 5:
                    # Trouver le membre
                    member = None
                    for guild in self.guilds:
                        member = guild.get_member(int(user_id))
                        if member:
                            break
                    
                    if member:
                        # Calculer XP pour 5 minutes
                        xp_gained = self.xp_calc.calculate_voice_xp(5)
                        coins_gained = 5 * self.config['coin_settings']['coins_per_voice_minute']
                        
                        await self.db.update_user_xp(user_id, voice_xp=xp_gained)
                        await self.db.update_user_coins(user_id, coins_gained)
                        
                        # Reset le timer
                        self.voice_users[user_id] = now
                        
        except Exception as e:
            logger.error(f"Erreur dans la tâche XP vocal : {e}")
    
    @voice_xp_task.before_loop
    async def before_voice_xp_task(self):
        """Attendre que le bot soit prêt avant de démarrer la tâche"""
        await self.wait_until_ready()
    
    async def close(self):
        """Fermeture propre du bot"""
        logger.info("Fermeture du bot...")
        await self.db.close()
        await super().close()
