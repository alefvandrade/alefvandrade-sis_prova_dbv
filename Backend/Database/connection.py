import sqlite3
from sqlite3 import Error

class DatabaseConnection:
    def __init__(self, db_file="sis_prova_dbv.sqlite"):
        self.db_file = db_file
        self.conn = None

    def conectar(self):
        """Cria uma conexão com o banco de dados SQLite."""
        try:
            self.conn = sqlite3.connect(self.db_file)
            print(f"Conectado ao banco de dados: {self.db_file}")
            return self.conn
        except Error as e:
            print(f"Erro ao conectar ao banco: {e}")
            return None

    def fechar(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn:
            self.conn.close()
            print("Conexão com o banco fechada.")

    def executar(self, sql, params=()):
        """Executa um comando SQL (INSERT, UPDATE, DELETE)."""
        if not self.conn:
            self.conectar()
        try:
            cur = self.conn.cursor()
            cur.execute(sql, params)
            self.conn.commit()
            return cur
        except Error as e:
            print(f"Erro ao executar SQL: {e}")
            return None

    def consultar(self, sql, params=()):
        """Executa uma consulta SQL (SELECT) e retorna os resultados."""
        if not self.conn:
            self.conectar()
        try:
            cur = self.conn.cursor()
            cur.execute(sql, params)
            return cur.fetchall()
        except Error as e:
            print(f"Erro ao consultar SQL: {e}")
            return None
