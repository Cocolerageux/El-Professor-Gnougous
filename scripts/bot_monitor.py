"""
Script de surveillance pour redémarrage automatique du bot
"""
import subprocess
import time
import logging
import os
import sys
from datetime import datetime

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_monitor.log'),
        logging.StreamHandler()
    ]
)

class BotMonitor:
    def __init__(self):
        self.bot_path = os.path.dirname(os.path.abspath(__file__))
        self.python_exe = os.path.join(self.bot_path, ".venv", "Scripts", "python.exe")
        self.main_script = os.path.join(self.bot_path, "main.py")
        self.restart_count = 0
        self.max_restarts_per_hour = 5
        self.restart_times = []
        
    def should_restart(self):
        """Vérifier si on peut redémarrer (limite les redémarrages fréquents)"""
        now = datetime.now()
        # Garder seulement les redémarrages de la dernière heure
        self.restart_times = [t for t in self.restart_times if (now - t).seconds < 3600]
        
        if len(self.restart_times) >= self.max_restarts_per_hour:
            logging.warning(f"Trop de redémarrages ({len(self.restart_times)}) dans la dernière heure")
            return False
        return True
        
    def run_bot(self):
        """Lance le bot et surveille son état"""
        while True:
            try:
                logging.info("🚀 Démarrage du bot Discord...")
                
                # Lancer le bot
                process = subprocess.Popen(
                    [self.python_exe, self.main_script],
                    cwd=self.bot_path,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                
                # Surveiller le processus
                while True:
                    output = process.stdout.readline()
                    if output:
                        print(output.strip())
                        
                    # Vérifier si le processus est toujours en vie
                    poll = process.poll()
                    if poll is not None:
                        # Le processus s'est arrêté
                        stderr_output = process.stderr.read()
                        if stderr_output:
                            logging.error(f"Erreur du bot: {stderr_output}")
                        
                        logging.warning(f"❌ Bot arrêté avec le code: {poll}")
                        break
                
                # Décider si on doit redémarrer
                if self.should_restart():
                    self.restart_times.append(datetime.now())
                    logging.info("⏳ Redémarrage dans 10 secondes...")
                    time.sleep(10)
                else:
                    logging.error("🛑 Arrêt du moniteur (trop de redémarrages)")
                    break
                    
            except KeyboardInterrupt:
                logging.info("🛑 Arrêt demandé par l'utilisateur")
                if 'process' in locals():
                    process.terminate()
                break
            except Exception as e:
                logging.error(f"❌ Erreur dans le moniteur: {e}")
                time.sleep(30)

if __name__ == "__main__":
    print("🤖 Moniteur du Bot Discord XP")
    print("Appuyez sur Ctrl+C pour arrêter")
    print("-" * 50)
    
    monitor = BotMonitor()
    monitor.run_bot()
