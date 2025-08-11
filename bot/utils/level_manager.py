"""
Gestionnaire de niveaux et rôles
"""
import discord
import logging

logger = logging.getLogger(__name__)

class LevelManager:
    """Gestionnaire des niveaux et attribution des rôles"""
    
    def __init__(self, config, bot):
        self.config = config
        self.bot = bot
        self.level_roles = config.get('level_roles', {})
    
    async def handle_level_up(self, member, channel, old_level, new_level, xp_type):
        """Traite la montée de niveau d'un utilisateur"""
        try:
            # Créer un embed de félicitations
            embed = discord.Embed(
                title="🎉 Niveau supérieur !",
                description=f"Félicitations {member.mention} !",
                color=discord.Color.gold()
            )
            
            if xp_type == 'text':
                embed.add_field(
                    name="📝 Niveau Textuel",
                    value=f"Niveau {old_level} → **Niveau {new_level}**",
                    inline=False
                )
                role_category = 'text_levels'
            else:
                embed.add_field(
                    name="🎤 Niveau Vocal",
                    value=f"Niveau {old_level} → **Niveau {new_level}**",
                    inline=False
                )
                role_category = 'voice_levels'
            
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.timestamp = discord.utils.utcnow()
            
            # Envoyer le message de félicitations
            await channel.send(embed=embed)
            
            # Attribuer les rôles si configurés
            await self.assign_level_roles(member, new_level, role_category)
            
        except Exception as e:
            logger.error(f"Erreur lors de la gestion de la montée de niveau : {e}")
    
    async def assign_level_roles(self, member, level, role_category):
        """Attribue les rôles correspondants au niveau"""
        try:
            roles_config = self.level_roles.get(role_category, {})
            
            # Vérifier s'il y a un rôle pour ce niveau
            role_name = roles_config.get(str(level))
            if not role_name:
                return
            
            guild = member.guild
            
            # Chercher le rôle existant
            role = discord.utils.get(guild.roles, name=role_name)
            
            # Créer le rôle s'il n'existe pas
            if not role:
                role = await self.create_level_role(guild, role_name, level, role_category)
            
            if role and role not in member.roles:
                await member.add_roles(role, reason=f"Niveau {level} atteint")
                logger.info(f"Rôle '{role_name}' attribué à {member.name}")
                
        except Exception as e:
            logger.error(f"Erreur lors de l'attribution du rôle : {e}")
    
    async def create_level_role(self, guild, role_name, level, role_category):
        """Crée un nouveau rôle de niveau"""
        try:
            # Couleurs selon le type et le niveau
            if role_category == 'text_levels':
                colors = {
                    5: discord.Color.blue(),
                    10: discord.Color.green(),
                    20: discord.Color.orange(),
                    50: discord.Color.purple()
                }
            else:  # voice_levels
                colors = {
                    5: discord.Color.teal(),
                    10: discord.Color.dark_green(),
                    20: discord.Color.dark_orange(),
                    50: discord.Color.dark_purple()
                }
            
            color = colors.get(level, discord.Color.default())
            
            # Créer le rôle
            role = await guild.create_role(
                name=role_name,
                color=color,
                reason=f"Rôle automatique pour niveau {level}"
            )
            
            logger.info(f"Rôle '{role_name}' créé pour le niveau {level}")
            return role
            
        except Exception as e:
            logger.error(f"Erreur lors de la création du rôle : {e}")
            return None
    
    async def sync_user_roles(self, member, text_level, voice_level):
        """Synchronise tous les rôles d'un utilisateur selon ses niveaux"""
        try:
            # Synchroniser les rôles textuels
            await self._sync_category_roles(member, text_level, 'text_levels')
            
            # Synchroniser les rôles vocaux
            await self._sync_category_roles(member, voice_level, 'voice_levels')
            
        except Exception as e:
            logger.error(f"Erreur lors de la synchronisation des rôles : {e}")
    
    async def _sync_category_roles(self, member, user_level, role_category):
        """Synchronise les rôles d'une catégorie pour un utilisateur"""
        try:
            roles_config = self.level_roles.get(role_category, {})
            guild = member.guild
            
            for level_str, role_name in roles_config.items():
                level = int(level_str)
                role = discord.utils.get(guild.roles, name=role_name)
                
                if not role:
                    continue
                
                # L'utilisateur devrait avoir ce rôle
                if user_level >= level:
                    if role not in member.roles:
                        await member.add_roles(role, reason=f"Synchronisation niveau {level}")
                # L'utilisateur ne devrait pas avoir ce rôle
                else:
                    if role in member.roles:
                        await member.remove_roles(role, reason=f"Niveau insuffisant pour {level}")
                        
        except Exception as e:
            logger.error(f"Erreur lors de la synchronisation des rôles de catégorie : {e}")
    
    def get_next_role_info(self, current_level, role_category):
        """Retourne les informations sur le prochain rôle à débloquer"""
        roles_config = self.level_roles.get(role_category, {})
        
        next_roles = []
        for level_str, role_name in roles_config.items():
            level = int(level_str)
            if level > current_level:
                next_roles.append((level, role_name))
        
        if next_roles:
            next_roles.sort(key=lambda x: x[0])
            return next_roles[0]  # Le prochain rôle
        
        return None
