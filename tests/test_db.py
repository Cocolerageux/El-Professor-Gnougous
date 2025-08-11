import asyncio
import sys
import os
import json
sys.path.append('.')
from database.database import DatabaseManager

async def test_db():
    try:
        # Charger la configuration
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        db = DatabaseManager(config['database_url'])
        await db.initialize()
        
        print('=== Test de récupération des utilisateurs ===')
        users = await db.get_all_users()
        print(f'Nombre d\'utilisateurs: {len(users)}')
        for user in users:
            print(f'  - {user}')
        
        print('\n=== Test de création d\'utilisateur ===')
        test_user = await db.get_user("123456789")
        if not test_user:
            test_user = await db.create_user("123456789", "TestUser", "0001")
        print(f'Utilisateur test: {test_user.username if test_user else "Aucun"}')
        
        print('\n=== Test du système de shop ===')
        items = await db.get_shop_items(user_text_level=100, user_voice_level=100)
        print(f'Articles disponibles: {len(items)}')
        for item in items:
            print(f'  - {item}')
            
        await db.close()
        print('\n✅ Tests terminés avec succès')
        
    except Exception as e:
        print(f'❌ Erreur lors des tests: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_db())
