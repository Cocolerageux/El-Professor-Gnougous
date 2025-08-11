"""
🔍 DIAGNOSTIC DES COMMANDES DISCORD
===================================

Vérifier pourquoi les commandes ne sont pas disponibles dans Discord.
"""

import asyncio
import discord
from discord.ext import commands
import json
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)

async def diagnostic_bot():
    print("🔍 DIAGNOSTIC DES COMMANDES DISCORD")
    print("=" * 40)
    
    # Charger la configuration
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        print("✅ Configuration chargée")
    except Exception as e:
        print(f"❌ Erreur de configuration : {e}")
        return
    
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
        print(f"📊 Guilds connectés : {len(bot.guilds)}")
        
        for guild in bot.guilds:
            print(f"   🏰 {guild.name} (ID: {guild.id})")
            print(f"      👥 Membres : {guild.member_count}")
            
            # Vérifier les permissions du bot
            bot_member = guild.get_member(bot.user.id)
            if bot_member:
                perms = bot_member.guild_permissions
                print(f"      🔑 Permissions importantes :")
                print(f"         - Envoyer messages : {perms.send_messages}")
                print(f"         - Utiliser slash commands : {perms.use_slash_commands}")
                print(f"         - Gérer rôles : {perms.manage_roles}")
                print(f"         - Voir canaux : {perms.view_channel}")
            
        # Lister les commandes slash
        try:
            synced = await bot.tree.sync()
            print(f"\n🔄 Commandes synchronisées : {len(synced)}")
            for cmd in synced:
                print(f"   /{cmd.name} - {cmd.description}")
        except Exception as e:
            print(f"❌ Erreur de synchronisation : {e}")
        
        # Tester une commande simple
        print("\n🧪 Test d'une commande simple...")
        
        await bot.close()
    
    @bot.tree.command(name="test", description="Commande de test simple")
    async def test_command(interaction: discord.Interaction):
        await interaction.response.send_message("✅ Le bot fonctionne !", ephemeral=True)
    
    try:
        await bot.start(config['bot_token'])
    except Exception as e:
        print(f"❌ Erreur de connexion : {e}")

def check_config():
    """Vérifier la configuration"""
    print("\n🔧 VÉRIFICATION DE LA CONFIGURATION")
    print("=" * 40)
    
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        
        # Vérifier les clés importantes
        required_keys = ['bot_token', 'guild_id']
        for key in required_keys:
            if key in config:
                if key == 'bot_token':
                    token_preview = config[key][:20] + "..." if config[key] else "VIDE"
                    print(f"✅ {key} : {token_preview}")
                else:
                    print(f"✅ {key} : {config[key]}")
            else:
                print(f"❌ {key} : MANQUANT")
        
        # Vérifier le guild_id
        if 'guild_id' in config and config['guild_id']:
            print(f"🏰 Serveur cible : {config['guild_id']}")
        else:
            print("⚠️  Aucun guild_id spécifié - commandes globales (peut prendre 1h)")
            
    except Exception as e:
        print(f"❌ Erreur de lecture config : {e}")

def show_troubleshooting():
    """Afficher les solutions de dépannage"""
    print("\n🛠️ SOLUTIONS POSSIBLES")
    print("=" * 30)
    print()
    print("1️⃣ **Permissions du bot sur Discord :**")
    print("   - Le bot doit avoir la permission 'applications.commands'")
    print("   - Vérifiez l'URL d'invitation du bot")
    print("   - Réinvitez le bot avec les bonnes permissions")
    print()
    print("2️⃣ **Synchronisation des commandes :**")
    print("   - Les commandes peuvent prendre du temps à apparaître")
    print("   - Essayez de redémarrer Discord")
    print("   - Attendez quelques minutes")
    print()
    print("3️⃣ **Configuration guild_id :**")
    print("   - Spécifiez l'ID du serveur dans config.json")
    print("   - Les commandes de serveur apparaissent immédiatement")
    print("   - Les commandes globales prennent jusqu'à 1 heure")
    print()
    print("4️⃣ **URL d'invitation correcte :**")
    print("   https://discord.com/oauth2/authorize?client_id=VOTRE_BOT_ID&permissions=8&scope=bot%20applications.commands")
    print()
    print("5️⃣ **Vérifications Discord :**")
    print("   - Tapez '/' dans un canal pour voir les commandes")
    print("   - Vérifiez que le bot est en ligne")
    print("   - Le bot doit avoir accès au canal")

if __name__ == "__main__":
    check_config()
    show_troubleshooting()
    
    print("\n🚀 Lancement du diagnostic...")
    asyncio.run(diagnostic_bot())
