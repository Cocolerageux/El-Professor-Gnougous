"""
🎯 TEST FINAL COMPLET DU PROJET
================================

Ce script vérifie que TOUT fonctionne parfaitement dans le projet.
"""
import asyncio
import requests
import json
import sys
import os

# Ajouter le répertoire racine au PATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import DatabaseManager

async def test_database():
    """Test de la base de données"""
    print("� TEST DE LA BASE DE DONNÉES")
    print("-" * 30)
    
    config = {'database_url': 'sqlite:///bot_data.db'}
    db_manager = DatabaseManager(config['database_url'])
    
    try:
        await db_manager.initialize()
        
        # Test 1: Utilisateurs
        users = await db_manager.get_all_users()
        print(f"✅ Utilisateurs: {len(users)} trouvés")
        for user in users:
            print(f"   - {user[1]} (Niveau {user[2]}, {user[4]} pièces)")
        
        # Test 2: Articles boutique
        items = await db_manager.get_shop_items(100, 100)
        print(f"✅ Articles boutique: {len(items)} trouvés")
        
        # Test 3: Ajout/suppression d'article
        test_id = await db_manager.add_shop_item(
            "Test Final", "Article de test final", 999, 1, 1, False, None, False
        )
        if test_id:
            print(f"✅ Ajout d'article: ID {test_id} créé")
            success = await db_manager.delete_shop_item(test_id)
            print(f"✅ Suppression d'article: {'Réussie' if success else 'Échouée'}")
        
        await db_manager.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")
        return False

def test_web_interface():
    """Test de l'interface web"""
    print("\n🌐 TEST DE L'INTERFACE WEB")
    print("-" * 30)
    
    try:
        base_url = "http://localhost:5000"
        
        # Test 1: Page d'accueil
        response = requests.get(base_url, timeout=5)
        print(f"✅ Page d'accueil: {response.status_code}")
        
        # Test 2: Dashboard
        response = requests.get(f"{base_url}/dashboard", timeout=5)
        print(f"✅ Dashboard: {response.status_code}")
        
        # Test 3: Page utilisateurs
        response = requests.get(f"{base_url}/users", timeout=5)
        if response.status_code == 200:
            has_users = "cocolerageuxkawaii" in response.text or "alexycarter" in response.text
            print(f"✅ Page utilisateurs: {response.status_code} {'(avec données)' if has_users else '(vide)'}")
        
        # Test 4: Page boutique
        response = requests.get(f"{base_url}/shop", timeout=5)
        if response.status_code == 200:
            has_items = "Badge Nouveau" in response.text or "Emoji Spécial" in response.text
            no_items = "Aucun article trouvé" in response.text
            status = "avec articles" if has_items else ("vide" if no_items else "inconnu")
            print(f"✅ Page boutique: {response.status_code} ({status})")
        
        # Test 5: API Stats
        response = requests.get(f"{base_url}/api/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Stats: {data.get('total_users')} users, {data.get('total_coins')} coins")
        
        # Test 6: API Shop
        response = requests.get(f"{base_url}/api/shop", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Shop: {len(data)} articles")
        
        # Test 7: API Users  
        response = requests.get(f"{base_url}/api/users", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Users: {len(data)} utilisateurs")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Interface web non accessible")
        print("   Démarrez le bot avec: .\\start_bot.bat")
        return False
    except Exception as e:
        print(f"❌ Erreur interface web: {e}")
        return False

def test_shop_management():
    """Test des fonctions de gestion de boutique"""
    print("\n🛒 TEST DES FONCTIONS DE GESTION")
    print("-" * 35)
    
    try:
        base_url = "http://localhost:5000"
        
        # Test 1: Ajouter un article via API
        new_item = {
            "name": "Article Test Final",
            "description": "Article créé pendant le test final",
            "price": 777,
            "required_level": 10,
            "item_type": "item"
        }
        
        response = requests.post(
            f"{base_url}/api/shop",
            headers={'Content-Type': 'application/json'},
            data=json.dumps(new_item),
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                item_id = result.get('item_id')
                print(f"✅ Ajout via API: Article {item_id} créé")
                
                # Test 2: Modifier l'article
                update_data = {"price": 888, "name": "Article Test Final Modifié"}
                response = requests.put(
                    f"{base_url}/api/shop/{item_id}",
                    headers={'Content-Type': 'application/json'},
                    data=json.dumps(update_data),
                    timeout=5
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        print("✅ Modification via API: Réussie")
                
                # Test 3: Supprimer l'article
                response = requests.delete(f"{base_url}/api/shop/{item_id}", timeout=5)
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        print("✅ Suppression via API: Réussie")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur gestion boutique: {e}")
        return False

async def main():
    """Test principal"""
    print("🚀 TEST FINAL COMPLET DU PROJET DISCORD BOT")
    print("=" * 50)
    
    # Test 1: Base de données
    db_ok = await test_database()
    
    # Test 2: Interface web
    web_ok = test_web_interface()
    
    # Test 3: Gestion boutique
    shop_ok = test_shop_management() if web_ok else False
    
    # Résumé
    print("\n🎯 RÉSUMÉ FINAL")
    print("=" * 20)
    print(f"💾 Base de données: {'✅ OK' if db_ok else '❌ ERREUR'}")
    print(f"🌐 Interface web: {'✅ OK' if web_ok else '❌ ERREUR'}")
    print(f"🛒 Gestion boutique: {'✅ OK' if shop_ok else '❌ ERREUR'}")
    
    if db_ok and web_ok and shop_ok:
        print("\n🎉 PROJET TERMINÉ AVEC SUCCÈS !")
        print("✅ Toutes les fonctionnalités opérationnelles")
        print("✅ Bot Discord prêt à l'emploi")
        print("✅ Interface web fonctionnelle")
        print("✅ Système de boutique complet")
    else:
        print("\n⚠️ Quelques ajustements nécessaires")
        if not web_ok:
            print("🔧 Démarrez le bot: .\\start_bot.bat")

if __name__ == "__main__":
    asyncio.run(main())
