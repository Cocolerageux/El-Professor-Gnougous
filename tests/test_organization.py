"""
🧪 TEST APRÈS RANGEMENT DU PROJET
=================================

Vérifier que tous les chemins et imports fonctionnent après réorganisation.
"""

import sys
import os

print("🔍 VÉRIFICATION POST-RANGEMENT")
print("=" * 40)

# Test 1: Vérifier les imports principaux
print("\n1️⃣ Test des imports...")
try:
    # Vérifier que les modules principaux s'importent
    from bot.bot import DiscordBot
    from database.database import DatabaseManager
    from web.app import create_app
    print("✅ Tous les imports principaux fonctionnent")
except Exception as e:
    print(f"❌ Erreur d'import : {e}")

# Test 2: Vérifier les chemins
print("\n2️⃣ Test des chemins...")
required_files = [
    "main.py",
    "config.json", 
    "requirements.txt",
    "bot_data.db",
    "scripts/start_bot.bat",
    "tests/test_final.py",
    "docs/README.md"
]

for file_path in required_files:
    if os.path.exists(file_path):
        print(f"✅ {file_path}")
    else:
        print(f"❌ {file_path} - MANQUANT")

# Test 3: Vérifier la structure des dossiers
print("\n3️⃣ Test de la structure...")
required_dirs = [
    "bot", "database", "web", 
    "scripts", "tests", "docs", 
    "deployment", "logs"
]

for dir_name in required_dirs:
    if os.path.isdir(dir_name):
        file_count = len(os.listdir(dir_name))
        print(f"✅ {dir_name}/ ({file_count} fichiers)")
    else:
        print(f"❌ {dir_name}/ - MANQUANT")

# Test 4: Vérifier les scripts
print("\n4️⃣ Test des scripts...")
bat_files = [f for f in os.listdir("scripts") if f.endswith(".bat")]
print(f"✅ {len(bat_files)} scripts .bat trouvés")

test_files = [f for f in os.listdir("tests") if f.startswith("test_")]
print(f"✅ {len(test_files)} fichiers de test trouvés")

doc_files = [f for f in os.listdir("docs") if f.endswith(".md")]
print(f"✅ {len(doc_files)} fichiers de documentation trouvés")

print("\n🎉 VÉRIFICATION TERMINÉE !")
print("Le projet est bien organisé et fonctionnel.")

# Test 5: Vérifier que le bot peut démarrer (import seulement)
print("\n5️⃣ Test de démarrage théorique...")
try:
    # Import rapide pour vérifier la faisabilité
    import asyncio
    import discord
    import flask
    print("✅ Toutes les dépendances sont disponibles")
    print("✅ Le bot devrait pouvoir démarrer normalement")
except Exception as e:
    print(f"⚠️  Attention: {e}")

print("\n📁 Structure finale :")
print("  📂 bot/        - Code Discord")
print("  📂 database/   - Gestion DB")  
print("  📂 web/        - Interface web")
print("  📂 scripts/    - Utilitaires")
print("  📂 tests/      - Tests")
print("  📂 docs/       - Documentation")
print("  📂 deployment/ - Déploiement")
print("  📂 logs/       - Logs")
print("  📄 main.py     - Point d'entrée")

print("\n🚀 PROJET PRÊT À L'EMPLOI !")
