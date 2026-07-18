from lserver.db import DBConnection

db = DBConnection()

def load_nodes():
    rows = db.fetchall('SELECT * FROM nodes')
    return {row['name']: dict(row) for row in rows}

def add_node(name, path, start_cmd):
    db.execute('''
        INSERT OR REPLACE INTO nodes (name, path, start_cmd, is_critical, backup_enabled) 
        VALUES (?, ?, ?,
            COALESCE((SELECT is_critical FROM nodes WHERE name=?), 0),
            COALESCE((SELECT backup_enabled FROM nodes WHERE name=?), 0)
        )
    ''', (name, path, start_cmd, name, name))

def get_node(name):
    row = db.fetchone('SELECT * FROM nodes WHERE name = ?', (name,))
    if row:
        return dict(row)
    return None

def remove_node(name):
    db.execute('DELETE FROM nodes WHERE name = ?', (name,))

def list_nodes():
    return load_nodes()

def set_node_critical(name, is_critical):
    db.execute('UPDATE nodes SET is_critical = ? WHERE name = ?', (int(is_critical), name))

def set_node_backup(name, backup_enabled):
    db.execute('UPDATE nodes SET backup_enabled = ? WHERE name = ?', (int(backup_enabled), name))

# --- v3: Uptime ---
def set_node_last_start(name, timestamp):
    db.execute('UPDATE nodes SET last_start = ? WHERE name = ?', (timestamp, name))

def add_node_uptime(name, seconds):
    db.execute('UPDATE nodes SET total_uptime = total_uptime + ? WHERE name = ?', (seconds, name))

# --- v3: Reinicios programados ---
def set_node_restart_time(name, time_str):
    db.execute('UPDATE nodes SET restart_time = ? WHERE name = ?', (time_str, name))

# --- v3: Settings genéricos ---
def set_setting(key, value):
    db.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, value))

def get_setting(key):
    row = db.fetchone('SELECT value FROM settings WHERE key = ?', (key,))
    if row:
        return row['value']
    return None

def remove_setting(key):
    db.execute('DELETE FROM settings WHERE key = ?', (key,))
