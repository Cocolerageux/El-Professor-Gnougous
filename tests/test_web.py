"""
Test simple de l'interface web sans le bot Discord
"""
import asyncio
import json
from web.app import create_web_app

def test_web_app():
    """Test l'application web"""
    # Charger la configuration
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Créer l'app Flask
    app = create_web_app(config)
    
    print("🌐 Test de l'interface web...")
    
    # Créer un client de test
    with app.test_client() as client:
        print("\n📊 Test de la page d'accueil...")
        response = client.get('/')
        print(f"   Status: {response.status_code}")
        
        print("\n📈 Test du dashboard...")
        response = client.get('/dashboard')
        print(f"   Status: {response.status_code}")
        
        print("\n👥 Test de la page utilisateurs...")
        response = client.get('/users')
        print(f"   Status: {response.status_code}")
        
        print("\n🛒 Test de la page boutique...")
        response = client.get('/shop')
        print(f"   Status: {response.status_code}")
        
        print("\n🔧 Test de l'API stats...")
        response = client.get('/api/stats')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"   Données: {data}")
        
        print("\n👤 Test de l'API users...")
        response = client.get('/api/users')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"   Utilisateurs trouvés: {len(data)}")
        
        print("\n🛍️ Test de l'API shop...")
        response = client.get('/api/shop')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"   Articles trouvés: {len(data)}")
    
    print("\n✅ Tests terminés")

if __name__ == "__main__":
    test_web_app()
