"""
Application web Flask pour la gestion du bot
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import json
import asyncio
import logging
from datetime import datetime
from database.database import DatabaseManager

logger = logging.getLogger(__name__)

# Variables globales pour la base de données
db_manager = None

async def get_stats_data():
    """Récupère les statistiques de la base de données"""
    global db_manager
    try:
        await db_manager.initialize()
        users = await db_manager.get_all_users()
        
        if not users:
            await db_manager.close()
            return {
                'total_users': 0,
                'avg_text_level': 0,
                'avg_voice_level': 0,
                'total_coins': 0,
                'total_messages': 0,
                'total_coins_distributed': 0
            }
        
        total_users = len(users)
        total_coins = sum(user[4] for user in users)  # coins
        avg_text_level = sum(user[2] for user in users) / total_users  # text_level
        avg_voice_level = sum(user[3] for user in users) / total_users  # voice_level
        
        await db_manager.close()
        
        return {
            'total_users': total_users,
            'avg_text_level': round(avg_text_level, 1),
            'avg_voice_level': round(avg_voice_level, 1),
            'total_coins': total_coins,
            'total_messages': total_coins // 2,  # Estimation basée sur les coins
            'total_coins_distributed': total_coins
        }
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des stats : {e}")
        try:
            await db_manager.close()
        except:
            pass
        return {
            'total_users': 0,
            'avg_text_level': 0,
            'avg_voice_level': 0,
            'total_coins': 0,
            'total_messages': 0,
            'total_coins_distributed': 0
        }

async def get_users_data():
    """Récupère la liste des utilisateurs"""
    global db_manager
    try:
        await db_manager.initialize()
        users = await db_manager.get_all_users()
        await db_manager.close()
        
        # Convertir en format pour le template
        users_list = []
        for user in users:
            users_list.append({
                'discord_id': user[0],
                'username': user[1],
                'text_level': user[2],
                'voice_level': user[3],
                'coins': user[4]
            })
        
        return users_list
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des utilisateurs : {e}")
        try:
            await db_manager.close()
        except:
            pass
        return []

async def get_shop_data():
    """Récupère les objets de la boutique"""
    global db_manager
    try:
        await db_manager.initialize()
        items = await db_manager.get_shop_items(user_text_level=100, user_voice_level=100)
        await db_manager.close()
        
        logger.info(f"Récupération boutique: {len(items)} articles trouvés")
        
        # Convertir en format pour le template
        shop_items = []
        for item in items:
            # Déterminer le type d'article
            is_role = bool(item[6])
            is_consumable = bool(item[9]) if len(item) > 9 else False
            
            if is_role:
                item_type = 'role'
            elif is_consumable:
                item_type = 'consumable'
            else:
                item_type = 'item'
            
            shop_item = {
                'id': item[0],
                'name': item[1],
                'description': item[2],
                'price': item[3],
                'required_text_level': item[4],
                'required_voice_level': item[5],
                'is_role': is_role,
                'role_id': item[7] if len(item) > 7 else None,
                'is_active': bool(item[8]) if len(item) > 8 else True,
                'is_consumable': is_consumable,
                'item_type': item_type
            }
            shop_items.append(shop_item)
            logger.debug(f"Article converti: {shop_item['name']} - {shop_item['item_type']}")
        
        return shop_items
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de la boutique : {e}")
        try:
            await db_manager.close()
        except:
            pass
        return []

async def add_shop_item_async(item_data):
    """Ajoute un article à la boutique"""
    global db_manager
    try:
        await db_manager.initialize()
        
        # Déterminer le type d'article
        is_role = item_data.get('item_type') == 'role'
        is_consumable = item_data.get('item_type') == 'consumable'
        
        item_id = await db_manager.add_shop_item(
            name=item_data['name'],
            description=item_data['description'],
            price=int(item_data['price']),
            required_text_level=int(item_data.get('required_level', 1)),
            required_voice_level=int(item_data.get('required_voice_level', item_data.get('required_level', 1))),
            is_role=is_role,
            role_id=item_data.get('role_id'),
            is_consumable=is_consumable
        )
        
        await db_manager.close()
        return item_id
    except Exception as e:
        logger.error(f"Erreur lors de l'ajout d'article : {e}")
        try:
            await db_manager.close()
        except:
            pass
        return None

async def update_shop_item_async(item_id, item_data):
    """Met à jour un article de la boutique"""
    global db_manager
    try:
        await db_manager.initialize()
        
        success = await db_manager.update_shop_item(
            item_id=int(item_id),
            name=item_data.get('name'),
            description=item_data.get('description'),
            price=int(item_data['price']) if 'price' in item_data else None,
            required_text_level=int(item_data['required_level']) if 'required_level' in item_data else None,
            required_voice_level=int(item_data.get('required_voice_level', item_data.get('required_level', 1))) if 'required_level' in item_data else None,
            is_active=item_data.get('is_active')
        )
        
        await db_manager.close()
        return success
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour d'article : {e}")
        try:
            await db_manager.close()
        except:
            pass
        return False

async def delete_shop_item_async(item_id):
    """Supprime un article de la boutique"""
    global db_manager
    try:
        await db_manager.initialize()
        success = await db_manager.delete_shop_item(int(item_id))
        await db_manager.close()
        return success
    except Exception as e:
        logger.error(f"Erreur lors de la suppression d'article : {e}")
        try:
            await db_manager.close()
        except:
            pass
        return False

def run_async_safe(coro):
    """Exécute une coroutine de façon sécurisée"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(coro)
        loop.close()
        return result
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution async : {e}")
        return None

def create_web_app(config):
    """Crée l'application Flask"""
    global db_manager
    
    app = Flask(__name__)
    app.secret_key = config.get('web_secret_key', 'changez_cette_cle')
    
    # Configuration CORS pour permettre les requêtes depuis d'autres domaines
    CORS(app)
    
    # Configuration de l'application
    app.config['CONFIG'] = config
    
    # Initialiser la base de données globale
    db_manager = DatabaseManager(config['database_url'])
    
    # Routes
    @app.route('/')
    def index():
        """Page d'accueil de l'interface web"""
        return render_template('index.html', config=config)
    
    @app.route('/dashboard')
    def dashboard():
        """Tableau de bord principal"""
        stats = run_async_safe(get_stats_data())
        if not stats:
            stats = {
                'total_users': 0,
                'avg_text_level': 0,
                'avg_voice_level': 0,
                'total_coins': 0,
                'total_messages': 0,
                'total_coins_distributed': 0
            }
        return render_template('dashboard.html', stats=stats)
    
    @app.route('/users')
    def users():
        """Liste des utilisateurs"""
        users_list = run_async_safe(get_users_data())
        if not users_list:
            users_list = []
        return render_template('users.html', users=users_list)
    
    @app.route('/shop')
    def shop_management():
        """Gestion de la boutique"""
        # Copier exactement la logique de l'API qui fonctionne
        try:
            shop_data = run_async_safe(get_shop_data())
            # Assurer que shop_data n'est jamais None
            if shop_data is None:
                shop_data = []
            return render_template('shop.html', shop_items=shop_data)
        except Exception as e:
            logger.error(f"Erreur route shop: {e}")
            return render_template('shop.html', shop_items=[])
    
    @app.route('/settings')
    def settings():
        """Paramètres de configuration"""
        return render_template('settings.html', config=config)
    
    # API Routes
    @app.route('/api/stats')
    def api_stats():
        """API pour récupérer les statistiques"""
        stats = run_async_safe(get_stats_data())
        return jsonify(stats if stats else {})
    
    @app.route('/api/users')
    def api_users():
        """API pour récupérer la liste des utilisateurs"""
        users = run_async_safe(get_users_data())
        return jsonify(users if users else [])
    
    @app.route('/api/user/<user_id>')
    def api_user_details(user_id):
        """API pour récupérer les détails d'un utilisateur"""
        # TODO: Implémenter la récupération des détails utilisateur
        user_details = {}
        return jsonify(user_details)
    
    @app.route('/api/shop')
    def api_shop():
        """API pour récupérer les objets de la boutique"""
        shop = run_async_safe(get_shop_data())
        return jsonify(shop if shop else [])
    
    @app.route('/api/shop', methods=['POST'])
    def api_add_shop_item():
        """API pour ajouter un objet à la boutique"""
        try:
            data = request.get_json()
            
            # Validation des données
            required_fields = ['name', 'description', 'price', 'required_level', 'item_type']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({'success': False, 'error': f'Le champ {field} est requis'}), 400
            
            # Validation du prix
            try:
                price = int(data['price'])
                if price <= 0:
                    return jsonify({'success': False, 'error': 'Le prix doit être positif'}), 400
            except ValueError:
                return jsonify({'success': False, 'error': 'Le prix doit être un nombre'}), 400
            
            # Validation du niveau requis
            try:
                required_level = int(data['required_level'])
                if required_level <= 0:
                    return jsonify({'success': False, 'error': 'Le niveau requis doit être positif'}), 400
            except ValueError:
                return jsonify({'success': False, 'error': 'Le niveau requis doit être un nombre'}), 400
            
            # Validation du type
            if data['item_type'] not in ['role', 'item', 'consumable']:
                return jsonify({'success': False, 'error': 'Type d\'article invalide'}), 400
            
            # Ajouter l'article
            item_id = run_async_safe(add_shop_item_async(data))
            
            if item_id:
                return jsonify({
                    'success': True, 
                    'message': 'Article ajouté avec succès',
                    'item_id': item_id
                })
            else:
                return jsonify({'success': False, 'error': 'Erreur lors de l\'ajout de l\'article'}), 500
                
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout d'objet : {e}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/shop/<int:item_id>', methods=['PUT'])
    def api_update_shop_item(item_id):
        """API pour modifier un objet de la boutique"""
        try:
            data = request.get_json()
            
            # Validation du prix si fourni
            if 'price' in data:
                try:
                    price = int(data['price'])
                    if price <= 0:
                        return jsonify({'success': False, 'error': 'Le prix doit être positif'}), 400
                except ValueError:
                    return jsonify({'success': False, 'error': 'Le prix doit être un nombre'}), 400
            
            # Validation du niveau requis si fourni
            if 'required_level' in data:
                try:
                    required_level = int(data['required_level'])
                    if required_level <= 0:
                        return jsonify({'success': False, 'error': 'Le niveau requis doit être positif'}), 400
                except ValueError:
                    return jsonify({'success': False, 'error': 'Le niveau requis doit être un nombre'}), 400
            
            # Mettre à jour l'article
            success = run_async_safe(update_shop_item_async(item_id, data))
            
            if success:
                return jsonify({'success': True, 'message': 'Article mis à jour avec succès'})
            else:
                return jsonify({'success': False, 'error': 'Erreur lors de la mise à jour de l\'article'}), 500
                
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour d'objet : {e}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/shop/<int:item_id>', methods=['DELETE'])
    def api_delete_shop_item(item_id):
        """API pour supprimer un objet de la boutique"""
        try:
            success = run_async_safe(delete_shop_item_async(item_id))
            
            if success:
                return jsonify({'success': True, 'message': 'Article supprimé avec succès'})
            else:
                return jsonify({'success': False, 'error': 'Erreur lors de la suppression de l\'article'}), 500
                
        except Exception as e:
            logger.error(f"Erreur lors de la suppression d'objet : {e}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/config', methods=['GET', 'POST'])
    def api_config():
        """API pour gérer la configuration"""
        if request.method == 'GET':
            return jsonify(config)
        
        try:
            data = request.get_json()
            # TODO: Implémenter la sauvegarde de la configuration
            # Pour l'instant, on met à jour temporairement
            config.update(data)
            return jsonify({'success': True, 'message': 'Configuration mise à jour'})
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de la configuration : {e}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.errorhandler(404)
    def not_found(error):
        """Gestionnaire d'erreur 404"""
        return render_template('error.html', error="Page non trouvée"), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Gestionnaire d'erreur 500"""
        return render_template('error.html', error="Erreur interne du serveur"), 500
    
    return app
