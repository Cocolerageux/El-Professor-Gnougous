"""
Commandes d'administration
"""
import discord
from discord.ext import commands
from discord import app_commands
import logging

logger = logging.getLogger(__name__)

class AdminCommands(commands.Cog):
    """Commandes d'administration pour les modérateurs"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="admin_give_xp", description="[ADMIN] Donne de l'XP à un utilisateur")
    @app_commands.describe(
        utilisateur="L'utilisateur à qui donner l'XP",
        type_xp="Type d'XP à donner",
        amount="Quantité d'XP à donner"
    )
    @app_commands.choices(type_xp=[
        app_commands.Choice(name="Textuel", value="text"),
        app_commands.Choice(name="Vocal", value="voice")
    ])
    async def admin_give_xp(
        self, 
        interaction: discord.Interaction, 
        utilisateur: discord.Member, 
        type_xp: str, 
        amount: int
    ):
        """Donne de l'XP à un utilisateur (admin only)"""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Vous devez être administrateur pour utiliser cette commande.",
                ephemeral=True
            )
            return
        
        try:
            user_id = str(utilisateur.id)
            user = await self.bot.db.get_user(user_id)
            
            if not user:
                user = await self.bot.db.create_user(
                    user_id,
                    utilisateur.name,
                    "0"  # Discord a supprimé les discriminateurs
                )
            
            if not user:
                await interaction.response.send_message(
                    "Erreur lors de la récupération des données utilisateur.",
                    ephemeral=True
                )
                return
            
            # Donner l'XP
            if type_xp == "text":
                await self.bot.db.update_user_xp(user_id, text_xp=amount)
            else:
                await self.bot.db.update_user_xp(user_id, voice_xp=amount)
            
            embed = discord.Embed(
                title="✅ XP Ajouté",
                description=f"{amount} XP {type_xp} ajouté à {utilisateur.mention}",
                color=discord.Color.green()
            )
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            logger.error(f"Erreur dans la commande admin_give_xp : {e}")
            await interaction.response.send_message(
                "Une erreur est survenue.",
                ephemeral=True
            )
    
    @app_commands.command(name="admin_give_coins", description="[ADMIN] Donne des pièces à un utilisateur")
    @app_commands.describe(
        utilisateur="L'utilisateur à qui donner les pièces",
        amount="Quantité de pièces à donner"
    )
    async def admin_give_coins(
        self, 
        interaction: discord.Interaction, 
        utilisateur: discord.Member, 
        amount: int
    ):
        """Donne des pièces à un utilisateur (admin only)"""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Vous devez être administrateur pour utiliser cette commande.",
                ephemeral=True
            )
            return
        
        try:
            user_id = str(utilisateur.id)
            user = await self.bot.db.get_user(user_id)
            
            if not user:
                user = await self.bot.db.create_user(
                    user_id,
                    utilisateur.name,
                    "0"  # Discord a supprimé les discriminateurs
                )
            
            if not user:
                await interaction.response.send_message(
                    "Erreur lors de la récupération des données utilisateur.",
                    ephemeral=True
                )
                return
            
            # Donner les pièces
            await self.bot.db.update_user_coins(user_id, amount)
            
            embed = discord.Embed(
                title="✅ Pièces Ajoutées",
                description=f"{amount:,} pièces ajoutées à {utilisateur.mention}",
                color=discord.Color.gold()
            )
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            logger.error(f"Erreur dans la commande admin_give_coins : {e}")
            await interaction.response.send_message(
                "Une erreur est survenue.",
                ephemeral=True
            )
    
    @app_commands.command(name="admin_reset_user", description="[ADMIN] Remet à zéro les données d'un utilisateur")
    @app_commands.describe(utilisateur="L'utilisateur à remettre à zéro")
    async def admin_reset_user(self, interaction: discord.Interaction, utilisateur: discord.Member):
        """Remet à zéro les données d'un utilisateur (admin only)"""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Vous devez être administrateur pour utiliser cette commande.",
                ephemeral=True
            )
            return
        
        try:
            user_id = str(utilisateur.id)
            
            # TODO: Implémenter la remise à zéro des données
            # Pour l'instant, on simule en donnant XP négatif pour remettre à 0
            user = await self.bot.db.get_user(user_id)
            if user:
                await self.bot.db.update_user_xp(user_id, text_xp=-user.text_xp)
                await self.bot.db.update_user_xp(user_id, voice_xp=-user.voice_xp)
                await self.bot.db.update_user_coins(user_id, -user.coins)
            
            embed = discord.Embed(
                title="✅ Utilisateur Remis à Zéro",
                description=f"Les données de {utilisateur.mention} ont été remises à zéro.",
                color=discord.Color.orange()
            )
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            logger.error(f"Erreur dans la commande admin_reset_user : {e}")
            await interaction.response.send_message(
                "Une erreur est survenue.",
                ephemeral=True
            )
    
    @app_commands.command(name="admin_sync_roles", description="[ADMIN] Synchronise les rôles d'un utilisateur")
    @app_commands.describe(utilisateur="L'utilisateur dont synchroniser les rôles")
    async def admin_sync_roles(self, interaction: discord.Interaction, utilisateur: discord.Member):
        """Synchronise les rôles d'un utilisateur selon ses niveaux (admin only)"""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Vous devez être administrateur pour utiliser cette commande.",
                ephemeral=True
            )
            return
        
        try:
            user_id = str(utilisateur.id)
            user = await self.bot.db.get_user(user_id)
            
            if not user:
                await interaction.response.send_message(
                    f"{utilisateur.mention} n'a pas de données enregistrées.",
                    ephemeral=True
                )
                return
            
            # Calculer les niveaux
            text_level = self.bot.xp_calc.xp_to_level(user.text_xp)
            voice_level = self.bot.xp_calc.xp_to_level(user.voice_xp)
            
            # Synchroniser les rôles
            await self.bot.level_manager.sync_user_roles(utilisateur, text_level, voice_level)
            
            embed = discord.Embed(
                title="✅ Rôles Synchronisés",
                description=f"Les rôles de {utilisateur.mention} ont été synchronisés.\n"
                           f"Niveau textuel: {text_level} • Niveau vocal: {voice_level}",
                color=discord.Color.blue()
            )
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            logger.error(f"Erreur dans la commande admin_sync_roles : {e}")
            await interaction.response.send_message(
                "Une erreur est survenue.",
                ephemeral=True
            )

async def setup(bot):
    """Charge le cog"""
    await bot.add_cog(AdminCommands(bot))
