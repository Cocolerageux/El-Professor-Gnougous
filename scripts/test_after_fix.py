"""
✅ SCRIPT DE VALIDATION POST-CORRECTION
=======================================

À utiliser APRÈS avoir réinvité le bot avec les bonnes permissions.
"""

import asyncio
import json
import sys
import os

# Ajouter le chemin parent pour les imports
sys.path.insert(0, os.path.abspath('.'))

from bot.bot import DiscordBot

async def test_bot_after_fix():
    """Tester le bot après correction des permissions"""
    
    print("🧪 TEST POST-CORRECTION DES PERMISSIONS")
    print("=" * 45)
    
    # Charger la configuration
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        print("✅ Configuration chargée")
    except Exception as e:
        print(f"❌ Erreur de configuration : {e}")
        return
    
    # Créer le bot comme dans main.py
    try:
        bot = DiscordBot(config)
        print("✅ Bot Discord créé")
        
        @bot.event
        async def on_ready():
            print(f"✅ Bot connecté : {bot.user}")
            print(f"📊 Serveurs : {len(bot.guilds)}")
            
            for guild in bot.guilds:
                print(f"   🏰 {guild.name} (ID: {guild.id})")
            
            # Lister les commandes disponibles
            print(f"\n📋 Commandes chargées : {len(bot.tree.get_commands())}")
            for cmd in bot.tree.get_commands():
                print(f"   /{cmd.name} - {cmd.description}")
            
            # Vérifier les extensions
            print(f"\n🧩 Extensions chargées : {len(bot.extensions)}")
            for ext in bot.extensions:
                print(f"   📦 {ext}")
            
            # Test de synchronisation
            try:
                guild_id = int(config['guild_id'])
                guild = bot.get_guild(guild_id)
                if guild:
                    synced = await bot.tree.sync(guild=guild)
                    print(f"\n🔄 {len(synced)} commandes synchronisées pour {guild.name}")
                    
                    if len(synced) > 0:
                        print("✅ SUCCÈS ! Les commandes devraient maintenant être disponibles !")
                        print("\n📱 Pour tester :")
                        print("1. Ouvrez Discord")
                        print("2. Allez sur votre serveur")
                        print("3. Tapez '/' dans un canal")
                        print("4. Vous devriez voir les commandes du bot")
                    else:
                        print("⚠️  Aucune commande synchronisée - vérifiez les permissions")
                        
                else:
                    print(f"❌ Serveur {guild_id} non trouvé")
                    
            except Exception as e:
                print(f"❌ Erreur de synchronisation : {e}")
            
            await bot.close()
        
        # Démarrer le bot
        await bot.start(config['bot_token'])
        
    except Exception as e:
        print(f"❌ Erreur de démarrage : {e}")

def show_instructions():
    """Afficher les instructions"""
    print("\n" + "="*50)
    print("🎯 INSTRUCTIONS IMPORTANTES")
    print("="*50)
    print()
    print("⚠️  AVANT D'UTILISER CE SCRIPT :")
    print()
    print("1️⃣ Réinvitez votre bot avec cette URL :")
    print("   https://discord.com/oauth2/authorize?client_id=1404484368679960666&permissions=2147483647&scope=bot%20applications.commands")
    print()
    print("2️⃣ Vérifiez que toutes les permissions sont cochées")
    print("3️⃣ Autorisez le bot sur votre serveur")
    print("4️⃣ Puis lancez ce script")
    print()
    print("✅ Si tout est correct, les commandes apparaîtront immédiatement")
    print()
    
    response = input("Avez-vous réinvité le bot ? (oui/non) : ").lower()
    if response not in ['oui', 'o', 'yes', 'y']:
        print("❌ Veuillez d'abord réinviter le bot, puis relancez ce script.")
        return False
    return True

if __name__ == "__main__":
    if show_instructions():
        print("\n🚀 Lancement du test...")
        asyncio.run(test_bot_after_fix())
    else:
        print("Script arrêté. Réinvitez d'abord le bot.")
