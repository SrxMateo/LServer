"""Sistema de grupos de nodos para LServer — Rediseño v4."""
import re
from lserver.db import DBConnection
from lserver.ui import (log_success, log_info, log_error, error_exit,
                        print_menu, GOLD, ORANGE, LIGHT_ORANGE, GREEN,
                        RED, GRAY, WHITE, CYAN, YELLOW, RESET, BOLD, _clean)

db = DBConnection()

# Crear tabla si no existe
db.execute('''CREATE TABLE IF NOT EXISTS groups_nodes
              (group_name TEXT, node_name TEXT, PRIMARY KEY(group_name, node_name))''')


def _validate_name(name):
    if not re.match(r'^[a-zA-Z0-9_-]+$', name):
        error_exit("Nombre inválido. Solo se permiten letras, números, guiones y guiones bajos.")


def create_group(name):
    """Crea un grupo y opcionalmente asigna nodos al mismo."""
    _validate_name(name)
    existing = get_group_nodes(name)
    if existing is not None:
        log_info(f"El grupo '{name}' ya existe con {len(existing)} nodo(s).")
        return

    db.execute('INSERT OR IGNORE INTO groups_nodes (group_name, node_name) VALUES (?, ?)',
               (name, '__group_marker__'))
    log_success(f"Grupo '{name}' creado exitosamente.")

    # Prompt interactivo limpio
    from lserver.state import list_nodes
    all_nodes = list(list_nodes().keys())
    if all_nodes:
        log_info(f"Nodos disponibles: {GOLD}{', '.join(all_nodes)}{RESET}")
    else:
        log_info("No hay nodos creados todavía. Crea uno con: lserver -c <nombre>")
        return

    print(f"\n  {LIGHT_ORANGE}Escribe los nombres de los nodos separados por coma")
    print(f"  {GRAY}(o presiona Enter para dejarlo vacío){RESET}")
    nodos_input = input(f"  {GOLD}➤{RESET}  Nodos: ").strip()
    if nodos_input:
        nodos_lista = [n.strip() for n in nodos_input.split(",") if n.strip()]
        added = 0
        for n in nodos_lista:
            from lserver.state import get_node
            if get_node(n):
                db.execute('INSERT OR IGNORE INTO groups_nodes (group_name, node_name) VALUES (?, ?)',
                           (name, n))
                log_success(f"  Nodo '{n}' agregado al grupo.")
                added += 1
            else:
                log_error(f"  El nodo '{n}' no existe, omitiendo.")
        if added > 0:
            log_success(f"Grupo '{name}' listo con {added} nodo(s).")


def delete_group(name):
    """Elimina un grupo (no borra los nodos, solo el grupo)."""
    _validate_name(name)
    nodes = get_group_nodes(name)
    if nodes is None:
        error_exit(f"El grupo '{name}' no existe.")

    db.execute('DELETE FROM groups_nodes WHERE group_name = ?', (name,))
    log_success(f"Grupo '{name}' eliminado.")
    log_info("Los nodos y sus carpetas NO han sido eliminados.")


def add_to_group(group_name, node_name):
    """Agrega un nodo a un grupo existente."""
    _validate_name(group_name)
    _validate_name(node_name)

    # Verificar que el grupo exista
    if get_group_nodes(group_name) is None:
        error_exit(f"El grupo '{group_name}' no existe. Créalo con: lserver group create {group_name}")

    from lserver.state import get_node
    node = get_node(node_name)
    if not node:
        error_exit(f"El nodo '{node_name}' no existe. Créalo con: lserver -c {node_name}")

    db.execute('INSERT OR IGNORE INTO groups_nodes (group_name, node_name) VALUES (?, ?)',
               (group_name, node_name))
    log_success(f"Nodo '{node_name}' agregado al grupo '{group_name}'.")


def remove_from_group(group_name, node_name):
    """Quita un nodo de un grupo sin borrarlo."""
    _validate_name(group_name)
    _validate_name(node_name)
    db.execute('DELETE FROM groups_nodes WHERE group_name = ? AND node_name = ?',
               (group_name, node_name))
    log_success(f"Nodo '{node_name}' retirado del grupo '{group_name}'.")
    log_info(f"Los archivos de '{node_name}' NO han sido borrados.")


def get_group_nodes(group_name):
    """Retorna lista de nodos del grupo, o None si el grupo no existe."""
    rows = db.fetchall('SELECT node_name FROM groups_nodes WHERE group_name = ?', (group_name,))
    if not rows:
        return None
    return [r['node_name'] for r in rows if r['node_name'] != '__group_marker__']


def list_groups():
    """Retorna dict {nombre_grupo: [nodos]}."""
    rows = db.fetchall('SELECT DISTINCT group_name FROM groups_nodes')
    result = {}
    for row in rows:
        gname = row['group_name']
        nodes = get_group_nodes(gname)
        result[gname] = nodes if nodes else []
    return result


def start_group(group_name):
    """Enciende todos los nodos de un grupo."""
    _validate_name(group_name)
    nodes = get_group_nodes(group_name)
    if nodes is None:
        error_exit(f"El grupo '{group_name}' no existe.")
    if not nodes:
        log_info(f"El grupo '{group_name}' está vacío. Agrega nodos con: lserver group add {group_name} <nodo>")
        return

    from lserver.core import start_node, is_running
    log_info(f"Encendiendo grupo '{group_name}' ({len(nodes)} nodo(s))...")
    ok = 0
    for name in nodes:
        try:
            if not is_running(name):
                start_node(name)
                ok += 1
            else:
                log_info(f"  '{name}' ya está corriendo.")
        except SystemExit:
            log_error(f"  No se pudo encender '{name}'.")
    log_success(f"Grupo '{group_name}': {ok}/{len(nodes)} nodo(s) encendidos.")


def stop_group(group_name):
    """Apaga todos los nodos de un grupo."""
    _validate_name(group_name)
    nodes = get_group_nodes(group_name)
    if nodes is None:
        error_exit(f"El grupo '{group_name}' no existe.")
    if not nodes:
        log_info(f"El grupo '{group_name}' está vacío.")
        return

    from lserver.core import stop_node, is_running
    log_info(f"Apagando grupo '{group_name}' ({len(nodes)} nodo(s))...")
    ok = 0
    for name in nodes:
        try:
            if is_running(name):
                stop_node(name)
                ok += 1
            else:
                log_info(f"  '{name}' ya estaba apagado.")
        except SystemExit:
            log_error(f"  No se pudo apagar '{name}'.")
    log_success(f"Grupo '{group_name}': {ok}/{len(nodes)} nodo(s) detenidos.")


def show_groups():
    """Muestra todos los grupos con sus nodos y estado ONLINE/OFFLINE."""
    groups = list_groups()
    if not groups:
        log_info("No hay grupos creados.")
        log_info(f"Crea uno con: {GOLD}lserver group create <nombre>{RESET}")
        return

    from lserver.core import is_running
    width = 58
    c = LIGHT_ORANGE

    print(f"\n{c}╔{'═' * width}╗{RESET}")
    title = f"  {GOLD}👥 GRUPOS DE NODOS{RESET}"
    pad = width - len(_clean(title)) - 1
    print(f"{c}║{RESET}{title}{' ' * max(0, pad)}{c}║{RESET}")

    for i, (gname, nodes) in enumerate(groups.items()):
        print(f"{c}╠{'═' * width}╣{RESET}")
        online = sum(1 for n in nodes if is_running(n))
        offline = len(nodes) - online
        header = f"  {ORANGE}{BOLD}{gname}{RESET}  {GRAY}({len(nodes)} nodo(s) · {GREEN}●{GRAY}{online} online · {RED}×{GRAY}{offline} offline){RESET}"
        pad = width - len(_clean(header)) - 1
        print(f"{c}║{RESET}{header}{' ' * max(0, pad)}{c}║{RESET}")

        if not nodes:
            empty = f"    {GRAY}(vacío — usa: lserver group add {gname} <nodo>){RESET}"
            pad = width - len(_clean(empty)) - 1
            print(f"{c}║{RESET}{empty}{' ' * max(0, pad)}{c}║{RESET}")
        else:
            for n in nodes:
                if is_running(n):
                    status = f"{GREEN}● ONLINE {RESET}"
                else:
                    status = f"{RED}× OFFLINE{RESET}"
                row = f"    {status}  {WHITE}{n}{RESET}"
                pad = width - len(_clean(row)) - 1
                print(f"{c}║{RESET}{row}{' ' * max(0, pad)}{c}║{RESET}")

    print(f"{c}╠{'═' * width}╣{RESET}")
    # Footer con ayuda rápida
    cmds = [
        f"  {GOLD}lserver group start <grupo>{RESET}  {GRAY}Encender todo{RESET}",
        f"  {GOLD}lserver group stop  <grupo>{RESET}  {GRAY}Apagar todo{RESET}",
        f"  {GOLD}lserver group add   <grupo> <nodo>{RESET}  {GRAY}Agregar nodo{RESET}",
    ]
    for cmd in cmds:
        pad = width - len(_clean(cmd)) - 1
        print(f"{c}║{RESET}{cmd}{' ' * max(0, pad)}{c}║{RESET}")
    print(f"{c}╚{'═' * width}╝{RESET}\n")


def interactive_group_menu():
    """Menú interactivo principal de grupos."""
    ans = print_menu(
        title="GESTIÓN DE GRUPOS",
        options=[
            ("1", "Crear nuevo grupo"),
            ("2", "Listar todos los grupos con estado"),
            ("3", "Agregar nodo a un grupo"),
            ("4", "Quitar nodo de un grupo (no borra archivos)"),
            ("5", "Encender grupo completo"),
            ("6", "Apagar grupo completo"),
            ("7", "Eliminar grupo"),
            ("0", "Cancelar"),
        ]
    )

    if ans == "1":
        name = input(f"  {GOLD}➤{RESET}  Nombre del nuevo grupo: ").strip()
        if name:
            create_group(name)
    elif ans == "2":
        show_groups()
    elif ans == "3":
        gname = input(f"  {GOLD}➤{RESET}  Nombre del grupo: ").strip()
        nname = input(f"  {GOLD}➤{RESET}  Nombre del nodo a agregar: ").strip()
        if gname and nname:
            add_to_group(gname, nname)
    elif ans == "4":
        gname = input(f"  {GOLD}➤{RESET}  Nombre del grupo: ").strip()
        nname = input(f"  {GOLD}➤{RESET}  Nombre del nodo a quitar: ").strip()
        if gname and nname:
            remove_from_group(gname, nname)
    elif ans == "5":
        gname = input(f"  {GOLD}➤{RESET}  Nombre del grupo a encender: ").strip()
        if gname:
            start_group(gname)
    elif ans == "6":
        gname = input(f"  {GOLD}➤{RESET}  Nombre del grupo a apagar: ").strip()
        if gname:
            stop_group(gname)
    elif ans == "7":
        gname = input(f"  {GOLD}➤{RESET}  Nombre del grupo a eliminar: ").strip()
        if gname:
            ans2 = input(f"  {RED}¿Confirmas eliminar el grupo '{gname}'? (s/N): {RESET}").strip().lower()
            if ans2 == "s":
                delete_group(gname)
    else:
        log_info("Operación cancelada.")
