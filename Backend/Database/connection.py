# Backend/Database/connection.py
import sqlite3
import os

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
        
def apply_migration():
    # Caminho absoluto para o banco de dados
    db_path = "e:\\vs\\alefvandrade-sis_prova_dbv\\Backend\\Data\\sis_prova_dbv.sqlite"
    migrations_path = os.path.join(os.path.dirname(__file__), "migrations.sql")
    
    print(f"Tentando abrir banco de dados: {db_path}")  # Depuração
    print(f"Tentando abrir migrations.sql: {migrations_path}")  # Depuração

    try:
        with open(migrations_path, "r") as f:
            sql_content = f.read()
            print(f"Conteúdo do migrations.sql: {sql_content}")  # Depuração
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA foreign_keys = ON;")  # Ativa chaves estrangeiras, se aplicável
                cursor.executescript(sql_content)
                conn.commit()
                # Verificar a estrutura após a migração
                cursor.execute("PRAGMA table_info(provas);")
                print("Estrutura da tabela provas:", cursor.fetchall())
                print("Migração aplicada com sucesso!")
    except FileNotFoundError as e:
        print(f"Erro: Arquivo migrations.sql ou banco de dados não encontrado: {e}")
    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    apply_migration()