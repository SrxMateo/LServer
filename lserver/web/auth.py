"""Autenticación multi-usuario para el panel web de LServer."""
import hashlib
import time
from lserver.db import DBConnection
from lserver.state import get_setting

db = DBConnection()

# Tabla de usuarios del panel web
db.execute('''CREATE TABLE IF NOT EXISTS web_users (
    username TEXT PRIMARY KEY,
    password_hash TEXT NOT NULL,
    created_at INTEGER
)''')

def _migrate_legacy_settings():
    """Migra el usuario antiguo guardado en settings a la nueva tabla web_users."""
    try:
        legacy_user = get_setting('web_user')
        legacy_hash = get_setting('web_pass_hash')
        if legacy_user and legacy_hash:
            db.execute('''INSERT OR IGNORE INTO web_users (username, password_hash, created_at)
                          VALUES (?, ?, ?)''', (legacy_user, legacy_hash, int(time.time())))
    except Exception:
        pass

_migrate_legacy_settings()

def _hash_pw(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def add_user(username, password):
    """Crea o actualiza un usuario con contraseña."""
    username = username.strip()
    if not username:
        raise ValueError("El nombre de usuario no puede estar vacío.")
    if len(password) < 4:
        raise ValueError("La contraseña debe tener al menos 4 caracteres.")
    pass_hash = _hash_pw(password)
    now = int(time.time())
    db.execute('''INSERT INTO web_users (username, password_hash, created_at)
                  VALUES (?, ?, ?)
                  ON CONFLICT(username) DO UPDATE SET password_hash=excluded.password_hash''',
               (username, pass_hash, now))
    return True

def delete_user(username):
    """Elimina un usuario del panel web."""
    username = username.strip()
    row = db.fetchone('SELECT username FROM web_users WHERE username = ?', (username,))
    if not row:
        raise ValueError(f"El usuario '{username}' no existe.")
    db.execute('DELETE FROM web_users WHERE username = ?', (username,))
    return True

def list_users():
    """Retorna la lista de usuarios registrados (sin contraseñas)."""
    rows = db.fetchall('SELECT username, created_at FROM web_users ORDER BY username ASC')
    return [{'username': r['username'], 'created_at': r['created_at']} for r in rows]

def verify_credentials(username, password):
    """Verifica si las credenciales de acceso coinciden con algún usuario activo."""
    if not has_credentials():
        return True  # Si no hay usuarios creados, acceso sin bloqueo
    username = (username or '').strip()
    pass_hash = _hash_pw(password or '')
    row = db.fetchone('SELECT username FROM web_users WHERE username = ? AND password_hash = ?',
                      (username, pass_hash))
    return bool(row)

def has_credentials():
    """Retorna True si hay al menos un usuario configurado."""
    row = db.fetchone('SELECT COUNT(*) as count FROM web_users')
    return bool(row and row['count'] > 0)

# Aliases de compatibilidad previa
def set_password(username, password):
    return add_user(username, password)

def get_credentials():
    rows = list_users()
    if rows:
        return (rows[0]['username'], 'configured')
    return (None, None)
