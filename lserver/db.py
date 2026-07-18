import sqlite3
import os
import threading

class DBConnection:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DBConnection, cls).__new__(cls)
                cls._instance._init_db()
            return cls._instance
            
    def _init_db(self):
        self.db_path = os.path.expanduser("~/.lserver.db")
        # Permitimos multithreading seguro (necesario para el daemon en bg y cli en fg)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
        
    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nodes (
                name TEXT PRIMARY KEY,
                path TEXT NOT NULL,
                start_cmd TEXT DEFAULT './start.sh',
                is_critical BOOLEAN DEFAULT 0,
                backup_enabled BOOLEAN DEFAULT 0,
                last_start REAL DEFAULT 0,
                total_uptime REAL DEFAULT 0,
                restart_time TEXT DEFAULT '',
                node_group TEXT DEFAULT ''
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups_nodes (
                group_name TEXT,
                node_name TEXT,
                PRIMARY KEY(group_name, node_name)
            )
        ''')
        self.conn.commit()
        
        # Migrar columnas nuevas si la tabla ya existía sin ellas
        self._migrate_columns(cursor)
    
    def _migrate_columns(self, cursor):
        """Añade columnas nuevas a tablas existentes sin romper datos."""
        existing = {row[1] for row in cursor.execute("PRAGMA table_info(nodes)").fetchall()}
        migrations = {
            'last_start': 'REAL DEFAULT 0',
            'total_uptime': 'REAL DEFAULT 0',
            'restart_time': "TEXT DEFAULT ''",
            'node_group': "TEXT DEFAULT ''"
        }
        for col, col_type in migrations.items():
            if col not in existing:
                cursor.execute(f"ALTER TABLE nodes ADD COLUMN {col} {col_type}")
        self.conn.commit()
        
    def execute(self, query, params=()):
        with self._lock:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            return cursor
            
    def fetchone(self, query, params=()):
        with self._lock:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
            
    def fetchall(self, query, params=()):
        with self._lock:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
