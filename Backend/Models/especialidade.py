from Backend.Database.connection import DatabaseConnection

class Especialidade:
    def __init__(self, codigo=None, nome=None, especialidade_id=None):
        self.id = especialidade_id
        self.codigo = codigo
        self.nome = nome
        self.db = DatabaseConnection()

    # ------------------ CREATE ------------------
    def cadastrar(self):
        sql = "INSERT INTO especialidades (codigo, nome) VALUES (?, ?)"
        cur = self.db.executar(sql, (self.codigo, self.nome))
        if cur:
            self.id = cur.lastrowid
            return True
        return False

    # ------------------ READ ------------------
    def buscar_por_id(self, especialidade_id):
        sql = "SELECT id, codigo, nome FROM especialidades WHERE id = ?"
        result = self.db.consultar(sql, (especialidade_id,))
        if result:
            self.id, self.codigo, self.nome = result[0]
            return self
        return None

    def buscar_por_codigo(self, codigo):
        sql = "SELECT id, codigo, nome FROM especialidades WHERE codigo = ?"
        result = self.db.consultar(sql, (codigo,))
        if result:
            self.id, self.codigo, self.nome = result[0]
            return self
        return None

    def listar_todos(self):
        sql = "SELECT id, codigo, nome FROM especialidades ORDER BY nome"
        return self.db.consultar(sql)

    # ------------------ UPDATE ------------------
    def atualizar(self):
        if not self.id:
            return False
        sql = "UPDATE especialidades SET codigo = ?, nome = ? WHERE id = ?"
        cur = self.db.executar(sql, (self.codigo, self.nome, self.id))
        return bool(cur)

    # ------------------ DELETE ------------------
    def excluir(self):
        if not self.id:
            return False
        sql = "DELETE FROM especialidades WHERE id = ?"
        cur = self.db.executar(sql, (self.id,))
        return bool(cur)
