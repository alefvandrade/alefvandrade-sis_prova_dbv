from Backend.Database.connection import DatabaseConnection

class Usuario:
    def __init__(self, nome=None, email=None, senha_hash=None, usuario_id=None):
        self.id = usuario_id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.db = DatabaseConnection()

    # ------------------ CREATE ------------------
    def cadastrar(self):
        sql = "INSERT INTO usuarios (nome, email, senha_hash) VALUES (?, ?, ?)"
        cur = self.db.executar(sql, (self.nome, self.email, self.senha_hash))
        if cur:
            self.id = cur.lastrowid
            return True
        return False

    # ------------------ READ ------------------
    def buscar_por_id(self, usuario_id):
        sql = "SELECT id, nome, email, senha_hash FROM usuarios WHERE id = ?"
        result = self.db.consultar(sql, (usuario_id,))
        if result:
            self.id, self.nome, self.email, self.senha_hash = result[0]
            return self
        return None

    def listar_todos(self):
        sql = "SELECT id, nome, email FROM usuarios"
        return self.db.consultar(sql)

    # ------------------ UPDATE ------------------
    def atualizar(self):
        if not self.id:
            return False
        sql = "UPDATE usuarios SET nome = ?, email = ?, senha_hash = ? WHERE id = ?"
        cur = self.db.executar(sql, (self.nome, self.email, self.senha_hash, self.id))
        return bool(cur)

    # ------------------ DELETE ------------------
    def excluir(self):
        if not self.id:
            return False
        sql = "DELETE FROM usuarios WHERE id = ?"
        cur = self.db.executar(sql, (self.id,))
        return bool(cur)
