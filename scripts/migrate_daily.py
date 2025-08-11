"""
Script de migration pour ajouter la colonne last_daily
"""

import asyncio
import aiosqlite
import os

async def migrate_database():
    """Ajoute la colonne last_daily à la table users"""
    
    db_path = "bot_data.db"
    
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée")
        return
    
    try:
        async with aiosqlite.connect(db_path) as db:
            # Vérifier si la colonne existe déjà
            cursor = await db.execute("PRAGMA table_info(users)")
            columns = await cursor.fetchall()
            
            column_names = [col[1] for col in columns]
            
            if 'last_daily' in column_names:
                print("✅ La colonne last_daily existe déjà")
                return
            
            # Ajouter la colonne
            print("🔧 Ajout de la colonne last_daily...")
            await db.execute("ALTER TABLE users ADD COLUMN last_daily TIMESTAMP DEFAULT NULL")
            await db.commit()
            
            print("✅ Colonne last_daily ajoutée avec succès")
            
    except Exception as e:
        print(f"❌ Erreur lors de la migration : {e}")

if __name__ == "__main__":
    asyncio.run(migrate_database())
