"""API REST para el panel web de LServer."""
import os

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
