# Backend/Models/questao_pratica.py
from Backend.Models.questao import Questao

class QuestaoPratica(Questao):
    def __init__(self, questao_id=None, enunciado=None, especialidade_id=None, prova_id=None, instrucoes=None, recurso=None):
        super().__init__(questao_id, enunciado, especialidade_id, prova_id)
        self.instrucoes = instrucoes  # detalhes do que o aluno deve fazer
        self.recurso = recurso        # link, arquivo ou referência prática

    # ------------------ CREATE ------------------
    def cadastrar(self):
        sql = """INSERT INTO questoes_pratica 
                 (enunciado, especialidade_id, prova_id, instrucoes, recurso)
                 VALUES (?, ?, ?, ?, ?)"""
        cur = self.db.executar(sql, (self.enunciado, self.especialidade_id, self.prova_id, self.instrucoes, self.recurso))
        if cur:
            self.id = cur.lastrowid
            return True
        return False

    # ------------------ READ ------------------
    def buscar_por_id(self, questao_id):
        sql = """SELECT id, enunciado, especialidade_id, prova_id, instrucoes, recurso
                 FROM questoes_pratica WHERE id = ?"""
        result = self.db.consultar(sql, (questao_id,))
        if result:
            self.id, self.enunciado, self.especialidade_id, self.prova_id, self.instrucoes, self.recurso = result[0]
            return self
        return None

    def listar_todos(self):
        sql = """SELECT id, enunciado, especialidade_id, prova_id, instrucoes, recurso
                 FROM questoes_pratica ORDER BY id"""
        return self.db.consultar(sql)

    # ------------------ UPDATE ------------------
    def atualizar(self):
        if not self.id:
            return False
        sql = """UPDATE questoes_pratica 
                 SET enunciado = ?, especialidade_id = ?, prova_id = ?, instrucoes = ?, recurso = ?
                 WHERE id = ?"""
        cur = self.db.executar(sql, (self.enunciado, self.especialidade_id, self.prova_id, self.instrucoes, self.recurso, self.id))
        return bool(cur)

    # ------------------ DELETE ------------------
    def excluir(self):
        if not self.id:
            return False
        sql = "DELETE FROM questoes_pratica WHERE id = ?"
        cur = self.db.executar(sql, (self.id,))
        return bool(cur)
