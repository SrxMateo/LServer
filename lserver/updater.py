"""Auto-actualizacion de LServer desde GitHub."""
import subprocess
import re
import os
from lserver import __version__
from lserver.ui import log_success, log_info, log_error, error_exit

REPO_URL = "https://github.com/SrxMateo/LServer.git"
RAW_VERSION_URL = "https://raw.githubusercontent.com/SrxMateo/LServer/main/lserver/__init__.py"

def _get_remote_version():
    """Obtiene la version remota desde GitHub usando urllib."""
    try:
        import urllib.request
        req = urllib.request.Request(RAW_VERSION_URL, headers={'User-Agent': 'LServer-Updater'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode('utf-8')
            match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                return match.group(1)
    except Exception:
        return None
    return None

def check_update():
    """Compara la version local vs la remota."""
    log_info(f"Version local: v{__version__}")
    log_info("Comprobando actualizaciones...")
    
    remote = _get_remote_version()
    if remote is None:
        log_error("No se pudo conectar con GitHub para comprobar actualizaciones.")
        return
    
    log_info(f"Version remota: v{remote}")
    
    if remote != __version__:
        log_info(f"Hay una nueva version disponible: v{remote}")
        ans = input("Deseas actualizar ahora? (s/N): ")
        if ans.lower() == 's':
            run_update()
        else:
            log_info("Actualizacion cancelada.")
    else:
        log_success("LServer esta actualizado. No hay nuevas versiones.")

def run_update():
    """Ejecuta la actualizacion descargando y reinstalando."""
    log_info("Descargando la ultima version...")
    
    # Encontrar el directorio de instalacion
    install_dir = _find_install_dir()
    if not install_dir:
        error_exit("No se pudo encontrar el directorio de instalacion de LServer.")
    
    try:
        subprocess.run(["git", "pull"], cwd=install_dir, check=True, 
                       capture_output=True, text=True)
        log_success("Codigo fuente actualizado.")
    except subprocess.CalledProcessError as e:
        error_exit(f"Error al descargar actualizacion: {e.stderr}")
    
    log_info("Reinstalando LServer...")
    try:
        env = os.environ.copy()
        env['PIP_BREAK_SYSTEM_PACKAGES'] = '1'
        subprocess.run(["pip3", "install", ".", "--break-system-packages"],
                       cwd=install_dir, check=True, capture_output=True, 
                       text=True, env=env)
        log_success("LServer actualizado correctamente. Reinicia tu terminal para usar la nueva version.")
    except subprocess.CalledProcessError:
        # Fallback sin --break-system-packages
        try:
            subprocess.run(["pip3", "install", "."], cwd=install_dir, 
                           check=True, capture_output=True, text=True)
            log_success("LServer actualizado correctamente.")
        except subprocess.CalledProcessError as e:
            error_exit(f"Error al instalar la actualizacion: {e.stderr}")

def _find_install_dir():
    """Busca el directorio donde esta instalado LServer."""
    # Opcion 1: directorio actual si tiene pyproject.toml
    cwd = os.getcwd()
    if os.path.exists(os.path.join(cwd, "pyproject.toml")):
        return cwd
    
    # Opcion 2: buscar en rutas comunes
    common_paths = [
        os.path.expanduser("~/LServer"),
        "/opt/LServer",
        "/tmp/LServer",
    ]
    for path in common_paths:
        if os.path.exists(os.path.join(path, "pyproject.toml")):
            return path
    
    # Opcion 3: encontrar via pip
    try:
        result = subprocess.run(["pip3", "show", "lserver"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if line.startswith("Location:"):
                loc = line.split(":", 1)[1].strip()
                parent = os.path.dirname(loc)
                if os.path.exists(os.path.join(parent, "pyproject.toml")):
                    return parent
    except Exception:
        pass
    
    return None
