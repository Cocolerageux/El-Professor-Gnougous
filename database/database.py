"""
Gestionnaire de base de données
"""
import aiosqlite
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from database.models import Base, User, ShopItem, Purchase, UserInventory, GuildConfig
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Gestionnaire principal de la base de données"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = None
        self.async_engine = None
        self.Session = None
        self.AsyncSession = None
        
    async def initialize(self):
        """Initialise la base de données"""
        try:
            # Créer les tables avec SQLite pur
            db_path = self.database_url.replace('sqlite:///', '')
            
            async with aiosqlite.connect(db_path) as db:
                # Créer la table users
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        discord_id TEXT UNIQUE NOT NULL,
                        username TEXT NOT NULL,
                        discriminator TEXT NOT NULL,
                        text_xp INTEGER DEFAULT 0,
                        text_level INTEGER DEFAULT 1,
                        voice_xp INTEGER DEFAULT 0,
                        voice_level INTEGER DEFAULT 1,
                        coins INTEGER DEFAULT 0,
                        last_daily TIMESTAMP DEFAULT NULL,
                        last_text_xp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_voice_xp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        joined_voice_at TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Créer la table shop_items
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS shop_items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        price INTEGER NOT NULL,
                        required_text_level INTEGER DEFAULT 0,
                        required_voice_level INTEGER DEFAULT 0,
                        is_role BOOLEAN DEFAULT 0,
                        role_id TEXT,
                        is_active BOOLEAN DEFAULT 1,
                        is_consumable BOOLEAN DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Créer la table purchases
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS purchases (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        item_id INTEGER NOT NULL,
                        price_paid INTEGER NOT NULL,
                        purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id),
                        FOREIGN KEY (item_id) REFERENCES shop_items (id)
                    )
                """)
                
                await db.commit()
            
            # Initialiser les données par défaut
            await self.initialize_default_data()
            
            logger.info("Base de données initialisée avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de la base de données : {e}")
            raise
    
    async def initialize_default_data(self):
        """Initialise les données par défaut"""
        try:
            async with aiosqlite.connect(self.database_url.replace('sqlite:///', '')) as db:
                # Vérifier si des objets existent déjà
                async with db.execute("SELECT COUNT(*) FROM shop_items") as cursor:
                    row = await cursor.fetchone()
                    count = row[0] if row else 0
                
                if count == 0:
                    # Créer des objets de boutique par défaut
                    default_items = [
                        ("Badge Nouveau", "Badge pour les nouveaux membres", 25, 1, 0, 0, "", 1, 0),
                        ("Emoji Spécial", "Accès à un emoji personnalisé", 50, 1, 1, 0, "", 1, 0),
                        ("Badge Débutant", "Un badge pour montrer votre progression", 100, 3, 0, 0, "", 1, 0),
                        ("Couleur Pseudo", "Accès à une couleur de pseudo spéciale", 200, 5, 3, 1, "", 1, 0),
                        ("Boost XP", "Double l'XP gagné pendant 1 heure", 150, 8, 5, 0, "", 1, 1),
                        ("Statut VIP", "Accès au statut VIP avec privilèges spéciaux", 500, 15, 10, 1, "", 1, 0),
                        ("Badge Expert", "Badge pour les experts", 800, 25, 20, 0, "", 1, 0),
                        ("Rôle Légendaire", "Rôle exclusif pour les légendes", 1500, 50, 40, 1, "", 1, 0)
                    ]
                    
                    for item in default_items:
                        await db.execute(
                            """INSERT INTO shop_items 
                               (name, description, price, required_text_level, required_voice_level, 
                                is_role, role_id, is_active, is_consumable) 
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            item
                        )
                    
                    await db.commit()
                    logger.info("Objets de boutique par défaut créés")
                    
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation des données par défaut : {e}")
    
    async def get_user(self, discord_id: str) -> User:
        """Récupère un utilisateur"""
        try:
            # Utiliser une connexion SQLite directe pour plus de simplicité
            async with aiosqlite.connect(self.database_url.replace('sqlite:///', '')) as db:
                async with db.execute(
                    "SELECT * FROM users WHERE discord_id = ?", (discord_id,)
                ) as cursor:
                    row = await cursor.fetchone()
                    
                    if row:
                        user = User()
                        user.id = row[0]
                        user.discord_id = row[1] 
                        user.username = row[2]
                        user.discriminator = row[3]
                        user.text_xp = row[4]
                        user.text_level = row[5]
                        user.voice_xp = row[6]
                        user.voice_level = row[7]
                        user.coins = row[8]
                        return user
                    else:
                        return None
                        
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'utilisateur : {e}")
            return None
    
    async def create_user(self, discord_id: str, username: str, discriminator: str) -> User:
        """Crée un nouvel utilisateur"""
        try:
            async with aiosqlite.connect(self.database_url.replace('sqlite:///', '')) as db:
                await db.execute(
                    """INSERT INTO users (discord_id, username, discriminator, text_xp, text_level, 
                       voice_xp, voice_level, coins) VALUES (?, ?, ?, 0, 1, 0, 1, 0)""",
                    (discord_id, username, discriminator)
                )
                await db.commit()
                
                # Récupérer l'utilisateur créé
                return await self.get_user(discord_id)
                
        except Exception as e:
            logger.error(f"Erreur lors de la création de l'utilisateur : {e}")
            return None
    
    async def update_user_xp(self, discord_id: str, text_xp: int = 0, voice_xp: int = 0):
        """Met à jour l'XP d'un utilisateur et recalcule les niveaux"""
        try:
            async with aiosqlite.connect(self.database_url.replace('sqlite:///', '')) as db:
                # Récupérer l'XP actuel
                async with db.execute(
                    "SELECT text_xp, voice_xp FROM users WHERE discord_id = ?", (discord_id,)
                ) as cursor:
                    row = await cursor.fetchone()
                    if not row:
                        return
                    
                    current_text_xp, current_voice_xp = row
                
                # Calculer les nouveaux XP et niveaux
                new_text_xp = current_text_xp + text_xp
                new_voice_xp = current_voice_xp + voice_xp
                
                # Calculer les niveaux (formule simple : level = sqrt(xp/100) + 1)
                import math
                new_text_level = int(math.sqrt(new_text_xp / 100)) + 1
                new_voice_level = int(math.sqrt(new_voice_xp / 100)) + 1
                
                # Mettre à jour en une seule requête
                await db.execute(
                    """UPDATE users SET 
                       text_xp = ?, text_level = ?, 
                       voice_xp = ?, voice_level = ?,
                       updated_at = CURRENT_TIMESTAMP
                       WHERE discord_id = ?""",
                    (new_text_xp, new_text_level, new_voice_xp, new_voice_level, discord_id)
                )
                
                await db.commit()
                
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de l'XP : {e}")
    
    async def update_user_coins(self, discord_id: str, coins: int):
        """Met à jour les pièces d'un utilisateur"""
        try:
            async with aiosqlite.connect(self.database_url.replace('sqlite:///', '')) as db:
                await db.execute(
                    "UPDATE users SET coins = coins + ? WHERE discord_id = ?",
                    (coins, discord_id)
                )
                await db.commit()
                
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour des pièces : {e}")
    
    async def get_leaderboard(self, by_voice: bool = False, limit: int = 10):
        """Récupère le classement"""
        try:
            async with aiosqlite.connect(self.database_url.replace('sqlite:///', '')) as db:
                if by_voice:
                    async with db.execute(
                        "SELECT username, voice_level, voice_xp FROM users ORDER BY voice_level DESC, voice_xp DESC LIMIT ?",
                        (limit,)
                    ) as cursor:
                        return await cursor.fetchall()
                else:
                    async with db.execute(
                        "SELECT username, text_level, text_xp FROM users ORDER BY text_level DESC, text_xp DESC LIMIT ?",
                        (limit,)
                    ) as cursor:
                        return await cursor.fetchall()
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du classement : {e}")
            return []
    
    async def get_shop_items(self, user_text_level: int = 0, user_voice_level: int = 0):
        """Récupère les objets de la boutique disponibles pour un utilisateur"""
        try:
            async with aiosqlite.connect(self.database_url.replace('sqlite:///', '')) as db:
                async with db.execute(
                    """SELECT * FROM shop_items 
                       WHERE is_active = 1 
                       AND required_text_level <= ? 
                       AND required_voice_level <= ?
                       ORDER BY price ASC""",
                    (user_text_level, user_voice_level)
                ) as cursor:
                    return await cursor.fetchall()
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des objets de boutique : {e}")
            return []
    
    async def purchase_item(self, user_id: str, item_id: int, price: int):
        """Effectue l'achat d'un objet"""
        try:
            async with aiosqlite.connect(self.database_url.replace('sqlite:///', '')) as db:
                # Déduire les pièces
                await db.execute(
                    "UPDATE users SET coins = coins - ? WHERE discord_id = ?",
                    (price, user_id)
                )
                
                # Enregistrer l'achat
                await db.execute(
                    """INSERT INTO purchases (user_id, item_id, price_paid) 
                       VALUES ((SELECT id FROM users WHERE discord_id = ?), ?, ?)""",
                    (user_id, item_id, price)
                )
                
                await db.commit()
                return True
                
        except Exception as e:
            logger.error(f"Erreur lors de l'achat d'objet : {e}")
            return False
    
    async def get_user_purchases(self, user_id: str):
        """Récupère l'historique des achats d'un utilisateur"""
        try:
            async with aiosqlite.connect(self.database_url.replace('sqlite:///', '')) as db:
                async with db.execute(
                    """SELECT p.id, s.name, p.price_paid, p.purchased_at 
                       FROM purchases p 
                       JOIN shop_items s ON p.item_id = s.id 
                       JOIN users u ON p.user_id = u.id 
                       WHERE u.discord_id = ? 
                       ORDER BY p.purchased_at DESC""",
                    (user_id,)
                ) as cursor:
                    return await cursor.fetchall()
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des achats : {e}")
            return []
    
    async def close(self):
        """Ferme les connexions à la base de données"""
        if self.async_engine:
            await self.async_engine.dispose()
        if self.engine:
            self.engine.dispose()
    
    async def get_all_users(self):
        """Récupère tous les utilisateurs"""
        try:
            async with aiosqlite.connect(self.database_url.replace('sqlite:///', '')) as db:
                async with db.execute(
                    "SELECT discord_id, username, text_level, voice_level, coins FROM users ORDER BY text_level DESC"
                ) as cursor:
                    return await cursor.fetchall()
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de tous les utilisateurs : {e}")
            return []
    
    async def add_shop_item(self, name: str, description: str, price: int, 
                           required_text_level: int = 0, required_voice_level: int = 0,
                           is_role: bool = False, role_id: str = None, 
                           is_consumable: bool = False):
        """Ajoute un nouvel article à la boutique"""
        try:
            async with aiosqlite.connect(self.database_url.replace('sqlite:///', '')) as db:
                cursor = await db.execute(
                    """INSERT INTO shop_items 
                       (name, description, price, required_text_level, required_voice_level, 
                        is_role, role_id, is_consumable) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (name, description, price, required_text_level, required_voice_level,
                     is_role, role_id, is_consumable)
                )
                
                await db.commit()
                return cursor.lastrowid
                
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout d'un article : {e}")
            return None
    
    async def update_shop_item(self, item_id: int, name: str = None, description: str = None, 
                              price: int = None, required_text_level: int = None, 
                              required_voice_level: int = None, is_active: bool = None):
        """Met à jour un article de la boutique"""
        try:
            updates = []
            params = []
            
            if name is not None:
                updates.append("name = ?")
                params.append(name)
            if description is not None:
                updates.append("description = ?")
                params.append(description)
            if price is not None:
                updates.append("price = ?")
                params.append(price)
            if required_text_level is not None:
                updates.append("required_text_level = ?")
                params.append(required_text_level)
            if required_voice_level is not None:
                updates.append("required_voice_level = ?")
                params.append(required_voice_level)
            if is_active is not None:
                updates.append("is_active = ?")
                params.append(is_active)
            
            if not updates:
                return False
            
            params.append(item_id)
            
            async with aiosqlite.connect(self.database_url.replace('sqlite:///', '')) as db:
                await db.execute(
                    f"UPDATE shop_items SET {', '.join(updates)} WHERE id = ?",
                    params
                )
                await db.commit()
                return True
                
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de l'article : {e}")
            return False
    
    async def delete_shop_item(self, item_id: int):
        """Supprime un article de la boutique"""
        try:
            async with aiosqlite.connect(self.database_url.replace('sqlite:///', '')) as db:
                await db.execute("DELETE FROM shop_items WHERE id = ?", (item_id,))
                await db.commit()
                return True
                
        except Exception as e:
            logger.error(f"Erreur lors de la suppression de l'article : {e}")
            return False
    
    async def check_daily_bonus(self, discord_id: str):
        """Vérifie si l'utilisateur peut récupérer son bonus quotidien"""
        try:
            async with aiosqlite.connect(self.database_url.replace('sqlite:///', '')) as db:
                cursor = await db.execute(
                    "SELECT last_daily FROM users WHERE discord_id = ?",
                    (discord_id,)
                )
                row = await cursor.fetchone()
                
                if not row or not row[0]:
                    return True  # Jamais récupéré de bonus
                
                # Vérifier si 24h ont passé
                from datetime import datetime, timedelta
                last_daily = datetime.fromisoformat(row[0])
                now = datetime.now()
                
                return (now - last_daily) >= timedelta(hours=24)
                
        except Exception as e:
            logger.error(f"Erreur lors de la vérification du daily : {e}")
            return False
    
    async def claim_daily_bonus(self, discord_id: str, bonus_amount: int):
        """Récupère le bonus quotidien"""
        try:
            from datetime import datetime
            
            async with aiosqlite.connect(self.database_url.replace('sqlite:///', '')) as db:
                # Mettre à jour les coins et la date du dernier bonus
                await db.execute(
                    """UPDATE users 
                       SET coins = coins + ?, 
                           last_daily = ?,
                           updated_at = CURRENT_TIMESTAMP 
                       WHERE discord_id = ?""",
                    (bonus_amount, datetime.now().isoformat(), discord_id)
                )
                await db.commit()
                
                # Récupérer le nouveau total de coins
                cursor = await db.execute(
                    "SELECT coins FROM users WHERE discord_id = ?",
                    (discord_id,)
                )
                row = await cursor.fetchone()
                return row[0] if row else 0
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du daily : {e}")
            return None
