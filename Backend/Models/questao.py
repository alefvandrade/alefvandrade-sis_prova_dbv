# Backend/Models/questao.py
from Backend.Database.connection import DatabaseConnection

class Questao:
    def __init__(self, questao_id=None, enunciado=None, especialidade_id=None, prova_id=None):
        self.id = questao_id
        self.enunciado = enunciado
        self.especialidade_id = especialidade_id
        self.prova_id = prova_id
        self.db = DatabaseConnection()

    # ------------------ CREATE ------------------
    def cadastrar(self):
        sql = "INSERT INTO questoes (enunciado, especialidade_id, prova_id) VALUES (?, ?, ?)"
        cur = self.db.executar(sql, (self.enunciado, self.especialidade_id, self.prova_id))
        if cur:
            self.id = cur.lastrowid
            return True
        return False

    # ------------------ READ ------------------
    def buscar_por_id(self, questao_id):
        sql = "SELECT id, enunciado, especialidade_id, prova_id FROM questoes WHERE id = ?"
        result = self.db.consultar(sql, (questao_id,))
        if result:
            self.id, self.enunciado, self.especialidade_id, self.prova_id = result[0]
            return self
        return None

    def listar_todos(self):
        sql = "SELECT id, enunciado, especialidade_id, prova_id FROM questoes ORDER BY id"
        return self.db.consultar(sql)

    # ------------------ UPDATE ------------------
    def atualizar(self):
        if not self.id:
            return False
        sql = "UPDATE questoes SET enunciado = ?, especialidade_id = ?, prova_id = ? WHERE id = ?"
        cur = self.db.executar(sql, (self.enunciado, self.especialidade_id, self.prova_id, self.id))
        return bool(cur)

    # ------------------ DELETE ------------------
    def excluir(self):
        if not self.id:
            return False
        sql = "DELETE FROM questoes WHERE id = ?"
        cur = self.db.executar(sql, (self.id,))
        return bool(cur)
