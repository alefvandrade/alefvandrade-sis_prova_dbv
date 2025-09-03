# Backend/Models/prova.py

from Backend.Database.connection import DatabaseConnection
from Backend.Models.questao import Questao
from datetime import datetime

class Prova:
    def __init__(self, usuario_id=None, especialidade_id=None, prova_id=None,
                 data_criacao=None, arquivo_pdf=None, arquivo_gabarito=None):
        self.id = prova_id
        self.usuario_id = usuario_id
        self.especialidade_id = especialidade_id
        self.data_criacao = data_criacao if data_criacao else datetime.now()
        self.arquivo_pdf = arquivo_pdf
        self.arquivo_gabarito = arquivo_gabarito
        self.db = DatabaseConnection()

    # ------------------ CREATE ------------------
    def cadastrar(self):
        sql = "INSERT INTO provas (usuario_id, especialidade_id, data_criacao, arquivo_pdf, arquivo_gabarito) VALUES (?, ?, ?, ?, ?)"
        cur = self.db.executar(sql, (self.usuario_id, self.especialidade_id, self.data_criacao, self.arquivo_pdf, self.arquivo_gabarito))
        if cur:
            self.id = cur.lastrowid
            return True
        return False

    # ------------------ READ ------------------
    def buscar_por_id(self, prova_id):
        sql = "SELECT id, usuario_id, especialidade_id, data_criacao, arquivo_pdf, arquivo_gabarito FROM provas WHERE id = ?"
        result = self.db.consultar(sql, (prova_id,))
        if result:
            self.id, self.usuario_id, self.especialidade_id, self.data_criacao, self.arquivo_pdf, self.arquivo_gabarito = result[0]
            return self
        return None

    def listar_todos(self):
        sql = "SELECT id, usuario_id, especialidade_id, data_criacao, arquivo_pdf, arquivo_gabarito FROM provas ORDER BY data_criacao DESC"
        return self.db.consultar(sql)

    def listar_com_questoes(self):
        """Retorna uma lista de provas com as questões incluídas"""
        provas = self.listar_todos()
        resultado = []
        for p in provas:
            prova_id = p[0]
            questao_obj = Questao()
            questoes = questao_obj.listar_por_prova(prova_id)  # método da classe Questao
            resultado.append({
                'prova': p,
                'questoes': questoes
            })
        return resultado

    # ------------------ UPDATE ------------------
    def atualizar(self):
        if not self.id:
            return False
        sql = "UPDATE provas SET usuario_id = ?, especialidade_id = ?, arquivo_pdf = ?, arquivo_gabarito = ? WHERE id = ?"
        cur = self.db.executar(sql, (self.usuario_id, self.especialidade_id, self.arquivo_pdf, self.arquivo_gabarito, self.id))
        return bool(cur)

    # ------------------ DELETE ------------------
    def excluir(self):
        if not self.id:
            return False
        sql = "DELETE FROM provas WHERE id = ?"
        cur = self.db.executar(sql, (self.id,))
        return bool(cur)
