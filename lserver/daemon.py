"""Daemon de LServer: Auto-Heal con Backoff, Backups, Reinicios y Log Rotation."""
import time
import os
import datetime
import tarfile
from lserver.state import list_nodes
from lserver.core import is_running, start_node, stop_node
from lserver.ui import log_info, log_error

# Backoff tracking: {node_name: {'fails': count, 'last_fail': timestamp, 'backoff': seconds}}
_backoff_state = {}

MAX_FAILS = 5
INITIAL_BACKOFF = 10  # segundos
MAX_BACKOFF = 300     # 5 minutos
MAX_LOG_SIZE = 50 * 1024 * 1024  # 50MB
MAX_LOG_FILES = 3

def _rotate_logs(node_name, node_path):
    """Rota el server.log si supera MAX_LOG_SIZE."""
    log_file = os.path.join(node_path, "server.log")
    if not os.path.exists(log_file):
        return
    
    try:
        size = os.path.getsize(log_file)
        if size < MAX_LOG_SIZE:
            return
        
        log_info(f"Log rotation para '{node_name}' ({size // (1024*1024)}MB)...")
        
        # Desplazar archivos existentes: .3 -> borrar, .2 -> .3, .1 -> .2, log -> .1
        for i in range(MAX_LOG_FILES, 1, -1):
            old = os.path.join(node_path, f"server.log.{i-1}")
            new = os.path.join(node_path, f"server.log.{i}")
            if os.path.exists(old):
                if i == MAX_LOG_FILES and os.path.exists(new):
                    os.remove(new)
                os.rename(old, new)
        
        # Mover el log actual a .1
        rotated = os.path.join(node_path, "server.log.1")
        os.rename(log_file, rotated)
        
        # Crear un nuevo log vacio
        with open(log_file, "w") as f:
            f.write(f"--- Log rotado el {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        
        log_info(f"Log rotation completado para '{node_name}'.")
    except Exception as e:
        log_error(f"Error en log rotation para '{node_name}': {e}")

def _handle_autoheal(name, data):
    """Auto-Heal con backoff exponencial inteligente."""
    global _backoff_state
    
    if name not in _backoff_state:
        _backoff_state[name] = {'fails': 0, 'last_fail': 0, 'backoff': INITIAL_BACKOFF}
    
    state = _backoff_state[name]
    
    # Si se supero el maximo de fallos, desactivar auto-heal
    if state['fails'] >= MAX_FAILS:
        # Solo logear una vez cada 5 minutos
        if time.time() - state.get('last_log', 0) > 300:
            log_error(f"Auto-Heal SUSPENDIDO para '{name}' tras {MAX_FAILS} fallos consecutivos.")
            state['last_log'] = time.time()
            
            # Enviar alerta webhook
            try:
                from lserver.alerts import send_alert
                send_alert(
                    "⚠️ Auto-Heal Suspendido",
                    f"El nodo **{name}** ha fallado {MAX_FAILS} veces consecutivas. Auto-Heal ha sido suspendido.",
                    color=0xFF0000
                )
            except Exception:
                pass
        return
    
    # Respetar el backoff
    if time.time() - state['last_fail'] < state['backoff']:
        return
    
    log_info(f"Auto-Heal: reiniciando nodo critico '{name}' (intento {state['fails'] + 1})...")
    try:
        start_node(name)
        # Exito: resetear backoff
        _backoff_state[name] = {'fails': 0, 'last_fail': 0, 'backoff': INITIAL_BACKOFF}
        
        try:
            from lserver.alerts import send_alert
            send_alert(
                "✅ Nodo Revivido",
                f"El nodo **{name}** fue revivido por Auto-Heal.",
                color=0x00FF00
            )
        except Exception:
            pass
    except Exception as e:
        state['fails'] += 1
        state['last_fail'] = time.time()
        state['backoff'] = min(state['backoff'] * 2, MAX_BACKOFF)
        log_error(f"Fallo al revivir '{name}': {e} (proximo intento en {state['backoff']}s)")

def _handle_scheduled_restart(name, data, now):
    """Reinicio programado si la hora coincide."""
    restart_time = data.get('restart_time', '') or ''
    if not restart_time:
        return
    
    try:
        hour, minute = map(int, restart_time.split(':'))
    except (ValueError, AttributeError):
        return
    
    if now.hour == hour and now.minute == minute:
        # Usar marker para no repetir el reinicio
        marker_file = os.path.join(data['path'], f".restart_{now.strftime('%Y%m%d')}")
        if os.path.exists(marker_file):
            return
        
        log_info(f"Reinicio programado para '{name}' a las {restart_time}...")
        try:
            if is_running(name):
                stop_node(name)
                time.sleep(2)
            start_node(name)
            
            with open(marker_file, "w") as f:
                f.write("done")
            
            log_info(f"Reinicio programado completado para '{name}'.")
            
            try:
                from lserver.alerts import send_alert
                send_alert(
                    "🔄 Reinicio Programado",
                    f"El nodo **{name}** fue reiniciado a las {restart_time} segun lo programado.",
                    color=0x3498DB
                )
            except Exception:
                pass
        except Exception as e:
            log_error(f"Error en reinicio programado de '{name}': {e}")

def _handle_backup(name, data, now):
    """Backup automatico a las 03:00 AM."""
    if not data.get('backup_enabled'):
        return
    
    if now.hour == 3 and now.minute < 5:
        backup_marker = os.path.join(data['path'], f".backup_{now.strftime('%Y%m%d')}")
        if os.path.exists(backup_marker):
            return
        
        log_info(f"Iniciando backup programado para '{name}'...")
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
            
            with open(backup_marker, "w") as f:
                f.write("done")
            log_info(f"Backup nocturno completado para '{name}'.")
        except Exception as e:
            log_error(f"Error al generar backup para '{name}': {e}")

def run_daemon():
    """Loop principal del daemon."""
    log_info("Daemon v3 inicializado. Monitoreando Auto-Heal, Backups, Reinicios y Log Rotation...")
    while True:
        try:
            nodes = list_nodes()
            now = datetime.datetime.now()
            
            for name, data in nodes.items():
                # 1. LOG ROTATION
                _rotate_logs(name, data['path'])
                
                # 2. AUTO-HEAL con BACKOFF
                if data.get('is_critical') and not is_running(name):
                    _handle_autoheal(name, data)
                elif data.get('is_critical') and is_running(name):
                    # Si esta online, resetear backoff
                    if name in _backoff_state:
                        _backoff_state[name] = {'fails': 0, 'last_fail': 0, 'backoff': INITIAL_BACKOFF}
                
                # 3. REINICIOS PROGRAMADOS
                _handle_scheduled_restart(name, data, now)
                
                # 4. BACKUPS
                _handle_backup(name, data, now)
                            
        except Exception as e:
            log_error(f"Error en el ciclo del Daemon: {e}")
            
        time.sleep(60)
