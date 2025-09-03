# Backend/Models/questao_multipla.py
from Backend.Models.questao import Questao

class QuestaoMultipla(Questao):
    def __init__(self, questao_id=None, enunciado=None, especialidade_id=None, prova_id=None,
                 opcao_a=None, opcao_b=None, opcao_c=None, opcao_d=None, opcao_e=None, resposta=None):
        super().__init__(questao_id, enunciado, especialidade_id, prova_id)
        self.opcao_a = opcao_a
        self.opcao_b = opcao_b
        self.opcao_c = opcao_c
        self.opcao_d = opcao_d
        self.opcao_e = opcao_e
        self.resposta = resposta

    # ------------------ CREATE ------------------
    def cadastrar(self):
        sql = """INSERT INTO questoes_multipla 
                 (enunciado, especialidade_id, prova_id, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e, resposta)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        cur = self.db.executar(sql, (self.enunciado, self.especialidade_id, self.prova_id,
                                     self.opcao_a, self.opcao_b, self.opcao_c, self.opcao_d, self.opcao_e, self.resposta))
        if cur:
            self.id = cur.lastrowid
            return True
        return False

    # ------------------ READ ------------------
    def buscar_por_id(self, questao_id):
        sql = """SELECT id, enunciado, especialidade_id, prova_id, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e, resposta 
                 FROM questoes_multipla WHERE id = ?"""
        result = self.db.consultar(sql, (questao_id,))
        if result:
            (self.id, self.enunciado, self.especialidade_id, self.prova_id,
             self.opcao_a, self.opcao_b, self.opcao_c, self.opcao_d, self.opcao_e, self.resposta) = result[0]
            return self
        return None

    def listar_todos(self):
        sql = """SELECT id, enunciado, especialidade_id, prova_id, opcao_a, opcao_b, opcao_c, opcao_d, opcao_e, resposta 
                 FROM questoes_multipla ORDER BY id"""
        return self.db.consultar(sql)

    # ------------------ UPDATE ------------------
    def atualizar(self):
        if not self.id:
            return False
        sql = """UPDATE questoes_multipla SET enunciado = ?, especialidade_id = ?, prova_id = ?, 
                 opcao_a = ?, opcao_b = ?, opcao_c = ?, opcao_d = ?, opcao_e = ?, resposta = ? 
                 WHERE id = ?"""
        cur = self.db.executar(sql, (self.enunciado, self.especialidade_id, self.prova_id,
                                     self.opcao_a, self.opcao_b, self.opcao_c, self.opcao_d, self.opcao_e,
                                     self.resposta, self.id))
        return bool(cur)

    # ------------------ DELETE ------------------
    def excluir(self):
        if not self.id:
            return False
        sql = "DELETE FROM questoes_multipla WHERE id = ?"
        cur = self.db.executar(sql, (self.id,))
        return bool(cur)
