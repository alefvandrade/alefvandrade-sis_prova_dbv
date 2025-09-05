import os
import configparser
import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = os.path.join("config.ini")

        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        if "BD" not in self.config:
            raise ValueError("Arquivo config.ini não possui seção [BD]")

        self.host = self.config["BD"].get("host", "localhost")
        self.user = self.config["BD"].get("user", "root")
        self.password = self.config["BD"].get("password", "")
        self.dbname = self.config["BD"].get("dbname", "")
        self.conn = None

    def __enter__(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.dbname
            )
            return self.conn
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()

    # Métodos auxiliares
    def execute(self, query, params=None):
        with self as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(query, params or ())
            conn.commit()
            return cur

    def fetch_all(self, query, params=None):
        with self as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(query, params or ())
            return cur.fetchall()

    def fetch_one(self, query, params=None):
        with self as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(query, params or ())
            return cur.fetchone()


# Teste rápido
if __name__ == "__main__":
    db = DatabaseConnection()
    try:
        with db as conn:
            print("Conexão bem-sucedida!")
    except Exception as e:
        print("Falha:", e)
