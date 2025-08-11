"""
Commandes pour la boutique
"""
import discord
from discord.ext import commands
from discord import app_commands
import logging

logger = logging.getLogger(__name__)

class ShopCommands(commands.Cog):
    """Commandes pour la boutique et les achats"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="boutique", description="Affiche la boutique")
    async def boutique(self, interaction: discord.Interaction):
        """Affiche les objets disponibles dans la boutique"""
        try:
            logger.info(f"Commande boutique appelée par {interaction.user.name}")
            user_id = str(interaction.user.id)
            user = await self.bot.db.get_user(user_id)
            
            logger.info(f"Utilisateur récupéré: {user.username if user else 'None'}")
            
            if not user:
                user = await self.bot.db.create_user(
                    user_id,
                    interaction.user.name,
                    "0"  # Discord a supprimé les discriminateurs
                )
            
            if not user:
                await interaction.response.send_message(
                    "Erreur lors de la récupération de vos données.",
                    ephemeral=True
                )
                return
            
            # Récupérer les objets de la boutique
            text_level = user.text_level
            voice_level = user.voice_level
            logger.info(f"Niveaux utilisateur: texte={text_level}, vocal={voice_level}")
            
            shop_items = await self.bot.db.get_shop_items(text_level, voice_level)
            logger.info(f"Articles boutique récupérés: {len(shop_items)}")
            
            if not shop_items:
                await interaction.response.send_message(
                    "Aucun objet disponible dans la boutique pour votre niveau.",
                    ephemeral=True
                )
                return
            
            # Créer l'embed de la boutique
            embed = discord.Embed(
                title="🛒 Boutique",
                description=f"Vos pièces: **{user.coins:,}** 💰",
                color=discord.Color.green()
            )
            
            for item_data in shop_items:
                item_id = item_data[0]
                name = item_data[1]
                description = item_data[2]
                price = item_data[3]
                req_text = item_data[4]
                req_voice = item_data[5]
                is_role = bool(item_data[6])
                is_consumable = bool(item_data[9])
                
                # Icône selon le type d'objet
                icon = "👑" if is_role else "🎁" if is_consumable else "⭐"
                
                # Vérifier si l'utilisateur peut se l'offrir
                can_afford = user.coins >= price
                price_text = f"💰 {price:,} coins" if can_afford else f"❌ {price:,} coins"
                
                requirements = []
                if req_text > 0:
                    requirements.append(f"📝 Niveau {req_text}")
                if req_voice > 0:
                    requirements.append(f"🎤 Niveau {req_voice}")
                
                req_text_display = " • ".join(requirements) if requirements else "Aucun prérequis"
                
                embed.add_field(
                    name=f"{icon} {name}",
                    value=f"{description}\n"
                          f"Prix: {price_text}\n"
                          f"Prérequis: {req_text_display}\n"
                          f"ID: `{item_id}`",
                    inline=True
                )
            
            embed.set_footer(text="Utilisez /acheter <id> pour acheter un objet")
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            logger.error(f"Erreur dans la commande boutique : {e}")
            await interaction.response.send_message(
                "Une erreur est survenue lors de l'affichage de la boutique.",
                ephemeral=True
            )
    
    @app_commands.command(name="acheter", description="Achète un objet de la boutique")
    async def acheter(self, interaction: discord.Interaction, item_id: int):
        """Achète un objet de la boutique"""
        try:
            await interaction.response.defer()
            
            user_id = str(interaction.user.id)
            user = await self.bot.db.get_user(user_id)
            
            if not user:
                await interaction.followup.send(
                    "Erreur lors de la récupération de vos données.",
                    ephemeral=True
                )
                return
            
            # Récupérer l'objet
            text_level = user.text_level
            voice_level = user.voice_level
            
            shop_items = await self.bot.db.get_shop_items(text_level, voice_level)
            
            # Trouver l'objet demandé
            target_item = None
            for item_data in shop_items:
                if item_data[0] == item_id:  # ID de l'objet
                    target_item = item_data
                    break
            
            if not target_item:
                await interaction.followup.send(
                    "Objet non trouvé ou non disponible pour votre niveau.",
                    ephemeral=True
                )
                return
            
            item_name = target_item[1]
            item_price = target_item[3]
            is_role = bool(target_item[6])
            role_id = target_item[7]
            
            # Vérifier si l'utilisateur a assez de pièces
            if user.coins < item_price:
                await interaction.followup.send(
                    f"Vous n'avez pas assez de pièces pour acheter **{item_name}**.\n"
                    f"Prix: {item_price:,} coins • Vos pièces: {user.coins:,} coins",
                    ephemeral=True
                )
                return
            
            # Traitement de l'achat
            success = await self.process_purchase(interaction.user, item_id, target_item, user)
            
            if success:
                # Déduire les pièces
                await self.bot.db.update_user_coins(user_id, -item_price)
                
                embed = discord.Embed(
                    title="✅ Achat réussi !",
                    description=f"Vous avez acheté **{item_name}** pour {item_price:,} coins.",
                    color=discord.Color.green()
                )
                
                new_balance = user.coins - item_price
                embed.add_field(
                    name="💰 Nouveau solde",
                    value=f"{new_balance:,} coins",
                    inline=True
                )
                
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(
                    "Erreur lors du traitement de l'achat.",
                    ephemeral=True
                )
            
        except Exception as e:
            logger.error(f"Erreur dans la commande acheter : {e}")
            await interaction.followup.send(
                "Une erreur est survenue lors de l'achat.",
                ephemeral=True
            )
    
    async def process_purchase(self, user, item_id, item_data, user_data):
        """Traite l'achat d'un objet"""
        try:
            item_name = item_data[1]
            is_role = bool(item_data[6])
            role_id = item_data[7]
            
            # Si c'est un rôle, l'attribuer
            if is_role and role_id:
                guild = user.guild
                role = guild.get_role(int(role_id)) if role_id.isdigit() else discord.utils.get(guild.roles, name=item_name)
                
                if role:
                    await user.add_roles(role, reason=f"Achat dans la boutique : {item_name}")
                    logger.info(f"Rôle {item_name} attribué à {user.name}")
                else:
                    logger.warning(f"Rôle {item_name} introuvable pour l'achat")
                    return False
            
            # TODO: Ajouter l'objet à l'inventaire si ce n'est pas un rôle
            # TODO: Enregistrer l'achat dans l'historique
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement de l'achat : {e}")
            return False
    
    @app_commands.command(name="inventaire", description="Affiche votre inventaire")
    async def inventaire(self, interaction: discord.Interaction):
        """Affiche l'inventaire de l'utilisateur"""
        try:
            user_id = str(interaction.user.id)
            user = await self.bot.db.get_user(user_id)
            
            if not user:
                await interaction.response.send_message(
                    "Vous n'avez pas encore d'activité enregistrée.",
                    ephemeral=True
                )
                return
            
            # Récupérer les rôles de l'utilisateur qui correspondent aux objets de boutique
            embed = discord.Embed(
                title="🎒 Votre Inventaire",
                description="Voici vos objets et rôles obtenus :",
                color=discord.Color.blue()
            )
            
            # Afficher les rôles liés aux niveaux
            level_roles = []
            text_level = user.text_level
            voice_level = user.voice_level
            
            # Rôles textuels
            text_roles_config = self.bot.config.get('level_roles', {}).get('text_levels', {})
            for level_str, role_name in text_roles_config.items():
                if text_level >= int(level_str):
                    level_roles.append(f"📝 {role_name} (Niveau {level_str})")
            
            # Rôles vocaux
            voice_roles_config = self.bot.config.get('level_roles', {}).get('voice_levels', {})
            for level_str, role_name in voice_roles_config.items():
                if voice_level >= int(level_str):
                    level_roles.append(f"🎤 {role_name} (Niveau {level_str})")
            
            if level_roles:
                embed.add_field(
                    name="👑 Rôles de Niveau",
                    value="\n".join(level_roles),
                    inline=False
                )
            
            # TODO: Ajouter l'inventaire des objets achetés
            
            embed.add_field(
                name="💰 Pièces",
                value=f"{user.coins:,} coins",
                inline=True
            )
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            logger.error(f"Erreur dans la commande inventaire : {e}")
            await interaction.response.send_message(
                "Une erreur est survenue lors de l'affichage de l'inventaire.",
                ephemeral=True
            )

async def setup(bot):
    """Charge le cog"""
    await bot.add_cog(ShopCommands(bot))
