import asyncio
import json
import sys
sys.path.append('.')
from database.database import DatabaseManager

async def test_shop_commands():
    """Test les commandes de la boutique"""
    try:
        # Charger la configuration
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        db = DatabaseManager(config['database_url'])
        await db.initialize()
        
        print("=== Test des commandes de boutique ===")
        
        # Test avec l'utilisateur existant
        user_id = "848335064533041163"  # cocolerageuxkawaii
        user = await db.get_user(user_id)
        
        if not user:
            # Créer l'utilisateur s'il n'existe pas
            print("👤 Création d'un utilisateur de test...")
            user = await db.create_user(user_id, "cocolerageuxkawaii", "0001")
            
            # Ajouter de l'XP et des pièces pour les tests
            await db.update_user_xp(user_id, text_xp=61, voice_xp=50)
            await db.update_user_coins(user_id, 100)  # Ajouter 100 pièces
            
            # Récupérer l'utilisateur mis à jour
            user = await db.get_user(user_id)
        
        if user:
            print(f"✅ Utilisateur trouvé: {user.username}")
            print(f"   - Niveau texte: {user.text_level} (XP: {user.text_xp})")
            print(f"   - Niveau vocal: {user.voice_level} (XP: {user.voice_xp})")
            print(f"   - Pièces: {user.coins}")
            
            # Test de récupération des objets de boutique
            shop_items = await db.get_shop_items(user.text_level, user.voice_level)
            print(f"\n📦 Articles disponibles: {len(shop_items)}")
            
            for item in shop_items:
                item_id, name, desc, price, req_text, req_voice, is_role, role_id, is_active, is_consumable = item[:10]
                print(f"   {item_id}. {name} - {price} coins (Req: T{req_text}/V{req_voice})")
            
            # Test d'achat simulé
            if shop_items and user.coins >= shop_items[0][3]:  # Premier article
                item = shop_items[0]
                item_id, name, price = item[0], item[1], item[3]
                
                # Simuler l'achat
                success = await db.purchase_item(user_id, item_id, price)
                if success:
                    print(f"\n✅ Achat simulé réussi: {name} pour {price} coins")
                    
                    # Vérifier le nouveau solde
                    updated_user = await db.get_user(user_id)
                    print(f"   Nouveau solde: {updated_user.coins} coins")
                else:
                    print(f"\n❌ Échec de l'achat simulé")
            else:
                print(f"\n⚠️  Pas assez de pièces pour un achat")
        else:
            print("❌ Utilisateur non trouvé")
        
        await db.close()
        print("\n✅ Tests terminés")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_shop_commands())
