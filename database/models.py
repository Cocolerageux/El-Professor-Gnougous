"""
Modèles de base de données pour le bot Discord
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    """Modèle pour les utilisateurs Discord"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    discord_id = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    discriminator = Column(String, nullable=False)
    
    # Expérience textuelle
    text_xp = Column(Integer, default=0)
    text_level = Column(Integer, default=1)
    
    # Expérience vocale
    voice_xp = Column(Integer, default=0)
    voice_level = Column(Integer, default=1)
    
    # Système de monnaie
    coins = Column(Integer, default=0)
    
    # Timestamps
    last_text_xp = Column(DateTime, default=datetime.utcnow)
    last_voice_xp = Column(DateTime, default=datetime.utcnow)
    joined_voice_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    purchases = relationship("Purchase", back_populates="user")
    inventory_items = relationship("UserInventory", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.username}#{self.discriminator}>"

class ShopItem(Base):
    """Modèle pour les objets de la boutique"""
    __tablename__ = 'shop_items'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Integer, nullable=False)
    
    # Conditions de déblocage
    required_text_level = Column(Integer, default=0)
    required_voice_level = Column(Integer, default=0)
    
    # Configuration
    is_role = Column(Boolean, default=False)
    role_id = Column(String, nullable=True)  # ID du rôle Discord si c'est un rôle
    is_active = Column(Boolean, default=True)
    is_consumable = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    purchases = relationship("Purchase", back_populates="item")
    inventory_items = relationship("UserInventory", back_populates="item")
    
    def __repr__(self):
        return f"<ShopItem {self.name}>"

class Purchase(Base):
    """Modèle pour l'historique des achats"""
    __tablename__ = 'purchases'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('shop_items.id'), nullable=False)
    price_paid = Column(Integer, nullable=False)
    purchased_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    user = relationship("User", back_populates="purchases")
    item = relationship("ShopItem", back_populates="purchases")
    
    def __repr__(self):
        return f"<Purchase {self.user.username} -> {self.item.name}>"

class UserInventory(Base):
    """Modèle pour l'inventaire des utilisateurs"""
    __tablename__ = 'user_inventory'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('shop_items.id'), nullable=False)
    quantity = Column(Integer, default=1)
    acquired_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    user = relationship("User", back_populates="inventory_items")
    item = relationship("ShopItem", back_populates="inventory_items")
    
    def __repr__(self):
        return f"<UserInventory {self.user.username} has {self.quantity}x {self.item.name}>"

class GuildConfig(Base):
    """Configuration par serveur Discord"""
    __tablename__ = 'guild_config'
    
    id = Column(Integer, primary_key=True)
    guild_id = Column(String, unique=True, nullable=False)
    
    # Canaux spéciaux
    level_up_channel_id = Column(String, nullable=True)
    welcome_channel_id = Column(String, nullable=True)
    
    # Configuration XP
    xp_enabled = Column(Boolean, default=True)
    voice_xp_enabled = Column(Boolean, default=True)
    text_xp_enabled = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<GuildConfig {self.guild_id}>"
