"""
Commandes liées à l'expérience et aux niveaux
"""
import discord
from discord.ext import commands
from discord import app_commands
import logging

logger = logging.getLogger(__name__)

class ExperienceCommands(commands.Cog):
    """Commandes pour l'expérience et les niveaux"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="niveau", description="Affiche votre niveau et expérience")
    async def niveau(self, interaction: discord.Interaction, utilisateur: discord.Member = None):
        """Affiche le niveau d'un utilisateur"""
        try:
            target_user = utilisateur or interaction.user
            user_id = str(target_user.id)
            
            # Récupérer les données utilisateur
            user = await self.bot.db.get_user(user_id)
            if not user:
                if target_user == interaction.user:
                    # Créer l'utilisateur s'il n'existe pas
                    user = await self.bot.db.create_user(
                        user_id,
                        target_user.name,
                        "0"  # Discord a supprimé les discriminateurs
                    )
                else:
                    await interaction.response.send_message(
                        f"{target_user.mention} n'a pas encore d'activité enregistrée.",
                        ephemeral=True
                    )
                    return
            
            if not user:
                await interaction.response.send_message(
                    "Erreur lors de la récupération des données.",
                    ephemeral=True
                )
                return
            
            # Calculer les informations de niveau
            text_info = self.bot.xp_calc.get_level_info(user.text_xp)
            voice_info = self.bot.xp_calc.get_level_info(user.voice_xp)
            
            # Créer l'embed
            embed = discord.Embed(
                title=f"📊 Profil de {target_user.display_name}",
                color=discord.Color.blue()
            )
            
            embed.set_thumbnail(url=target_user.display_avatar.url)
            
            # Niveau textuel
            embed.add_field(
                name="📝 Niveau Textuel",
                value=f"**Niveau {text_info['level']}**\n"
                      f"XP: {user.text_xp:,}\n"
                      f"Progrès: {text_info['progress']}/{text_info['total_needed']} "
                      f"({text_info['percentage']:.1f}%)\n"
                      f"Prochain niveau: {text_info['xp_to_next']} XP",
                inline=True
            )
            
            # Niveau vocal
            embed.add_field(
                name="🎤 Niveau Vocal",
                value=f"**Niveau {voice_info['level']}**\n"
                      f"XP: {user.voice_xp:,}\n"
                      f"Progrès: {voice_info['progress']}/{voice_info['total_needed']} "
                      f"({voice_info['percentage']:.1f}%)\n"
                      f"Prochain niveau: {voice_info['xp_to_next']} XP",
                inline=True
            )
            
            # Coins
            embed.add_field(
                name="💰 Pièces",
                value=f"{user.coins:,} coins",
                inline=True
            )
            
            # Prochains rôles
            next_text_role = self.bot.level_manager.get_next_role_info(
                text_info['level'], 'text_levels'
            )
            next_voice_role = self.bot.level_manager.get_next_role_info(
                voice_info['level'], 'voice_levels'
            )
            
            next_rewards = []
            if next_text_role:
                next_rewards.append(f"📝 Niveau {next_text_role[0]}: {next_text_role[1]}")
            if next_voice_role:
                next_rewards.append(f"🎤 Niveau {next_voice_role[0]}: {next_voice_role[1]}")
            
            if next_rewards:
                embed.add_field(
                    name="🎁 Prochaines récompenses",
                    value="\n".join(next_rewards),
                    inline=False
                )
            
            embed.timestamp = discord.utils.utcnow()
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            logger.error(f"Erreur dans la commande niveau : {e}")
            await interaction.response.send_message(
                "Une erreur est survenue lors de la récupération des informations.",
                ephemeral=True
            )
    
    @app_commands.command(name="classement", description="Affiche le classement des utilisateurs")
    @app_commands.choices(type=[
        app_commands.Choice(name="Textuel", value="text"),
        app_commands.Choice(name="Vocal", value="voice")
    ])
    async def classement(self, interaction: discord.Interaction, type: str = "text"):
        """Affiche le classement"""
        try:
            # Récupérer le classement
            is_voice = (type == "voice")
            leaderboard = await self.bot.db.get_leaderboard(by_voice=is_voice, limit=10)
            
            if not leaderboard:
                await interaction.response.send_message(
                    "Aucune donnée de classement disponible.",
                    ephemeral=True
                )
                return
            
            # Créer l'embed
            title = "🎤 Classement Vocal" if is_voice else "📝 Classement Textuel"
            embed = discord.Embed(
                title=title,
                color=discord.Color.gold()
            )
            
            # Emojis pour les positions
            position_emojis = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
            
            description = ""
            for i, (username, level, xp) in enumerate(leaderboard):
                emoji = position_emojis[i] if i < len(position_emojis) else f"{i+1}."
                description += f"{emoji} **{username}** - Niveau {level} ({xp:,} XP)\n"
            
            embed.description = description
            embed.timestamp = discord.utils.utcnow()
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            logger.error(f"Erreur dans la commande classement : {e}")
            await interaction.response.send_message(
                "Une erreur est survenue lors de la récupération du classement.",
                ephemeral=True
            )
    
    @app_commands.command(name="coins", description="Affiche vos pièces")
    async def coins(self, interaction: discord.Interaction):
        """Affiche les pièces de l'utilisateur"""
        try:
            user_id = str(interaction.user.id)
            user = await self.bot.db.get_user(user_id)
            
            if not user:
                user = await self.bot.db.create_user(
                    user_id,
                    interaction.user.name,
                    "0"  # Discord a supprimé les discriminateurs
                )
            
            if user:
                embed = discord.Embed(
                    title="💰 Vos Pièces",
                    description=f"Vous avez **{user.coins:,}** coins",
                    color=discord.Color.gold()
                )
                embed.set_thumbnail(url=interaction.user.display_avatar.url)
            else:
                embed = discord.Embed(
                    title="❌ Erreur",
                    description="Impossible de récupérer vos données",
                    color=discord.Color.red()
                )
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            logger.error(f"Erreur dans la commande coins : {e}")
            await interaction.response.send_message(
                "Une erreur est survenue.",
                ephemeral=True
            )
    
    @app_commands.command(name="daily", description="Récupérer votre bonus quotidien de pièces")
    async def daily(self, interaction: discord.Interaction):
        """Commande pour récupérer le bonus quotidien"""
        try:
            user_id = str(interaction.user.id)
            
            # Vérifier si l'utilisateur existe
            user = await self.bot.db.get_user(user_id)
            if not user:
                user = await self.bot.db.create_user(
                    user_id,
                    interaction.user.name,
                    "0"  # Discord a supprimé les discriminateurs
                )
            
            if not user:
                await interaction.response.send_message(
                    "Erreur lors de la récupération des données.",
                    ephemeral=True
                )
                return
            
            # Vérifier si le bonus quotidien est disponible
            can_claim = await self.bot.db.check_daily_bonus(user_id)
            
            if not can_claim:
                embed = discord.Embed(
                    title="⏰ Bonus quotidien déjà récupéré",
                    description="Vous avez déjà récupéré votre bonus quotidien !\n"
                               "Revenez dans 24 heures pour le prochain bonus.",
                    color=discord.Color.orange()
                )
                embed.set_thumbnail(url=interaction.user.display_avatar.url)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            # Récupérer le bonus
            daily_amount = self.bot.config['coin_settings']['daily_bonus']
            new_total = await self.bot.db.claim_daily_bonus(user_id, daily_amount)
            
            if new_total is not None:
                embed = discord.Embed(
                    title="🎁 Bonus quotidien récupéré !",
                    description=f"Vous avez reçu **{daily_amount:,}** pièces !\n"
                               f"Total : **{new_total:,}** pièces",
                    color=discord.Color.green()
                )
                embed.set_thumbnail(url=interaction.user.display_avatar.url)
                embed.add_field(
                    name="💡 Astuce",
                    value="Revenez demain pour un nouveau bonus !",
                    inline=False
                )
            else:
                embed = discord.Embed(
                    title="❌ Erreur",
                    description="Impossible de récupérer le bonus quotidien.",
                    color=discord.Color.red()
                )
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            logger.error(f"Erreur dans la commande daily : {e}")
            await interaction.response.send_message(
                "Une erreur est survenue.",
                ephemeral=True
            )

async def setup(bot):
    """Charge le cog"""
    await bot.add_cog(ExperienceCommands(bot))
