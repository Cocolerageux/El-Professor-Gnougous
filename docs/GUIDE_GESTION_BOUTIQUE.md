# 🛒 Guide d'Utilisation - Interface de Gestion de Boutique

## 🎯 Fonctionnalités Développées

L'interface web de votre bot Discord dispose maintenant d'un **système complet de gestion de la boutique** avec les fonctionnalités suivantes :

### ✅ **Ajout d'Articles**
- **Formulaire intuitif** avec validation complète
- **3 types d'articles** : Rôles Discord, Objets permanents, Objets consommables
- **Validation en temps réel** côté client et serveur
- **Ajout instantané** sans rechargement de page

### ✅ **Modification d'Articles**
- **Édition rapide** via prompts JavaScript
- **Mise à jour en temps réel** de tous les champs
- **Validation des nouvelles valeurs**
- **Actualisation automatique** de l'affichage

### ✅ **Suppression d'Articles**
- **Confirmation de sécurité** avant suppression
- **Suppression instantanée** de la base de données
- **Mise à jour immédiate** de l'interface

### ✅ **Interface Utilisateur Avancée**
- **Design responsive** (mobile + desktop)
- **Graphiques en temps réel** (répartition par type et prix)
- **Icônes Font Awesome** pour une meilleure expérience
- **Alertes et confirmations** utilisateur

---

## 🚀 Comment Utiliser l'Interface

### 1. **Démarrer le Bot**
```bash
.\start_bot.bat
```
ou
```bash
python main.py
```

### 2. **Accéder à l'Interface Web**
Ouvrez votre navigateur et allez sur :
```
http://localhost:5000
```

### 3. **Naviguer vers la Boutique**
- Cliquez sur **"Boutique"** dans le menu
- Vous verrez la liste actuelle des articles

### 4. **Ajouter un Nouvel Article**

#### 📝 **Étapes :**
1. Cliquez sur le bouton **"Ajouter un Article"** (vert)
2. Remplissez le formulaire :

   **Champs obligatoires :**
   - **Nom** : Nom affiché de l'article
   - **Description** : Description détaillée
   - **Prix** : Coût en pièces (nombre positif)
   - **Niveau requis** : Niveau minimum pour acheter
   - **Type** : Choisir parmi les 3 types

3. Cliquez sur **"Ajouter"**
4. L'article apparaît instantanément dans la liste

#### 🏷️ **Types d'Articles :**

| Type | Description | Utilisation |
|------|-------------|-------------|
| **🏆 Rôle Discord** | Attribue un rôle Discord | Couleurs, permissions spéciales |
| **📦 Objet permanent** | Reste dans l'inventaire | Badges, titres, accès |
| **🍎 Objet consommable** | Usage unique | Boosts temporaires, bonus |

#### 💡 **Exemples d'Articles :**

**Rôle Discord :**
- Nom : "Contributeur Actif"
- Description : "Rôle pour les membres les plus actifs"
- Prix : 300
- Niveau : 10
- Type : Rôle Discord

**Objet Consommable :**
- Nom : "Boost XP Mega"
- Description : "Triple l'XP pendant 2 heures"
- Prix : 500
- Niveau : 20
- Type : Objet consommable

### 5. **Modifier un Article Existant**

1. Cliquez sur l'icône **✏️ (crayon)** à côté de l'article
2. Modifiez les valeurs dans les prompts qui apparaissent
3. Les changements sont appliqués instantanément

### 6. **Supprimer un Article**

1. Cliquez sur l'icône **🗑️ (poubelle)** à côté de l'article
2. Confirmez la suppression dans la popup
3. L'article est supprimé définitivement

### 7. **Voir les Détails d'un Article**

1. Cliquez sur l'icône **👁️ (œil)** à côté de l'article
2. Une popup affiche tous les détails

---

## 📊 Statistiques et Graphiques

L'interface affiche automatiquement :

### **Graphique des Types d'Articles**
- Répartition visuelle par type (Rôles, Objets, Consommables)
- Mise à jour en temps réel

### **Graphique des Prix**
- Répartition par tranches de prix
- Aide à équilibrer l'économie du serveur

---

## 🔧 API pour Développeurs

Si vous voulez intégrer d'autres services, l'API REST est disponible :

### **Endpoints Disponibles :**

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/api/shop` | Récupérer tous les articles |
| `POST` | `/api/shop` | Ajouter un nouvel article |
| `PUT` | `/api/shop/<id>` | Modifier un article |
| `DELETE` | `/api/shop/<id>` | Supprimer un article |

### **Exemple d'Ajout via API :**
```javascript
fetch('/api/shop', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        name: "Nouvel Article",
        description: "Description de l'article",
        price: 200,
        required_level: 5,
        item_type: "item"
    })
})
```

---

## 🛡️ Sécurité et Validation

### **Validations Automatiques :**
- ✅ **Prix positif** (minimum 1 pièce)
- ✅ **Niveau positif** (minimum niveau 1)
- ✅ **Champs obligatoires** vérifiés
- ✅ **Type d'article valide** (role/item/consumable)
- ✅ **Confirmation** pour suppressions

### **Gestion d'Erreurs :**
- Messages d'erreur clairs en français
- Validation côté client ET serveur
- Rollback automatique en cas d'erreur

---

## 🎮 Intégration Discord

### **Comment ça fonctionne avec le bot :**

1. **Les utilisateurs** gagnent des pièces en chattant/parlant
2. **Ils achètent** des articles via les commandes Discord (`/boutique`, `/acheter`)
3. **Vous gérez** les articles via l'interface web
4. **Les changements** sont instantanés dans Discord

### **Commandes Discord Liées :**
- `/boutique` - Voir les articles disponibles
- `/acheter <article>` - Acheter un article
- `/inventaire` - Voir ses achats
- `/profil` - Voir son niveau et ses pièces

---

## 🎉 Résumé des Fonctionnalités

Votre interface de gestion de boutique est maintenant **100% fonctionnelle** avec :

- ✅ **Ajout d'articles** via formulaire web
- ✅ **Modification** d'articles existants  
- ✅ **Suppression** avec confirmation
- ✅ **Interface responsive** (mobile/desktop)
- ✅ **Graphiques statistiques** en temps réel
- ✅ **API REST complète** pour intégrations
- ✅ **Validation** côté client et serveur
- ✅ **Gestion d'erreurs** robuste

**Votre bot Discord dispose maintenant d'un système de boutique professionnel et facile à gérer !** 🚀
