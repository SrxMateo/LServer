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
