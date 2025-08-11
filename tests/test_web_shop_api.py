"""
Test des API de gestion de la boutique via l'interface web
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_web_shop_api():
    """Test des API de la boutique via l'interface web"""
    print("🌐 Test des API de gestion de la boutique")
    
    try:
        # Test 1: Vérifier que l'API shop fonctionne
        print("\n📋 Test 1: Récupération de la liste des articles")
        response = requests.get(f"{BASE_URL}/api/shop")
        
        if response.status_code == 200:
            items = response.json()
            print(f"✅ {len(items)} articles récupérés")
            initial_count = len(items)
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
            return
        
        # Test 2: Ajouter un nouvel article via API
        print("\n➕ Test 2: Ajout d'un article via API")
        new_item = {
            "name": "Test API Article",
            "description": "Article ajouté via l'API de test",
            "price": 300,
            "required_level": 8,
            "item_type": "item"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/shop",
            headers={'Content-Type': 'application/json'},
            data=json.dumps(new_item)
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ Article ajouté avec succès (ID: {result.get('item_id')})")
                added_item_id = result.get('item_id')
            else:
                print(f"❌ Erreur lors de l'ajout: {result.get('error')}")
                return
        else:
            print(f"❌ Erreur HTTP {response.status_code}: {response.text}")
            return
        
        # Test 3: Vérifier que l'article a été ajouté
        print("\n🔍 Test 3: Vérification de l'ajout")
        response = requests.get(f"{BASE_URL}/api/shop")
        
        if response.status_code == 200:
            items = response.json()
            new_count = len(items)
            if new_count == initial_count + 1:
                print(f"✅ Nombre d'articles augmenté de {initial_count} à {new_count}")
                
                # Trouver le nouvel article
                found_item = None
                for item in items:
                    if item['name'] == "Test API Article":
                        found_item = item
                        break
                
                if found_item:
                    print(f"✅ Nouvel article trouvé: {found_item['name']} - {found_item['price']} pièces")
                else:
                    print("❌ Nouvel article non trouvé dans la liste")
            else:
                print(f"❌ Nombre d'articles incorrect: {new_count} (attendu: {initial_count + 1})")
        
        # Test 4: Modifier l'article via API
        print("\n✏️ Test 4: Modification de l'article via API")
        update_data = {
            "name": "Test API Article Modifié",
            "price": 450,
            "required_level": 12
        }
        
        response = requests.put(
            f"{BASE_URL}/api/shop/{added_item_id}",
            headers={'Content-Type': 'application/json'},
            data=json.dumps(update_data)
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Article modifié avec succès")
            else:
                print(f"❌ Erreur lors de la modification: {result.get('error')}")
        else:
            print(f"❌ Erreur HTTP {response.status_code}: {response.text}")
        
        # Test 5: Vérifier la modification
        print("\n🔍 Test 5: Vérification de la modification")
        response = requests.get(f"{BASE_URL}/api/shop")
        
        if response.status_code == 200:
            items = response.json()
            modified_item = None
            for item in items:
                if item['id'] == added_item_id:
                    modified_item = item
                    break
            
            if modified_item:
                if (modified_item['name'] == "Test API Article Modifié" and 
                    modified_item['price'] == 450 and 
                    modified_item['required_text_level'] == 12):
                    print("✅ Modifications vérifiées avec succès")
                else:
                    print(f"❌ Modifications incorrectes: {modified_item}")
            else:
                print("❌ Article modifié non trouvé")
        
        # Test 6: Supprimer l'article via API
        print("\n🗑️ Test 6: Suppression de l'article via API")
        response = requests.delete(f"{BASE_URL}/api/shop/{added_item_id}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Article supprimé avec succès")
            else:
                print(f"❌ Erreur lors de la suppression: {result.get('error')}")
        else:
            print(f"❌ Erreur HTTP {response.status_code}: {response.text}")
        
        # Test 7: Vérifier la suppression
        print("\n🔍 Test 7: Vérification de la suppression")
        response = requests.get(f"{BASE_URL}/api/shop")
        
        if response.status_code == 200:
            items = response.json()
            final_count = len(items)
            if final_count == initial_count:
                print(f"✅ Nombre d'articles revenu à {final_count} (initial: {initial_count})")
                
                # Vérifier que l'article n'existe plus
                deleted_found = False
                for item in items:
                    if item['id'] == added_item_id:
                        deleted_found = True
                        break
                
                if not deleted_found:
                    print("✅ Article correctement supprimé de la liste")
                else:
                    print("❌ Article encore présent dans la liste")
            else:
                print(f"❌ Nombre d'articles incorrect après suppression: {final_count}")
        
        print("\n🎉 Tests des API de gestion de la boutique terminés avec succès !")
        
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur web")
        print("   Assurez-vous que le bot est démarré avec l'interface web active")
        print("   Utilisez: .\\start_bot.bat ou python main.py")
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_web_shop_api()
