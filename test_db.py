import sqlite3

# Caminho para o banco
db_path = "data/db.sqlite"

# Caminho para o script SQL
sql_path = "backend/database/migrations.sql"

# Conecta/cria o banco
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Lê o SQL
with open(sql_path, 'r', encoding='utf-8') as f:
    sql_script = f.read()

# Executa o script
try:
    cursor.executescript(sql_script)
    conn.commit()
    print("Tabelas criadas com sucesso!")
except Exception as e:
    print("Erro ao criar tabelas:", e)

# Lista as tabelas existentes
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tabelas no banco:", tables)

conn.close()
