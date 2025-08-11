"""
Test détaillé de l'interface web avec vérification du contenu HTML
"""
import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "http://localhost:5000"

def test_dashboard_content():
    """Test du contenu du dashboard"""
    print("🎯 Test détaillé du Dashboard")
    
    try:
        # Test de la page dashboard
        response = requests.get(f"{BASE_URL}/dashboard")
        if response.status_code != 200:
            print(f"❌ Erreur {response.status_code} sur /dashboard")
            return
        
        # Analyser le HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Chercher les éléments de statistiques
        total_users = soup.find(id='total-users')
        total_messages = soup.find(id='total-messages')
        coins_distributed = soup.find(id='coins-distributed')
        
        print(f"📊 Contenu du dashboard:")
        print(f"   • Utilisateurs: {total_users.text if total_users else 'NON TROUVÉ'}")
        print(f"   • Messages: {total_messages.text if total_messages else 'NON TROUVÉ'}")
        print(f"   • Pièces: {coins_distributed.text if coins_distributed else 'NON TROUVÉ'}")
        
        # Test de l'API stats en parallèle
        stats_response = requests.get(f"{BASE_URL}/api/stats")
        if stats_response.status_code == 200:
            stats_data = stats_response.json()
            print(f"📈 Données API stats:")
            print(f"   • total_users: {stats_data.get('total_users')}")
            print(f"   • total_messages: {stats_data.get('total_messages')}")
            print(f"   • total_coins_distributed: {stats_data.get('total_coins_distributed')}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

def test_shop_content():
    """Test du contenu de la boutique"""
    print("\n🛒 Test détaillé de la Boutique")
    
    try:
        # Test de la page boutique
        response = requests.get(f"{BASE_URL}/shop")
        if response.status_code != 200:
            print(f"❌ Erreur {response.status_code} sur /shop")
            return
        
        # Analyser le HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Chercher le tableau des articles
        table = soup.find('table')
        if not table:
            print("❌ Tableau d'articles non trouvé")
            return
        
        # Compter les lignes d'articles
        rows = table.find('tbody').find_all('tr')
        
        print(f"📋 Contenu de la boutique:")
        print(f"   • Lignes trouvées dans le tableau: {len(rows)}")
        
        if len(rows) == 1 and 'Aucun article' in rows[0].text:
            print("   ❌ Message 'Aucun article trouvé' affiché")
        else:
            print("   ✅ Articles trouvés dans le tableau:")
            for i, row in enumerate(rows[:5]):  # Afficher les 5 premiers
                cells = row.find_all('td')
                if len(cells) >= 2:
                    name = cells[0].text.strip()
                    price = cells[2].text.strip() if len(cells) > 2 else "N/A"
                    print(f"      {i+1}. {name} - {price}")
        
        # Test de l'API shop en parallèle
        shop_response = requests.get(f"{BASE_URL}/api/shop")
        if shop_response.status_code == 200:
            shop_data = shop_response.json()
            print(f"🛍️ Données API shop:")
            print(f"   • Nombre d'articles: {len(shop_data)}")
            if shop_data:
                print("   • Premiers articles:")
                for item in shop_data[:3]:
                    print(f"      - {item.get('name')} ({item.get('price')} pièces)")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

def test_users_content():
    """Test du contenu de la page utilisateurs"""
    print("\n👥 Test détaillé des Utilisateurs")
    
    try:
        # Test de la page utilisateurs
        response = requests.get(f"{BASE_URL}/users")
        if response.status_code != 200:
            print(f"❌ Erreur {response.status_code} sur /users")
            return
        
        # Analyser le HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Chercher le tableau des utilisateurs
        table = soup.find('table')
        if not table:
            print("❌ Tableau d'utilisateurs non trouvé")
            return
        
        rows = table.find('tbody').find_all('tr')
        
        print(f"👤 Contenu de la page utilisateurs:")
        print(f"   • Lignes trouvées: {len(rows)}")
        
        if len(rows) == 1 and 'Aucun utilisateur' in rows[0].text:
            print("   ❌ Message 'Aucun utilisateur trouvé' affiché")
        else:
            print("   ✅ Utilisateurs trouvés:")
            for i, row in enumerate(rows):
                cells = row.find_all('td')
                if len(cells) >= 2:
                    username = cells[0].text.strip()
                    text_level = cells[1].text.strip() if len(cells) > 1 else "N/A"
                    coins = cells[3].text.strip() if len(cells) > 3 else "N/A"
                    print(f"      {i+1}. {username} - Niveau {text_level} - {coins}")
        
        # Test de l'API users en parallèle
        users_response = requests.get(f"{BASE_URL}/api/users")
        if users_response.status_code == 200:
            users_data = users_response.json()
            print(f"👤 Données API users:")
            print(f"   • Nombre d'utilisateurs: {len(users_data)}")
            if users_data:
                print("   • Utilisateurs:")
                for user in users_data:
                    print(f"      - {user.get('username')} (Niveau {user.get('text_level')}, {user.get('coins')} pièces)")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    print("🔍 DIAGNOSTIC DÉTAILLÉ DE L'INTERFACE WEB")
    print("=" * 50)
    
    try:
        # Vérifier que le serveur répond
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code != 200:
            print(f"❌ Serveur web non accessible sur {BASE_URL}")
            print("   Assurez-vous que le bot est démarré avec l'interface web")
            exit(1)
        
        print("✅ Serveur web accessible")
        
        test_dashboard_content()
        test_shop_content()
        test_users_content()
        
        print("\n🎉 Diagnostic terminé !")
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Impossible de se connecter à {BASE_URL}")
        print("   Démarrez le bot avec: .\\start_bot.bat")
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
