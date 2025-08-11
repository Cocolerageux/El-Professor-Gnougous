"""
🚨 TEST SIMPLE DES COMMANDES
============================

Créer une commande ultra-simple pour identifier le problème.
"""

import discord
from discord.ext import commands
import json
import asyncio

async def test_simple_command():
    print("🧪 TEST COMMANDE SIMPLE")
    print("=" * 25)
    
    # Charger config
    with open("config.json", "r") as f:
        config = json.load(f)
    
    # Bot minimal
    intents = discord.Intents.default()
    intents.message_content = True
    
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        print(f"✅ {bot.user} connecté")
        
        # Commande ultra-simple
        @bot.tree.command(name="ping", description="Test simple")
        async def ping(interaction: discord.Interaction):
            print(f"📨 Commande ping reçue de {interaction.user}")
            await interaction.response.send_message("🏓 Pong!", ephemeral=True)
            print("✅ Réponse envoyée")
        
        # Sync
        guild = discord.Object(id=int(config['guild_id']))
        await bot.tree.sync(guild=guild)
        print("✅ Commande synchronisée")
        
        print("\n🎯 Testez /ping sur Discord")
        print("Les logs apparaîtront ici...")
    
    @bot.event  
    async def on_interaction(interaction):
        print(f"🔔 Interaction: {interaction.type} de {interaction.user}")
    
    try:
        await bot.start(config['bot_token'])
    except KeyboardInterrupt:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(test_simple_command())
