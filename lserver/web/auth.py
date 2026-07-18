"""Autenticacion para el panel web de LServer."""
import hashlib
from lserver.state import set_setting, get_setting

def set_password(username, password):
    """Guarda credenciales con hash SHA-256."""
    pass_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    set_setting('web_user', username)
    set_setting('web_pass_hash', pass_hash)

def verify_credentials(username, password):
    """Verifica credenciales comparando hash SHA-256."""
    stored_user = get_setting('web_user')
    stored_hash = get_setting('web_pass_hash')
    if not stored_user or not stored_hash:
        return False
    pass_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return username == stored_user and pass_hash == stored_hash

def get_credentials():
    """Retorna (username, pass_hash) o (None, None)."""
    user = get_setting('web_user')
    pass_hash = get_setting('web_pass_hash')
    return (user, pass_hash)

def has_credentials():
    """Retorna True si hay credenciales configuradas."""
    user, ph = get_credentials()
    return user is not None and ph is not None
