"""Servidor HTTP del panel web de LServer."""
import os
import json
import base64
import subprocess
import signal
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from lserver.web.auth import verify_credentials, has_credentials
from lserver.web import api
from lserver.ui import log_success, log_info, log_error, error_exit

WEB_PID_FILE = os.path.expanduser("~/.lserver_web.pid")
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

class LServerHandler(BaseHTTPRequestHandler):
    """Handler HTTP con autenticacion y rutas API."""
    
    def log_message(self, format, *args):
        """Silenciar logs del servidor HTTP."""
        pass
    
    def _check_auth(self):
        """Verifica HTTP Basic Auth. Retorna True si OK."""
        if not has_credentials():
            return True  # Si no hay password, acceso libre
        
        auth_header = self.headers.get('Authorization', '')
        if not auth_header.startswith('Basic '):
            self._send_auth_required()
            return False
        
        try:
            decoded = base64.b64decode(auth_header[6:]).decode('utf-8')
            username, password = decoded.split(':', 1)
            if verify_credentials(username, password):
                return True
        except Exception:
            pass
        
        self._send_auth_required()
        return False
    
    def _send_auth_required(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="LServer Panel"')
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<h1>401 - No autorizado</h1><p>Credenciales invalidas.</p>')
    
    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)
    
    def _send_file(self, filepath, content_type):
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')
    
    def do_GET(self):
        if not self._check_auth():
            return
        
        parsed = urllib.parse.urlsplit(self.path)
        path = parsed.path.rstrip('/')
        query = urllib.parse.parse_qs(parsed.query)
        
        if path == '' or path == '/':
            self._send_file(os.path.join(STATIC_DIR, 'index.html'), 'text/html; charset=utf-8')
        elif path == '/api/nodes':
            self._send_json(api.api_nodes())
        elif path == '/api/groups':
            self._send_json(api.api_groups())
        elif path == '/api/templates':
            self._send_json(api.api_templates())
        elif path.startswith('/api/logs/'):
            node_name = path.split('/api/logs/', 1)[1]
            self._send_json(api.api_logs(node_name))
        elif path.startswith('/api/startsh/'):
            node_name = path.split('/api/startsh/', 1)[1]
            self._send_json(api.api_get_startsh(node_name))
        elif path.startswith('/api/files/list/'):
            node_name = path.split('/api/files/list/', 1)[1]
            subpath = query.get('path', [''])[0]
            self._send_json(api.api_list_files(node_name, subpath))
        elif path.startswith('/api/files/read/'):
            node_name = path.split('/api/files/read/', 1)[1]
            subpath = query.get('path', [''])[0]
            self._send_json(api.api_read_file(node_name, subpath))
        else:
            # Servir archivos estaticos
            safe_path = path.lstrip('/')
            filepath = os.path.join(STATIC_DIR, safe_path)
            if os.path.exists(filepath) and os.path.isfile(filepath):
                ct = 'text/html'
                if filepath.endswith('.css'): ct = 'text/css'
                elif filepath.endswith('.js'): ct = 'application/javascript'
                elif filepath.endswith('.png'): ct = 'image/png'
                elif filepath.endswith('.svg'): ct = 'image/svg+xml'
                self._send_file(filepath, ct)
            else:
                self.send_response(404)
                self.end_headers()
    
    def do_POST(self):
        if not self._check_auth():
            return
        
        parsed = urllib.parse.urlsplit(self.path)
        path = parsed.path.rstrip('/')
        content_length = int(self.headers.get('Content-Length', 0))
        body_data = {}
        if content_length > 0:
            try:
                body_data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            except Exception:
                body_data = {}
        
        if path == '/api/node/create':
            name = body_data.get('name', '')
            template = body_data.get('template', None)
            self._send_json(api.api_create_node(name, template))
        elif path.startswith('/api/node/delete/'):
            node_name = path.split('/api/node/delete/', 1)[1]
            delete_files = bool(body_data.get('delete_files', False))
            self._send_json(api.api_delete_node(node_name, delete_files))
        elif path.startswith('/api/start/'):
            node_name = path.split('/api/start/', 1)[1]
            self._send_json(api.api_start(node_name))
        elif path.startswith('/api/stop/'):
            node_name = path.split('/api/stop/', 1)[1]
            self._send_json(api.api_stop(node_name))
        elif path.startswith('/api/kill/'):
            node_name = path.split('/api/kill/', 1)[1]
            self._send_json(api.api_kill(node_name))
        elif path.startswith('/api/restart/'):
            node_name = path.split('/api/restart/', 1)[1]
            self._send_json(api.api_restart(node_name))
        elif path.startswith('/api/startsh/'):
            node_name = path.split('/api/startsh/', 1)[1]
            self._send_json(api.api_save_startsh(node_name, body_data.get('content', '')))
        elif path.startswith('/api/files/write/'):
            node_name = path.split('/api/files/write/', 1)[1]
            self._send_json(api.api_write_file(node_name, body_data.get('path', ''), body_data.get('content', '')))
        elif path.startswith('/api/files/create/'):
            node_name = path.split('/api/files/create/', 1)[1]
            self._send_json(api.api_create_file(node_name, body_data.get('path', ''), body_data.get('is_dir', False)))
        elif path.startswith('/api/files/delete/'):
            node_name = path.split('/api/files/delete/', 1)[1]
            self._send_json(api.api_delete_file(node_name, body_data.get('path', '')))
        elif path.startswith('/api/files/upload/'):
            node_name = path.split('/api/files/upload/', 1)[1]
            self._send_json(api.api_upload_file(node_name, body_data.get('path', ''), body_data.get('filename', ''), body_data.get('content_b64', '')))
        elif path.startswith('/api/group/start/'):
            gname = path.split('/api/group/start/', 1)[1]
            self._send_json(api.api_group_start(gname))
        elif path.startswith('/api/group/stop/'):
            gname = path.split('/api/group/stop/', 1)[1]
            self._send_json(api.api_group_stop(gname))
        elif path.startswith('/api/command/'):
            node_name = path.split('/api/command/', 1)[1]
            self._send_json(api.api_send_command(node_name, body_data.get('command', '')))
        else:
            self._send_json({'error': 'Ruta no encontrada'}, 404)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Authorization, Content-Type')
        self.end_headers()

def start_web_server(port=9090):
    """Inicia el servidor web en segundo plano."""
    if os.path.exists(WEB_PID_FILE):
        with open(WEB_PID_FILE, 'r') as f:
            try:
                pid = int(f.read().strip())
                os.kill(pid, 0)
                log_info(f"El panel web ya esta corriendo (PID: {pid}).")
                return
            except (ValueError, OSError):
                pass
    
    import subprocess
    log_file = os.path.expanduser("~/.lserver_web.log")
    f_log = open(log_file, "a")
    
    process = subprocess.Popen(
        ["lserver", "--run-web", str(port)],
        stdout=f_log, stderr=subprocess.STDOUT,
        start_new_session=True
    )
    
    with open(WEB_PID_FILE, "w") as f:
        f.write(str(process.pid))
    
    log_success(f"Panel web iniciado en http://0.0.0.0:{port}")
    if not has_credentials():
        log_info("Configura una contrasena con: lserver web password")

def stop_web_server():
    """Detiene el servidor web."""
    if os.path.exists(WEB_PID_FILE):
        with open(WEB_PID_FILE, 'r') as f:
            try:
                pid = int(f.read().strip())
                os.killpg(pid, signal.SIGTERM)
                log_success("Panel web detenido.")
            except (ValueError, OSError):
                log_info("Panel web no estaba corriendo.")
        os.remove(WEB_PID_FILE)
    else:
        log_info("Panel web no esta corriendo.")

def run_web_server(port=9090):
    """Ejecuta el servidor HTTP (bloqueante, para uso interno)."""
    server = HTTPServer(('0.0.0.0', port), LServerHandler)
    log_info(f"Panel web escuchando en puerto {port}...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
