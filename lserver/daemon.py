import time
import os
import datetime
import subprocess
import tarfile
from lserver.state import list_nodes
from lserver.core import is_running, start_node
from lserver.ui import log_info, log_error

def run_daemon():
    log_info("Daemon inicializado. Monitoreando Auto-Heal y Backups 24/7...")
    while True:
        try:
            nodes = list_nodes()
            now = datetime.datetime.now()
            
            for name, data in nodes.items():
                # 1. AUTO-HEAL (Watchdog)
                if data['is_critical']:
                    if not is_running(name):
                        log_info(f"Auto-Heal detectó que el nodo crítico '{name}' está caído. Reiniciando...")
                        try:
                            start_node(name)
                        except Exception as e:
                            log_error(f"Fallo al revivir el nodo '{name}': {e}")
                            
                # 2. AUTO-BACKUPS (03:00 AM)
                if data['backup_enabled']:
                    if now.hour == 3 and now.minute < 5:
                        backup_marker = os.path.join(data['path'], f".backup_{now.strftime('%Y%m%d')}")
                        if not os.path.exists(backup_marker):
                            log_info(f"Iniciando backup programado para el nodo '{name}'...")
                            backup_dir = os.path.join(data['path'], "backups")
                            os.makedirs(backup_dir, exist_ok=True)
                            backup_file = os.path.join(backup_dir, f"backup_{now.strftime('%Y%m%d_%H%M%S')}.tar.gz")
                            
                            try:
                                def filter_backups(tarinfo):
                                    if "backups" in tarinfo.name:
                                        return None
                                    return tarinfo
                                
                                with tarfile.open(backup_file, "w:gz") as tar:
                                    tar.add(data['path'], arcname=name, filter=filter_backups)
                                
                                # Escribimos el marker para no volver a hacerlo hoy
                                with open(backup_marker, "w") as f:
                                    f.write("done")
                                log_info(f"Backup nocturno completado para '{name}'.")
                            except Exception as e:
                                log_error(f"Error fatal al generar backup para '{name}': {e}")
                                
        except Exception as e:
            log_error(f"Error en el ciclo del Daemon: {e}")
            
        time.sleep(60) # Intervalo de chequeo (1 minuto)
