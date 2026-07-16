import os
import subprocess
import shutil
import signal
import re
from lserver.state import add_node, remove_node, get_node, list_nodes, set_node_critical, set_node_backup
from lserver.ui import log_success, log_info, log_error, error_exit

def validate_node_name(name):
    if not re.match(r'^[a-zA-Z0-9_-]+$', name):
        error_exit("ERROR DE SEGURIDAD: El nombre del nodo contiene caracteres inválidos. Solo se permiten letras, números, guiones y guiones bajos.")

def toggle_critical(name):
    validate_node_name(name)
    node = get_node(name)
    if not node:
        log_error(f"El nodo '{name}' no existe.")
        return
    new_state = not node.get('is_critical', False)
    set_node_critical(name, new_state)
    estado = "ACTIVADO" if new_state else "DESACTIVADO"
    log_success(f"Auto-Heal para '{name}' ha sido {estado}.")

def handle_backup(name):
    validate_node_name(name)
    node = get_node(name)
    if not node:
        log_error(f"El nodo '{name}' no existe.")
        return
    
    print(f"\n\033[38;5;220mOpciones de Backup para el nodo '{name}':\033[0m")
    print("1) Backup Manual (Crear copia de seguridad ahora mismo)")
    print("2) Backup Automático (Cada 24h a las 03:00 AM)")
    print("3) Desactivar Backup Automático")
    print("0) Cancelar\n")
    
    ans = input("Elige una opción (0-3): ")
    if ans == "1":
        create_manual_backup(name, node['path'])
    elif ans == "2":
        set_node_backup(name, True)
        log_success(f"Auto-Backups 24H ACTIVADOS para '{name}'.")
    elif ans == "3":
        set_node_backup(name, False)
        log_success(f"Auto-Backups 24H DESACTIVADOS para '{name}'.")
    else:
        log_info("Operación cancelada.")

def create_manual_backup(name, path):
    validate_node_name(name)
    import datetime
    import tarfile
    now = datetime.datetime.now()
    log_info(f"Creando backup manual para '{name}'...")
    backup_dir = os.path.join(path, "backups")
    os.makedirs(backup_dir, exist_ok=True)
    backup_file = os.path.join(backup_dir, f"backup_manual_{now.strftime('%Y%m%d_%H%M%S')}.tar.gz")
    
    try:
        def filter_backups(tarinfo):
            if "backups" in tarinfo.name:
                return None
            return tarinfo
        
        with tarfile.open(backup_file, "w:gz") as tar:
            tar.add(path, arcname=name, filter=filter_backups)
        log_success(f"Backup manual guardado exitosamente en:\n  {backup_file}")
    except Exception as e:
        log_error(f"Fallo al crear el backup: {e}")

def start_daemon():
    pid_file = os.path.expanduser("~/.lserver_daemon.pid")
    log_file = os.path.expanduser("~/.lserver_daemon.log")
    
    if os.path.exists(pid_file):
        with open(pid_file, "r") as f:
            try:
                pid = int(f.read().strip())
                os.killpg(pid, 0)
                log_info("LServer Daemon ya está corriendo.")
                return
            except (ValueError, OSError):
                pass
                
    f_log = open(log_file, "a")
    process = subprocess.Popen(
        ["lserver", "--run-daemon"],
        stdout=f_log, stderr=subprocess.STDOUT,
        start_new_session=True
    )
    with open(pid_file, "w") as f:
        f.write(str(process.pid))
    log_success("LServer Daemon iniciado en segundo plano (Python Puro).")

def stop_daemon():
    pid_file = os.path.expanduser("~/.lserver_daemon.pid")
    if os.path.exists(pid_file):
        with open(pid_file, "r") as f:
            try:
                pid = int(f.read().strip())
                os.killpg(pid, signal.SIGTERM)
                log_success("LServer Daemon detenido.")
            except (ValueError, OSError):
                log_info("LServer Daemon no estaba corriendo.")
        os.remove(pid_file)
    else:
        log_info("LServer Daemon no está corriendo.")

def create_node(name):
    validate_node_name(name)
    if get_node(name):
        error_exit(f"El nodo '{name}' ya existe.")
    
    # Crear carpeta en el directorio actual
    current_dir = os.getcwd()
    node_path = os.path.join(current_dir, name)
    
    if os.path.exists(node_path):
        log_info(f"La carpeta {node_path} ya existe. Se vinculará a este nodo.")
    else:
        try:
            os.makedirs(node_path)
            log_success(f"Directorio creado en {node_path}")
        except Exception as e:
            error_exit(f"No se pudo crear el directorio: {e}")

    # Crear script de inicio por defecto si no existe
    start_script = os.path.join(node_path, "start.sh")
    if not os.path.exists(start_script):
        with open(start_script, "w") as f:
            f.write("#!/bin/bash\n")
            f.write("echo 'Iniciando LServer Nodo: " + name + "'\n")
            f.write("# Agrega aquí el comando para iniciar tu servidor (ej: npm start, node index.js)\n")
            f.write("while true; do sleep 1000; done\n")
        os.chmod(start_script, 0o755)
        log_info(f"Se ha creado un script de inicio por defecto en {start_script}")

    add_node(name, node_path, "./start.sh")
    log_success(f"Nodo '{name}' creado exitosamente.")

def get_node_pid_file(name):
    node = get_node(name)
    if node:
        return os.path.join(node["path"], "server.pid")
    return None

def is_running(name):
    validate_node_name(name)
    pid_file = get_node_pid_file(name)
    if not pid_file or not os.path.exists(pid_file):
        return False
    
    with open(pid_file, "r") as f:
        try:
            pid = int(f.read().strip())
            os.killpg(pid, 0)
            return True
        except (ValueError, OSError):
            return False

def start_node(name):
    validate_node_name(name)
    node = get_node(name)
    if not node:
        error_exit(f"El nodo '{name}' no existe. Créalo primero con -c.")
    
    if is_running(name):
        error_exit(f"El nodo '{name}' ya está corriendo.")

    path = node["path"]
    start_cmd = node["start_cmd"]
    
    if not os.path.exists(path):
        error_exit(f"La ruta del nodo no existe: {path}")

    log_info(f"Arrancando nodo '{name}' en {path}...")
    try:
        log_file_path = os.path.join(path, "server.log")
        f_log = open(log_file_path, "a")
        
        process = subprocess.Popen(
            ["bash", "-c", start_cmd],
            cwd=path,
            stdout=f_log,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            start_new_session=True
        )
        
        pid_file = os.path.join(path, "server.pid")
        with open(pid_file, "w") as f:
            f.write(str(process.pid))
            
        log_success(f"Nodo '{name}' arrancado en segundo plano (PID: {process.pid}).")
    except Exception as e:
        error_exit(f"Error al arrancar el nodo: {e}")

def stop_node(name):
    validate_node_name(name)
    if not get_node(name):
        error_exit(f"El nodo '{name}' no existe.")
    
    if not is_running(name):
        log_info(f"El nodo '{name}' no está corriendo.")
        return

    log_info(f"Deteniendo nodo '{name}' de forma segura...")
    pid_file = get_node_pid_file(name)
    with open(pid_file, "r") as f:
        pid = int(f.read().strip())
    
    try:
        os.killpg(pid, signal.SIGTERM)
        log_success(f"Nodo '{name}' detenido.")
    except OSError as e:
        error_exit(f"Fallo al intentar detener el nodo '{name}': {e}")
    
    if os.path.exists(pid_file):
        os.remove(pid_file)

def kill_node(name):
    validate_node_name(name)
    if not get_node(name):
        error_exit(f"El nodo '{name}' no existe.")

    log_info(f"Matando forzosamente el nodo '{name}'...")
    if is_running(name):
        pid_file = get_node_pid_file(name)
        with open(pid_file, "r") as f:
            pid = int(f.read().strip())
        try:
            os.killpg(pid, signal.SIGKILL)
            log_success(f"Señal SIGKILL enviada al proceso de '{name}'.")
        except OSError as e:
            log_error(f"Error al matar proceso: {e}")
        
        if os.path.exists(pid_file):
            os.remove(pid_file)
    else:
        log_info(f"El nodo '{name}' no estaba corriendo.")

def enter_node(name):
    validate_node_name(name)
    node = get_node(name)
    if not node:
        error_exit(f"El nodo '{name}' no existe.")
    
    if not is_running(name):
        error_exit(f"El nodo '{name}' no está corriendo. Inícialo primero con -p.")
    
    log_info(f"Mostrando consola en vivo de '{name}'. Haz scroll hacia arriba para ver el historial.")
    log_info("Presiona Ctrl+C para salir.")
    try:
        log_file_path = os.path.join(node["path"], "server.log")
        if not os.path.exists(log_file_path):
            error_exit("El archivo de log aún no existe.")
        
        # 'tail -n +1 -f' imprime desde la línea 1 hasta el final y se queda escuchando
        subprocess.run(["tail", "-n", "+1", "-f", log_file_path])
    except KeyboardInterrupt:
        print("\nSaliendo del log en vivo.")
    except Exception as e:
        error_exit(f"Error al leer el log: {e}")

def list_all_nodes():
    nodes = list_nodes()
    from lserver.ui import print_dashboard
    print_dashboard(nodes, is_running)

def delete_node(name):
    validate_node_name(name)
    node = get_node(name)
    if not node:
        error_exit(f"El nodo '{name}' no existe.")
    
    if is_running(name):
        log_info(f"El nodo '{name}' está corriendo. Deteniéndolo primero...")
        stop_node(name)
    
    path = node["path"]
    
    # Preguntar si se quiere borrar la carpeta
    ans = input(f"¿Deseas eliminar también la carpeta física del nodo en {path}? (s/N): ")
    if ans.lower() == 's':
        try:
            shutil.rmtree(path)
            log_success(f"Carpeta {path} eliminada.")
        except Exception as e:
            log_error(f"No se pudo eliminar la carpeta: {e}")
    else:
        log_info("La carpeta física se ha conservado.")

    remove_node(name)
    log_success(f"Nodo '{name}' eliminado de la base de datos.")
