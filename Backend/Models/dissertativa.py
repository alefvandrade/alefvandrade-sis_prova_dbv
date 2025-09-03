# Backend/Models/questao_dissertativa.py
from Backend.Models.questao import Questao

class QuestaoDissertativa(Questao):
    def __init__(self, questao_id=None, enunciado=None, especialidade_id=None, prova_id=None, resposta_modelo=None):
        super().__init__(questao_id, enunciado, especialidade_id, prova_id)
        self.resposta_modelo = resposta_modelo

    # ------------------ CREATE ------------------
    def cadastrar(self):
        sql = """INSERT INTO questoes_dissertativa 
                 (enunciado, especialidade_id, prova_id, resposta_modelo)
                 VALUES (?, ?, ?, ?)"""
        cur = self.db.executar(sql, (self.enunciado, self.especialidade_id, self.prova_id, self.resposta_modelo))
        if cur:
            self.id = cur.lastrowid
            return True
        return False

    # ------------------ READ ------------------
    def buscar_por_id(self, questao_id):
        sql = """SELECT id, enunciado, especialidade_id, prova_id, resposta_modelo
                 FROM questoes_dissertativa WHERE id = ?"""
        result = self.db.consultar(sql, (questao_id,))
        if result:
            self.id, self.enunciado, self.especialidade_id, self.prova_id, self.resposta_modelo = result[0]
            return self
        return None

    def listar_todos(self):
        sql = """SELECT id, enunciado, especialidade_id, prova_id, resposta_modelo 
                 FROM questoes_dissertativa ORDER BY id"""
        return self.db.consultar(sql)

    # ------------------ UPDATE ------------------
    def atualizar(self):
        if not self.id:
            return False
        sql = """UPDATE questoes_dissertativa SET enunciado = ?, especialidade_id = ?, prova_id = ?, resposta_modelo = ?
                 WHERE id = ?"""
        cur = self.db.executar(sql, (self.enunciado, self.especialidade_id, self.prova_id, self.resposta_modelo, self.id))
        return bool(cur)

    # ------------------ DELETE ------------------
    def excluir(self):
        if not self.id:
            return False
        sql = "DELETE FROM questoes_dissertativa WHERE id = ?"
        cur = self.db.executar(sql, (self.id,))
        return bool(cur)
