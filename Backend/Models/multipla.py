# Backend/Models/multipla.py
import json
from Backend.Models.questao import Questao
from Backend.Database.connection import DatabaseConnection

class QuestaoMultipla(Questao):
    """
    Representa uma questão de múltipla escolha (objetiva).
    Herdada da superclasse Questao.
    """
    def __init__(self, especialidade_id: int, enunciado: str,
                 alternativas: list, resposta_correta: str,
                 id: int = None, criado_em: str = None):
        super().__init__(
            id=id,
            especialidade_id=especialidade_id,
            enunciado=enunciado,
            tipo="objetiva",  # sempre será objetiva
            alternativas=alternativas,
            resposta_correta=resposta_correta,
            criado_em=criado_em
        )

    def cadastrar(self) -> bool:
        """
        Insere a questão de múltipla escolha no banco.
        """
        query = """
            INSERT INTO questoes (especialidade_id, enunciado, tipo, alternativas, resposta_correta)
            VALUES (?, ?, 'objetiva', ?, ?)
        """
        params = (
            self.especialidade_id,
            self.enunciado,
            json.dumps(self.alternativas, ensure_ascii=False),
            self.resposta_correta
        )

        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            self.id = cursor.lastrowid
            return True

    @staticmethod
    def buscar_por_id(questao_id: int):
        """
        Recupera uma questão múltipla por ID.
        """
        query = """
            SELECT id, especialidade_id, enunciado, alternativas, resposta_correta, criado_em
            FROM questoes
            WHERE id = ? AND tipo = 'objetiva'
        """
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (questao_id,))
            row = cursor.fetchone()

        if row:
            return QuestaoMultipla(
                id=row[0],
                especialidade_id=row[1],
                enunciado=row[2],
                alternativas=json.loads(row[3]) if row[3] else [],
                resposta_correta=row[4],
                criado_em=row[5]
            )
        return None
