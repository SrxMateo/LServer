import os
import subprocess
import shutil
from lserver.state import add_node, remove_node, get_node, list_nodes, set_node_critical, set_node_backup
from lserver.ui import log_success, log_info, log_error, error_exit
import re

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
    subprocess.run(["screen", "-dmS", "lserver_daemon", "lserver", "--run-daemon"])
    log_success("LServer Daemon (Auto-Heal & Backups) iniciado en segundo plano.")

def stop_daemon():
    subprocess.run(["screen", "-S", "lserver_daemon", "-X", "quit"])
    log_success("LServer Daemon detenido.")

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

def is_running(name):
    validate_node_name(name)
    # Comprobar si hay una sesion de screen con este nombre
    try:
        result = subprocess.run(["screen", "-ls"], capture_output=True, text=True)
        return f".{name}\t" in result.stdout
    except FileNotFoundError:
        log_error("La utilidad 'screen' no está instalada. No se puede comprobar el estado.")
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

    # Iniciamos screen en modo detached (-dm)
    # y damos el nombre de sesion (-S)
    cmd = f"cd {path} && {start_cmd}"
    log_info(f"Arrancando nodo '{name}' en {path}...")
    try:
        subprocess.run(["screen", "-dmS", name, "bash", "-c", cmd], check=True)
        log_success(f"Nodo '{name}' arrancado y corriendo en segundo plano.")
    except subprocess.CalledProcessError as e:
        error_exit(f"Error al arrancar el nodo: {e}")
    except FileNotFoundError:
        error_exit("La utilidad 'screen' no está instalada.")

def stop_node(name):
    validate_node_name(name)
    if not get_node(name):
        error_exit(f"El nodo '{name}' no existe.")
    
    if not is_running(name):
        log_info(f"El nodo '{name}' no está corriendo.")
        return

    log_info(f"Deteniendo nodo '{name}' de forma segura...")
    try:
        subprocess.run(["screen", "-S", name, "-X", "quit"], check=True)
        log_success(f"Nodo '{name}' detenido.")
    except subprocess.CalledProcessError:
        error_exit(f"Fallo al intentar detener el nodo '{name}'.")
    except FileNotFoundError:
        error_exit("La utilidad 'screen' no está instalada.")

def kill_node(name):
    validate_node_name(name)
    if not get_node(name):
        error_exit(f"El nodo '{name}' no existe.")

    log_info(f"Matando forzosamente el nodo '{name}'...")
    # Usamos pkill para matar las sesiones de screen asociadas a este nodo
    subprocess.run(["pkill", "-f", f"SCREEN.*{name}"], capture_output=True)
    log_success(f"Señales de terminación enviadas a procesos de '{name}'.")

def enter_node(name):
    validate_node_name(name)
    if not get_node(name):
        error_exit(f"El nodo '{name}' no existe.")
    
    if not is_running(name):
        error_exit(f"El nodo '{name}' no está corriendo. Inícialo primero con -p.")
    
    log_info(f"Entrando al nodo '{name}'. Presiona Ctrl+A, y luego D para salir sin detenerlo.")
    try:
        subprocess.run(["screen", "-r", name])
    except FileNotFoundError:
        error_exit("La utilidad 'screen' no está instalada.")
    except Exception as e:
        error_exit(f"Error al entrar a la sesión: {e}")

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
