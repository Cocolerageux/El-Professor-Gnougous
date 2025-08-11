"""
Correction rapide des discriminateurs Discord
"""

import os
import re

def fix_discriminators():
    """Remplace tous les .discriminator par '0'"""
    
    files_to_fix = [
        "bot/commands/shop.py",
        "bot/commands/admin.py", 
        "bot/events/xp_events.py",
        "bot/bot.py"
    ]
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            print(f"🔧 Correction de {file_path}")
            
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Remplacer les patterns de discriminator
            patterns = [
                (r'(\w+)\.discriminator', r'"0"  # Discord a supprimé les discriminateurs'),
            ]
            
            for pattern, replacement in patterns:
                content = re.sub(pattern, replacement, content)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"✅ {file_path} corrigé")
        else:
            print(f"❌ {file_path} non trouvé")

if __name__ == "__main__":
    print("🔧 CORRECTION DES DISCRIMINATEURS")
    print("Discord a supprimé les discriminateurs, on remplace par '0'")
    fix_discriminators()
    print("✅ Correction terminée")
