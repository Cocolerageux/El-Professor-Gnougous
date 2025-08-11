"""
🔍 DIAGNOSTIC RÉPONSE AUX COMMANDES
===================================

Vérifier pourquoi le bot ne répond pas aux interactions.
"""

import asyncio
import discord
from discord.ext import commands
import json
import logging

# Activer tous les logs pour voir les erreurs
logging.basicConfig(level=logging.DEBUG)

async def test_interactions():
    """Tester les interactions du bot"""
    
    print("🔍 DIAGNOSTIC DES INTERACTIONS")
    print("=" * 35)
    
    # Charger la configuration
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
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
        
        # Créer une commande de test simple
        @bot.tree.command(name="test_reponse", description="Test de réponse simple")
        async def test_reponse(interaction: discord.Interaction):
            print(f"🎯 Commande reçue de {interaction.user}")
            try:
                await interaction.response.send_message("✅ Je réponds correctement !", ephemeral=True)
                print("✅ Réponse envoyée avec succès")
            except Exception as e:
                print(f"❌ Erreur lors de la réponse : {e}")
        
        # Synchroniser
        try:
            guild_id = int(config['guild_id'])
            guild = discord.Object(id=guild_id)
            synced = await bot.tree.sync(guild=guild)
            print(f"✅ {len(synced)} commandes synchronisées")
        except Exception as e:
            print(f"❌ Erreur de synchronisation : {e}")
        
        print("\n📋 TESTEZ MAINTENANT :")
        print("1. Tapez /test_reponse sur Discord")
        print("2. Regardez les logs ici")
        print("3. Appuyez sur Ctrl+C pour arrêter")
        
        # Garder le bot en vie pour les tests
        while True:
            await asyncio.sleep(1)
    
    @bot.event
    async def on_application_command_error(interaction: discord.Interaction, error):
        print(f"❌ ERREUR COMMANDE : {error}")
        print(f"   Commande : {interaction.data}")
        print(f"   Utilisateur : {interaction.user}")
        try:
            if not interaction.response.is_done():
                await interaction.response.send_message(f"❌ Erreur : {error}", ephemeral=True)
        except:
            pass
    
    @bot.event
    async def on_interaction(interaction: discord.Interaction):
        print(f"📨 INTERACTION REÇUE :")
        print(f"   Type : {interaction.type}")
        print(f"   Utilisateur : {interaction.user}")
        print(f"   Canal : {interaction.channel}")
        print(f"   Données : {interaction.data}")
    
    @bot.event
    async def on_error(event, *args, **kwargs):
        print(f"❌ ERREUR GÉNÉRALE : {event}")
        import traceback
        traceback.print_exc()
    
    try:
        await bot.start(config['bot_token'])
    except KeyboardInterrupt:
        print("\n🛑 Test arrêté par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur de connexion : {e}")

if __name__ == "__main__":
    print("🧪 Ce script va créer une commande de test pour diagnostiquer")
    print("   pourquoi le bot ne répond pas aux interactions.")
    print()
    input("Appuyez sur Entrée pour continuer...")
    asyncio.run(test_interactions())
