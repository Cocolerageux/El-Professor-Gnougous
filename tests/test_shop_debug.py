"""
Test avec récupération du HTML pour voir le debug
"""
import requests

print("🔍 Test HTML de la page boutique...")

try:
    response = requests.get("http://localhost:5000/shop", timeout=10)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        html_content = response.text
        
        # Chercher les commentaires DEBUG
        debug_lines = []
        for line in html_content.split('\n'):
            if 'DEBUG:' in line:
                debug_lines.append(line.strip())
        
        if debug_lines:
            print("🔍 Messages de debug trouvés:")
            for debug_line in debug_lines:
                print(f"   {debug_line}")
        else:
            print("❌ Aucun message de debug trouvé")
            
        # Chercher le message d'erreur
        if "Aucun article trouvé" in html_content:
            print("❌ Message 'Aucun article trouvé' présent")
        else:
            print("✅ Message 'Aucun article trouvé' absent")
            
    else:
        print(f"❌ Erreur {response.status_code}")
        
except Exception as e:
    print(f"❌ Erreur: {e}")
