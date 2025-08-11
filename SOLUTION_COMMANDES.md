# 🚨 PROBLÈME IDENTIFIÉ : PERMISSIONS DU BOT

## ❌ Cause du problème
Votre bot **n'a pas la permission `applications.commands`** sur Discord, ce qui l'empêche d'utiliser les slash commands.

## ✅ SOLUTION RAPIDE

### 1️⃣ Réinviter le bot avec les bonnes permissions

**Utilisez cette URL pour réinviter votre bot :**

```
https://discord.com/oauth2/authorize?client_id=1404484368679960666&permissions=2147483647&scope=bot%20applications.commands
```

### 2️⃣ Vérifications à faire

1. **Cliquez sur le lien ci-dessus**
2. **Sélectionnez votre serveur "Only For Goat"**
3. **Vérifiez que toutes les permissions sont cochées** (surtout "Use Slash Commands")
4. **Cliquez sur "Autoriser"**

### 3️⃣ Test après réinvitation

Une fois le bot réinvité :

1. **Redémarrez le bot** :
   ```bash
   python main.py
   ```

2. **Testez les commandes** :
   - Tapez `/` dans un canal Discord
   - Vous devriez voir les commandes du bot apparaître

## 🔧 Commandes qui devraient être disponibles

Après correction, vous devriez voir ces commandes :

- `/niveau` - Voir votre niveau et XP
- `/classement` - Top des utilisateurs  
- `/boutique` - Voir les articles disponibles
- `/acheter` - Acheter un article
- `/daily` - Bonus quotidien
- `/admin_add_coins` - Ajouter des pièces (admin)
- `/admin_set_level` - Définir un niveau (admin)
- `/admin_shop_add` - Ajouter un article (admin)
- `/admin_shop_remove` - Supprimer un article (admin)
- `/admin_shop_list` - Lister les articles (admin)

## 🎯 Points importants

1. **Les slash commands nécessitent des permissions spéciales**
2. **Le scope `applications.commands` est obligatoire**
3. **Les commandes peuvent prendre quelques minutes pour apparaître**
4. **Redémarrez Discord si nécessaire**

## 🔄 Si le problème persiste

1. **Vérifiez que le bot est en ligne** (indicateur vert sur Discord)
2. **Attendez 5-10 minutes** après la réinvitation
3. **Redémarrez votre client Discord**
4. **Testez dans un canal où le bot a accès**

---

**🎉 Une fois corrigé, toutes les fonctionnalités du bot seront disponibles !**
