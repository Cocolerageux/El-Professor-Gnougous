"""
🔄 FORCE RESYNCHRONISATION DES COMMANDES
========================================

Force la synchronisation et liste toutes les commandes.
"""

import asyncio
import discord
from discord.ext import commands
import json

async def force_sync_and_list():
    """Force la synchronisation et liste les commandes"""
    
    print("🔄 RESYNCHRONISATION FORCÉE")
    print("=" * 30)
    
    # Charger config
    with open("config.json", "r") as f:
        config = json.load(f)
    
    # Configuration bot
    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True
    intents.members = True
    
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        print(f"✅ Bot connecté : {bot.user}")
        
        # Charger les extensions comme dans le vrai bot
        try:
            await bot.load_extension('bot.commands.experience')
            await bot.load_extension('bot.commands.shop')
            await bot.load_extension('bot.commands.admin')
            print("✅ Extensions chargées")
        except Exception as e:
            print(f"❌ Erreur chargement extensions : {e}")
            await bot.close()
            return
        
        # Lister toutes les commandes avant sync
        print(f"\n📋 Commandes locales chargées : {len(bot.tree.get_commands())}")
        for cmd in bot.tree.get_commands():
            print(f"   /{cmd.name} - {cmd.description}")
        
        # Synchronisation pour le serveur
        try:
            guild_id = int(config['guild_id'])
            guild = discord.Object(id=guild_id)
            
            print(f"\n🎯 Synchronisation pour le serveur {guild_id}...")
            synced = await bot.tree.sync(guild=guild)
            
            print(f"✅ {len(synced)} commandes synchronisées :")
            for cmd in synced:
                print(f"   /{cmd.name} - {cmd.description}")
                
            if len(synced) != len(bot.tree.get_commands()):
                print(f"⚠️  Différence détectée !")
                print(f"   Local : {len(bot.tree.get_commands())}")
                print(f"   Sync : {len(synced)}")
            
        except Exception as e:
            print(f"❌ Erreur de synchronisation : {e}")
        
        print("\n📱 VÉRIFIEZ MAINTENANT SUR DISCORD :")
        print("1. Fermez Discord complètement")
        print("2. Rouvrez Discord")
        print("3. Tapez '/' dans votre serveur")
        print("4. La commande /daily devrait apparaître")
        
        await bot.close()
    
    try:
        await bot.start(config['bot_token'])
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    asyncio.run(force_sync_and_list())
