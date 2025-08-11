"""
Test simple d'accès à la page boutique
"""
import requests
import time

print("🔄 Test de la page boutique...")

try:
    response = requests.get("http://localhost:5000/shop", timeout=10)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Page boutique accessible")
        # Compter les occurrences d'articles
        if "Aucun article trouvé" in response.text:
            print("❌ Message 'Aucun article trouvé' présent")
        elif "<tr>" in response.text:
            tr_count = response.text.count("<tr>")
            print(f"✅ {tr_count} lignes <tr> trouvées dans le HTML")
        
    else:
        print(f"❌ Erreur {response.status_code}")
        
except Exception as e:
    print(f"❌ Erreur: {e}")
    
print("🔄 Test de l'API boutique...")
try:
    response = requests.get("http://localhost:5000/api/shop", timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ API: {len(data)} articles trouvés")
    else:
        print(f"❌ API Erreur {response.status_code}")
except Exception as e:
    print(f"❌ API Erreur: {e}")
