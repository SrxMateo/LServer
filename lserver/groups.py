"""Sistema de grupos de nodos para LServer."""
import re
from lserver.db import DBConnection
from lserver.ui import log_success, log_info, log_error, error_exit
from lserver.state import get_node

db = DBConnection()

def _validate_name(name):
    if not re.match(r'^[a-zA-Z0-9_-]+$', name):
        error_exit("Nombre invalido. Solo se permiten letras, numeros, guiones y guiones bajos.")

def create_group(name):
    _validate_name(name)
    existing = get_group_nodes(name)
    if existing is not None:
        log_info(f"El grupo '{name}' ya existe con {len(existing)} nodos.")
        return
    # Insertamos un registro vacio para marcar el grupo como existente
    db.execute('INSERT OR IGNORE INTO groups_nodes (group_name, node_name) VALUES (?, ?)', (name, '__group_marker__'))
    log_success(f"Grupo '{name}' creado.")

def delete_group(name):
    _validate_name(name)
    db.execute('DELETE FROM groups_nodes WHERE group_name = ?', (name,))
    log_success(f"Grupo '{name}' eliminado.")

def add_to_group(group_name, node_name):
    _validate_name(group_name)
    _validate_name(node_name)
    node = get_node(node_name)
    if not node:
        error_exit(f"El nodo '{node_name}' no existe.")
    db.execute('INSERT OR IGNORE INTO groups_nodes (group_name, node_name) VALUES (?, ?)', (group_name, node_name))
    log_success(f"Nodo '{node_name}' agregado al grupo '{group_name}'.")

def remove_from_group(group_name, node_name):
    _validate_name(group_name)
    _validate_name(node_name)
    db.execute('DELETE FROM groups_nodes WHERE group_name = ? AND node_name = ?', (group_name, node_name))
    log_success(f"Nodo '{node_name}' removido del grupo '{group_name}'.")

def get_group_nodes(group_name):
    rows = db.fetchall('SELECT node_name FROM groups_nodes WHERE group_name = ?', (group_name,))
    if not rows:
        return None
    return [r['node_name'] for r in rows if r['node_name'] != '__group_marker__']

def list_groups():
    rows = db.fetchall('SELECT DISTINCT group_name FROM groups_nodes')
    result = {}
    for row in rows:
        gname = row['group_name']
        nodes = get_group_nodes(gname)
        result[gname] = nodes if nodes else []
    return result

def start_group(group_name):
    _validate_name(group_name)
    nodes = get_group_nodes(group_name)
    if nodes is None:
        error_exit(f"El grupo '{group_name}' no existe.")
    if not nodes:
        log_info(f"El grupo '{group_name}' esta vacio.")
        return
    
    from lserver.core import start_node, is_running
    log_info(f"Arrancando grupo '{group_name}' ({len(nodes)} nodos)...")
    for name in nodes:
        try:
            if not is_running(name):
                start_node(name)
            else:
                log_info(f"  '{name}' ya esta corriendo.")
        except SystemExit:
            pass
    log_success(f"Grupo '{group_name}' arrancado.")

def stop_group(group_name):
    _validate_name(group_name)
    nodes = get_group_nodes(group_name)
    if nodes is None:
        error_exit(f"El grupo '{group_name}' no existe.")
    if not nodes:
        log_info(f"El grupo '{group_name}' esta vacio.")
        return
    
    from lserver.core import stop_node, is_running
    log_info(f"Deteniendo grupo '{group_name}' ({len(nodes)} nodos)...")
    for name in nodes:
        try:
            if is_running(name):
                stop_node(name)
            else:
                log_info(f"  '{name}' no esta corriendo.")
        except SystemExit:
            pass
    log_success(f"Grupo '{group_name}' detenido.")

def show_groups():
    groups = list_groups()
    if not groups:
        log_info("No hay grupos creados.")
        return
    
    GOLD = "\033[38;5;220m"
    ORANGE = "\033[38;5;208m"
    RESET = "\033[0m"
    
    print(f"\n{GOLD}Grupos de Nodos:{RESET}")
    for gname, nodes in groups.items():
        node_list = ", ".join(nodes) if nodes else "(vacio)"
        print(f"  {ORANGE}{gname}{RESET}: {node_list}")
    print()
