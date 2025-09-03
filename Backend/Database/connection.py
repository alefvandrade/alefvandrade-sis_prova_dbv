# Backend/Database/connection.py
import sqlite3

class DatabaseConnection:
    def __init__(self, db_path="Data/sis_prova_dbv.sqlite"):
        self.db_path = db_path
        self.conn = None

    # Context manager
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # retorna linhas como dict
        return self.conn  # retorna a conexão, não o cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()

    # Métodos auxiliares opcionais
    def execute(self, query, params=()):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(query, params)
            conn.commit()
            return cur

    def fetch_all(self, query, params=()):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(query, params)
            return cur.fetchall()

    def fetch_one(self, query, params=()):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(query, params)
            return cur.fetchone()
