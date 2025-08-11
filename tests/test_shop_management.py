"""
Test des fonctionnalités d'ajout d'articles dans la boutique
"""
import asyncio
import sys
import os

# Ajouter le répertoire racine au PATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import DatabaseManager
import json

# Configuration de test
config = {
    'database_url': 'sqlite:///bot_data.db'
}

async def test_shop_management():
    """Test des fonctions de gestion de la boutique"""
    print("🛒 Test des fonctions de gestion de la boutique")
    
    db_manager = DatabaseManager(config['database_url'])
    
    try:
        await db_manager.initialize()
        print("✅ Base de données initialisée")
        
        # Test 1: Ajouter un nouvel article
        print("\n📝 Test 1: Ajout d'un nouvel article")
        item_id = await db_manager.add_shop_item(
            name="Rôle VIP Test",
            description="Rôle VIP pour les tests",
            price=500,
            required_text_level=10,
            required_voice_level=5,
            is_role=True,
            role_id="123456789",
            is_consumable=False
        )
        
        if item_id:
            print(f"✅ Article ajouté avec l'ID: {item_id}")
        else:
            print("❌ Échec de l'ajout d'article")
            return
        
        # Test 2: Vérifier que l'article a été ajouté
        print("\n🔍 Test 2: Vérification de l'ajout")
        items = await db_manager.get_shop_items(user_text_level=100, user_voice_level=100)
        new_item = None
        for item in items:
            if item[0] == item_id:  # id = item[0]
                new_item = item
                break
        
        if new_item:
            print(f"✅ Article trouvé: {new_item[1]} - {new_item[2]} - {new_item[3]} pièces")
        else:
            print("❌ Article non trouvé après ajout")
            return
        
        # Test 3: Modifier l'article
        print("\n✏️ Test 3: Modification de l'article")
        success = await db_manager.update_shop_item(
            item_id=item_id,
            name="Rôle VIP Test Modifié",
            price=750,
            required_text_level=15
        )
        
        if success:
            print("✅ Article modifié avec succès")
        else:
            print("❌ Échec de la modification")
            return
        
        # Test 4: Vérifier la modification
        print("\n🔍 Test 4: Vérification de la modification")
        items = await db_manager.get_shop_items(user_text_level=100, user_voice_level=100)
        modified_item = None
        for item in items:
            if item[0] == item_id:
                modified_item = item
                break
        
        if modified_item:
            print(f"✅ Article modifié trouvé: {modified_item[1]} - {modified_item[3]} pièces - Niveau {modified_item[4]}")
        else:
            print("❌ Article modifié non trouvé")
            return
        
        # Test 5: Ajouter un article consommable
        print("\n🍎 Test 5: Ajout d'un article consommable")
        consumable_id = await db_manager.add_shop_item(
            name="Boost XP Temporaire",
            description="Double l'XP pendant 1 heure",
            price=200,
            required_text_level=5,
            required_voice_level=5,
            is_role=False,
            is_consumable=True
        )
        
        if consumable_id:
            print(f"✅ Article consommable ajouté avec l'ID: {consumable_id}")
        else:
            print("❌ Échec de l'ajout d'article consommable")
        
        # Test 6: Lister tous les articles
        print("\n📋 Test 6: Liste complète des articles")
        all_items = await db_manager.get_shop_items(user_text_level=100, user_voice_level=100)
        print(f"✅ {len(all_items)} articles trouvés dans la boutique:")
        for item in all_items:
            item_type = "Rôle" if item[6] else ("Consommable" if (len(item) > 9 and item[9]) else "Objet")
            print(f"   - {item[1]} ({item_type}) - {item[3]} pièces - Niveau {item[4]}")
        
        # Test 7: Supprimer l'article de test
        print("\n🗑️ Test 7: Suppression de l'article de test")
        delete_success = await db_manager.delete_shop_item(item_id)
        
        if delete_success:
            print("✅ Article supprimé avec succès")
        else:
            print("❌ Échec de la suppression")
        
        # Test 8: Vérifier la suppression
        print("\n🔍 Test 8: Vérification de la suppression")
        final_items = await db_manager.get_shop_items(user_text_level=100, user_voice_level=100)
        deleted_found = False
        for item in final_items:
            if item[0] == item_id:
                deleted_found = True
                break
        
        if not deleted_found:
            print("✅ Article correctement supprimé")
        else:
            print("❌ Article encore présent après suppression")
        
        print(f"\n📊 Résumé: {len(final_items)} articles dans la boutique après les tests")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await db_manager.close()

if __name__ == "__main__":
    asyncio.run(test_shop_management())
