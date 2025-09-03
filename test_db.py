import sqlite3

# Caminho pro banco
db_path = r"data/db.sqlite"

# Conectar (vai criar se não existir)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Listar tabelas existentes
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tabelas no banco:", tables)

# Fechar conexão
conn.close()
