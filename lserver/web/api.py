"""API REST para el panel web de LServer."""
import os
import base64
import shutil

def api_nodes():
    """Retorna lista de todos los nodos con su estado y metricas."""
    try:
        from lserver.state import list_nodes
        from lserver.core import is_running, get_node_resources, get_node_ports, get_current_uptime, format_uptime
        
        nodes = list_nodes()
        result = []
        for name, data in nodes.items():
            running = is_running(name)
            node_info = {
                'name': name,
                'path': data.get('path', ''),
                'status': 'online' if running else 'offline',
                'is_critical': bool(data.get('is_critical')),
                'backup_enabled': bool(data.get('backup_enabled')),
                'restart_time': data.get('restart_time', ''),
                'cpu': '—',
                'ram': '—',
                'ports': '—',
                'uptime': '—'
            }
            
            if running:
                pid_file = os.path.join(data['path'], 'server.pid')
                try:
                    with open(pid_file, 'r') as f:
                        pid = int(f.read().strip())
                    res = get_node_resources(pid)
                    node_info['cpu'] = res['cpu']
                    node_info['ram'] = res['ram']
                    node_info['ports'] = get_node_ports(pid)
                except Exception:
                    pass
                node_info['uptime'] = format_uptime(get_current_uptime(name))
            else:
                total_up = data.get('total_uptime', 0) or 0
                if total_up > 0:
                    node_info['uptime'] = format_uptime(total_up)
            
            result.append(node_info)
        return {'nodes': result}
    except Exception as e:
        return {'error': str(e)}

def api_start(node_name):
    try:
        from lserver.core import start_node
        start_node(node_name)
        return {'status': 'ok', 'message': f"Nodo '{node_name}' arrancado."}
    except SystemExit:
        return {'error': f"No se pudo arrancar '{node_name}'."}
    except Exception as e:
        return {'error': str(e)}

def api_stop(node_name):
    try:
        from lserver.core import stop_node
        stop_node(node_name)
        return {'status': 'ok', 'message': f"Nodo '{node_name}' detenido."}
    except SystemExit:
        return {'error': f"No se pudo detener '{node_name}'."}
    except Exception as e:
        return {'error': str(e)}

def api_kill(node_name):
    try:
        from lserver.core import kill_node
        kill_node(node_name)
        return {'status': 'ok', 'message': f"Nodo '{node_name}' eliminado."}
    except SystemExit:
        return {'error': f"No se pudo matar '{node_name}'."}
    except Exception as e:
        return {'error': str(e)}

def api_logs(node_name):
    try:
        from lserver.state import get_node
        node = get_node(node_name)
        if not node:
            return {'error': f"Nodo '{node_name}' no existe."}
        
        log_file = os.path.join(node['path'], 'server.log')
        if not os.path.exists(log_file):
            return {'logs': '(Sin logs disponibles)'}
        
        with open(log_file, 'r', errors='replace') as f:
            lines = f.readlines()
        
        # Retornar las ultimas 200 lineas
        last_lines = lines[-200:] if len(lines) > 200 else lines
        return {'logs': ''.join(last_lines)}
    except Exception as e:
        return {'error': str(e)}

def api_send_command(node_name, command):
    try:
        from lserver.state import get_node
        from lserver.core import is_running
        node = get_node(node_name)
        if not node:
            return {'error': f"Nodo '{node_name}' no existe."}
        if not is_running(node_name):
            return {'error': f"Nodo '{node_name}' no está encendido."}
        
        fifo_path = os.path.join(node['path'], 'server.stdin')
        if not os.path.exists(fifo_path):
            return {'error': "El canal de entrada (FIFO) no existe."}
            
        with open(fifo_path, 'w') as f:
            f.write(command + '\n')
            
        return {'status': 'ok'}
    except Exception as e:
        return {'error': str(e)}

def api_groups():
    try:
        from lserver.groups import list_groups
        from lserver.core import is_running
        groups_data = list_groups()
        result = []
        for gname, nodes in groups_data.items():
            active = sum(1 for n in nodes if is_running(n))
            result.append({
                'name': gname,
                'nodes': nodes,
                'active': active,
                'total': len(nodes)
            })
        return {'groups': result}
    except Exception as e:
        return {'error': str(e)}

def api_group_start(group_name):
    try:
        from lserver.groups import start_group
        start_group(group_name)
        return {'status': 'ok', 'message': f"Grupo '{group_name}' arrancado."}
    except Exception as e:
        return {'error': str(e)}

def api_group_stop(group_name):
    try:
        from lserver.groups import stop_group
        stop_group(group_name)
        return {'status': 'ok', 'message': f"Grupo '{group_name}' detenido."}
    except Exception as e:
        return {'error': str(e)}

def api_get_startsh(node_name):
    """Retorna el contenido del start.sh de un nodo."""
    try:
        from lserver.state import get_node
        node = get_node(node_name)
        if not node:
            return {'error': f"Nodo '{node_name}' no existe."}
        path = os.path.join(node['path'], 'start.sh')
        if not os.path.exists(path):
            return {'error': 'start.sh no encontrado.'}
        with open(path, 'r', errors='replace') as f:
            content = f.read()
        return {'content': content}
    except Exception as e:
        return {'error': str(e)}

def api_save_startsh(node_name, content):
    """Guarda el contenido del start.sh de un nodo."""
    try:
        from lserver.state import get_node
        node = get_node(node_name)
        if not node:
            return {'error': f"Nodo '{node_name}' no existe."}
        path = os.path.join(node['path'], 'start.sh')
        with open(path, 'w') as f:
            f.write(content)
        os.chmod(path, 0o755)
        return {'status': 'ok'}
    except Exception as e:
        return {'error': str(e)}

def api_restart(node_name):
    """Detiene y vuelve a arrancar un nodo."""
    try:
        from lserver.core import stop_node, start_node, is_running
        import time
        if is_running(node_name):
            stop_node(node_name)
            time.sleep(1.5)
        start_node(node_name)
        return {'status': 'ok', 'message': f"Nodo '{node_name}' reiniciado."}
    except SystemExit:
        return {'error': f"No se pudo reiniciar '{node_name}'."}
    except Exception as e:
        return {'error': str(e)}

def api_templates():
    """Retorna las plantillas disponibles y categorías del menú."""
    try:
        from lserver.templates import MENU, TEMPLATES
        templates_info = []
        for key, val in TEMPLATES.items():
            templates_info.append({
                'key': key,
                'description': val.get('description', key)
            })
        return {'menu': MENU, 'templates': templates_info}
    except Exception as e:
        return {'error': str(e)}

def api_create_node(name, template=None):
    """Crea un nuevo nodo desde la interfaz web."""
    try:
        from lserver.core import validate_node_name
        from lserver.state import get_node, add_node
        validate_node_name(name)
        if get_node(name):
            return {'error': f"El nodo '{name}' ya existe."}
        
        current_dir = os.getcwd()
        node_path = os.path.join(current_dir, name)
        os.makedirs(node_path, exist_ok=True)
        
        start_script = os.path.join(node_path, "start.sh")
        if not os.path.exists(start_script):
            from lserver.templates import get_template
            content = get_template(template) if template else None
            if not content:
                content = (
                    "#!/bin/bash\n"
                    "# Fue creado con mucho amor por SrxMateo & LumaxStudio\n"
                    f"echo 'Iniciando LServer Nodo: {name}'\n"
                    "while true; do sleep 1000; done\n"
                )
            with open(start_script, "w") as f:
                f.write(content)
            os.chmod(start_script, 0o755)
            
        add_node(name, node_path, "./start.sh")
        return {'status': 'ok', 'message': f"Servidor '{name}' creado exitosamente."}
    except Exception as e:
        return {'error': str(e)}

def api_delete_node(name, delete_files=False):
    """Elimina un nodo (y opcionalmente sus archivos físicos)."""
    try:
        from lserver.core import stop_node, is_running
        from lserver.state import get_node, remove_node
        node = get_node(name)
        if not node:
            return {'error': f"El nodo '{name}' no existe."}
        if is_running(name):
            stop_node(name)
        if delete_files:
            path = node.get('path')
            if path and os.path.exists(path):
                shutil.rmtree(path, ignore_errors=True)
        remove_node(name)
        return {'status': 'ok', 'message': f"Servidor '{name}' eliminado."}
    except Exception as e:
        return {'error': str(e)}

def _safe_node_path(node_name, subpath=''):
    """Valida y resuelve una ruta dentro del directorio de un nodo para evitar path traversal."""
    from lserver.state import get_node
    node = get_node(node_name)
    if not node:
        raise ValueError(f"Nodo '{node_name}' no existe.")
    base = os.path.realpath(node['path'])
    cleaned = (subpath or '').lstrip('/').replace('\\', '/')
    target = os.path.realpath(os.path.join(base, cleaned))
    if target != base and not target.startswith(base + os.sep):
        raise ValueError("Acceso denegado: ruta fuera del directorio del nodo.")
    return base, target

def api_list_files(node_name, subpath=''):
    """Lista archivos y subcarpetas dentro del nodo."""
    try:
        base, target = _safe_node_path(node_name, subpath)
        if not os.path.exists(target):
            return {'error': 'Directorio no encontrado.'}
        if not os.path.isdir(target):
            return {'error': 'La ruta solicitada no es un directorio.'}
        
        entries = []
        for item in os.scandir(target):
            try:
                st = item.stat()
                entries.append({
                    'name': item.name,
                    'is_dir': item.is_dir(),
                    'size': st.st_size if not item.is_dir() else 0,
                    'mtime': int(st.st_mtime)
                })
            except Exception:
                pass
        
        entries.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
        rel_path = os.path.relpath(target, base)
        if rel_path == '.':
            rel_path = ''
        return {
            'status': 'ok',
            'current_path': rel_path,
            'files': entries
        }
    except Exception as e:
        return {'error': str(e)}

def api_read_file(node_name, subpath):
    """Lee el contenido de un archivo de texto dentro del nodo."""
    try:
        base, target = _safe_node_path(node_name, subpath)
        if not os.path.exists(target):
            return {'error': 'Archivo no encontrado.'}
        if os.path.isdir(target):
            return {'error': 'La ruta es un directorio, no un archivo.'}
        if os.path.getsize(target) > 5 * 1024 * 1024:
            return {'error': 'Archivo demasiado grande para el editor web (máx 5MB).'}
        with open(target, 'r', errors='replace') as f:
            content = f.read()
        return {'status': 'ok', 'content': content, 'path': subpath}
    except Exception as e:
        return {'error': str(e)}

def api_write_file(node_name, subpath, content):
    """Guarda el contenido de un archivo dentro del nodo."""
    try:
        base, target = _safe_node_path(node_name, subpath)
        if os.path.isdir(target):
            return {'error': 'No se puede sobreescribir un directorio.'}
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, 'w') as f:
            f.write(content)
        return {'status': 'ok'}
    except Exception as e:
        return {'error': str(e)}

def api_create_file(node_name, subpath, is_dir=False):
    """Crea un archivo vacío o una carpeta en la ruta especificada."""
    try:
        base, target = _safe_node_path(node_name, subpath)
        if os.path.exists(target):
            return {'error': 'Ya existe un archivo o carpeta con ese nombre.'}
        if is_dir:
            os.makedirs(target, exist_ok=True)
        else:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, 'w') as f:
                f.write('')
        return {'status': 'ok'}
    except Exception as e:
        return {'error': str(e)}

def api_delete_file(node_name, subpath):
    """Elimina un archivo o directorio dentro del nodo."""
    try:
        base, target = _safe_node_path(node_name, subpath)
        if target == base:
            return {'error': 'No se puede eliminar la raíz del nodo desde aquí.'}
        if not os.path.exists(target):
            return {'error': 'El archivo o carpeta no existe.'}
        if os.path.isdir(target):
            shutil.rmtree(target)
        else:
            os.remove(target)
        return {'status': 'ok'}
    except Exception as e:
        return {'error': str(e)}

def api_upload_file(node_name, subpath, filename, content_b64):
    """Recibe un archivo en Base64 (drag & drop o selector) y lo escribe en disco."""
    try:
        base, target_dir = _safe_node_path(node_name, subpath)
        if not os.path.isdir(target_dir):
            return {'error': 'La carpeta de destino no es un directorio válido.'}
        safe_fname = os.path.basename(filename.replace('\\', '/'))
        if not safe_fname or safe_fname in ['.', '..']:
            return {'error': 'Nombre de archivo inválido.'}
        target_file = os.path.join(target_dir, safe_fname)
        raw_data = base64.b64decode(content_b64)
        with open(target_file, 'wb') as f:
            f.write(raw_data)
        return {'status': 'ok', 'filename': safe_fname}
    except Exception as e:
        return {'error': str(e)}

def api_users():
    """Retorna la lista de usuarios del panel web."""
    try:
        from lserver.web.auth import list_users
        return {'users': list_users()}
    except Exception as e:
        return {'error': str(e)}

def api_add_user(username, password):
    """Crea o actualiza una cuenta de usuario."""
    try:
        from lserver.web.auth import add_user
        add_user(username, password)
        return {'status': 'ok', 'message': f"Usuario '{username}' guardado exitosamente."}
    except Exception as e:
        return {'error': str(e)}

def api_delete_user(username):
    """Elimina una cuenta de usuario."""
    try:
        from lserver.web.auth import delete_user
        delete_user(username)
        return {'status': 'ok', 'message': f"Usuario '{username}' eliminado."}
    except Exception as e:
        return {'error': str(e)}
