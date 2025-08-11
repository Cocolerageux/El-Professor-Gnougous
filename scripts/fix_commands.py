"""
🔧 SCRIPT DE RÉPARATION DES COMMANDES DISCORD
==============================================

Force la resynchronisation des commandes slash.
"""

import asyncio
import discord
from discord.ext import commands
import json
import logging

async def force_sync_commands():
    """Force la synchronisation des commandes"""
    
    # Charger la configuration
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
    print("🔄 RESYNCHRONISATION DES COMMANDES")
    print("=" * 40)
    
    # Configuration des intents
    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True
    intents.members = True
    
    bot = commands.Bot(
        command_prefix='!',
        intents=intents,
        help_command=None
    )
    
    @bot.event
    async def on_ready():
        print(f"✅ Bot connecté : {bot.user}")
        
        # Ajouter quelques commandes de test simples
        @bot.tree.command(name="ping", description="Test de connexion")
        async def ping(interaction: discord.Interaction):
            await interaction.response.send_message("🏓 Pong !", ephemeral=True)
        
        @bot.tree.command(name="niveau", description="Voir votre niveau")
        async def niveau(interaction: discord.Interaction):
            await interaction.response.send_message("📊 Votre niveau sera affiché ici", ephemeral=True)
        
        @bot.tree.command(name="boutique", description="Voir la boutique")
        async def boutique(interaction: discord.Interaction):
            await interaction.response.send_message("🛒 Boutique en cours de chargement...", ephemeral=True)
        
        try:
            # Synchronisation pour le serveur spécifique
            guild_id = int(config['guild_id'])
            guild = discord.Object(id=guild_id)
            
            print(f"🎯 Synchronisation pour le serveur {guild_id}...")
            synced = await bot.tree.sync(guild=guild)
            print(f"✅ {len(synced)} commandes synchronisées pour le serveur")
            
            for cmd in synced:
                print(f"   /{cmd.name} - {cmd.description}")
                
        except Exception as e:
            print(f"❌ Erreur de synchronisation serveur : {e}")
            
            # Fallback : synchronisation globale
            try:
                print("🌍 Tentative de synchronisation globale...")
                synced = await bot.tree.sync()
                print(f"✅ {len(synced)} commandes synchronisées globalement")
                print("⚠️  Les commandes globales peuvent prendre jusqu'à 1 heure pour apparaître")
            except Exception as e2:
                print(f"❌ Erreur de synchronisation globale : {e2}")
        
        print("\n📋 INSTRUCTIONS :")
        print("1. Ouvrez Discord")
        print("2. Allez sur votre serveur")
        print("3. Tapez '/' dans un canal")
        print("4. Vous devriez voir les commandes du bot")
        print()
        print("🔗 Si ça ne marche pas, réinvitez le bot avec cette URL :")
        print(f"https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions=2147483647&scope=bot%20applications.commands")
        
        await bot.close()
    
    try:
        await bot.start(config['bot_token'])
    except Exception as e:
        print(f"❌ Erreur de connexion : {e}")

if __name__ == "__main__":
    asyncio.run(force_sync_commands())
