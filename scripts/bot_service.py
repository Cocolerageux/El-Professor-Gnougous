"""
Script pour installer le bot comme service Windows
Nécessite: pip install pywin32
"""
import sys
import os
import subprocess
import time
import logging

# Vérifier et importer les modules Windows
try:
    import win32serviceutil
    import win32service
    import win32event
    import servicemanager
    WINDOWS_SERVICE_AVAILABLE = True
except ImportError as e:
    WINDOWS_SERVICE_AVAILABLE = False
    print("❌ Modules Windows manquants !")
    print("Pour installer le service Windows, exécutez :")
    print("pip install pywin32")
    print(f"Erreur d'import : {e}")
    print()
    print("Alternative : Utilisez les fichiers .bat pour gérer le bot")

# Classe du service Windows (seulement si les modules sont disponibles)
if WINDOWS_SERVICE_AVAILABLE:
    class DiscordBotService(win32serviceutil.ServiceFramework):
        _svc_name_ = "DiscordBotXP"
        _svc_display_name_ = "Discord Bot XP Service"
        _svc_description_ = "Service pour faire tourner le bot Discord avec système d'XP 24h/24"
        
        def __init__(self, args):
            win32serviceutil.ServiceFramework.__init__(self, args)
            self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
            self.is_alive = True
            
            # Chemin vers le script principal
            self.bot_path = os.path.dirname(os.path.abspath(__file__))
            self.python_exe = os.path.join(self.bot_path, ".venv", "Scripts", "python.exe")
            self.main_script = os.path.join(self.bot_path, "main.py")
            
            # Configuration du logging
            logging.basicConfig(
                filename=os.path.join(self.bot_path, "service.log"),
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
            
        def SvcStop(self):
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            win32event.SetEvent(self.hWaitStop)
            self.is_alive = False
            logging.info("Service arrêté")
            
        def SvcDoRun(self):
            servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STARTED,
                (self._svc_name_, '')
            )
            
            logging.info("Service démarré")
            self.main()
            
        def main(self):
            while self.is_alive:
                try:
                    # Lancer le bot
                    logging.info("Démarrage du bot Discord...")
                    process = subprocess.Popen(
                        [self.python_exe, self.main_script],
                        cwd=self.bot_path,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    
                    # Surveiller le processus
                    while self.is_alive and process.poll() is None:
                        if win32event.WaitForSingleObject(self.hWaitStop, 1000) == win32event.WAIT_OBJECT_0:
                            process.terminate()
                            break
                    
                    # Si le processus s'arrête de manière inattendue, le redémarrer
                    if self.is_alive and process.poll() is not None:
                        logging.warning(f"Bot arrêté de manière inattendue (code: {process.returncode})")
                        logging.info("Redémarrage dans 10 secondes...")
                        time.sleep(10)
                        
                except Exception as e:
                    logging.error(f"Erreur dans le service : {e}")
                    time.sleep(30)  # Attendre avant de réessayer

else:
    # Classe factice si les modules Windows ne sont pas disponibles
    class DiscordBotService:
        def __init__(self, *args):
            pass

if __name__ == '__main__':
    if not WINDOWS_SERVICE_AVAILABLE:
        print("❌ Les modules Windows (pywin32) ne sont pas installés !")
        print()
        print("🔧 Pour installer les dépendances :")
        print("   pip install pywin32")
        print()
        print("📁 Alternative recommandée :")
        print("   - Utilisez start_bot.bat pour démarrer le bot")
        print("   - Utilisez stop_bot.bat pour l'arrêter")
        print("   - Utilisez restart_bot.bat pour le redémarrer")
        print()
        input("Appuyez sur Entrée pour continuer...")
        sys.exit(1)
    
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(DiscordBotService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(DiscordBotService)
