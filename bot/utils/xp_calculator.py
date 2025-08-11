"""
Calculateur d'expérience
"""
import random
import math

class XPCalculator:
    """Classe pour calculer l'expérience et les niveaux"""
    
    def __init__(self, xp_settings):
        self.settings = xp_settings
    
    def calculate_text_xp(self) -> int:
        """Calcule l'XP gagné pour un message"""
        min_xp = self.settings.get('text_xp_min', 15)
        max_xp = self.settings.get('text_xp_max', 25)
        return random.randint(min_xp, max_xp)
    
    def calculate_voice_xp(self, minutes: float) -> int:
        """Calcule l'XP gagné pour du temps en vocal"""
        xp_per_minute = self.settings.get('voice_xp_per_minute', 10)
        return int(minutes * xp_per_minute)
    
    def xp_to_level(self, xp: int) -> int:
        """Convertit l'XP en niveau"""
        if xp <= 0:
            return 1
        
        multiplier = self.settings.get('level_multiplier', 100)
        # Formule : niveau = floor(sqrt(xp / multiplier)) + 1
        level = int(math.sqrt(xp / multiplier)) + 1
        return max(1, level)
    
    def level_to_xp(self, level: int) -> int:
        """Calcule l'XP nécessaire pour atteindre un niveau"""
        if level <= 1:
            return 0
        
        multiplier = self.settings.get('level_multiplier', 100)
        # Formule : xp = (niveau - 1)² * multiplier
        return ((level - 1) ** 2) * multiplier
    
    def xp_for_next_level(self, current_xp: int) -> int:
        """Calcule l'XP nécessaire pour le prochain niveau"""
        current_level = self.xp_to_level(current_xp)
        next_level_xp = self.level_to_xp(current_level + 1)
        return next_level_xp - current_xp
    
    def progress_to_next_level(self, current_xp: int) -> tuple:
        """Retourne le progrès vers le prochain niveau"""
        current_level = self.xp_to_level(current_xp)
        current_level_xp = self.level_to_xp(current_level)
        next_level_xp = self.level_to_xp(current_level + 1)
        
        progress = current_xp - current_level_xp
        total_needed = next_level_xp - current_level_xp
        
        return progress, total_needed
    
    def get_level_info(self, xp: int) -> dict:
        """Retourne toutes les informations sur le niveau d'un utilisateur"""
        level = self.xp_to_level(xp)
        progress, total_needed = self.progress_to_next_level(xp)
        percentage = (progress / total_needed) * 100 if total_needed > 0 else 0
        
        return {
            'level': level,
            'xp': xp,
            'progress': progress,
            'total_needed': total_needed,
            'percentage': percentage,
            'xp_to_next': total_needed - progress
        }
