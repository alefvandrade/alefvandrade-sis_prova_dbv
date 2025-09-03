# Backend/Models/questoes_prova.py
import sqlite3
from Backend.Database.connection import DatabaseConnection

class QuestaoProva:
    def __init__(self, id=None, prova_id=None, questao_id=None, ordem=None):
        self.id = id
        self.prova_id = prova_id
        self.questao_id = questao_id
        self.ordem = ordem

    @staticmethod
    def adicionar_questao(prova_id, questao_id, ordem):
        db = DatabaseConnection()
        query = """
            INSERT INTO questoes_prova (prova_id, questao_id, ordem)
            VALUES (?, ?, ?)
        """
        db.execute(query, (prova_id, questao_id, ordem))

    @staticmethod
    def listar_por_prova(prova_id):
        """
        Retorna uma lista de objetos QuestaoProva para uma prova específica.
        Cada objeto terá o atributo 'questao' carregado com a questão correspondente.
        """
        db = DatabaseConnection()
        query = "SELECT * FROM questoes_prova WHERE prova_id = ? ORDER BY ordem"
        resultados = db.fetch_all(query, (prova_id,))
        questoes_prova = []

        for row in resultados:
            qp = QuestaoProva(id=row["id"], prova_id=row["prova_id"], questao_id=row["questao_id"], ordem=row["ordem"])
            
            # Carregar questão associada
            from Backend.Models.questao import Questao  # import dinâmico para evitar loop
            qp.questao = Questao.buscar_por_id(qp.questao_id)
            
            questoes_prova.append(qp)
        return questoes_prova
