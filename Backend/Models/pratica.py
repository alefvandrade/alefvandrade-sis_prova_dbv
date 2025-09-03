# Backend/Models/pratica.py
from Backend.Models.questao import Questao
from Backend.Database.connection import DatabaseConnection

class QuestaoPratica(Questao):
    """
    Representa uma questão prática.
    Herdada da superclasse Questao.
    Inclui espaço para assinatura e data.
    """
    def __init__(self, especialidade_id: int, enunciado: str,
                 id: int = None, criado_em: str = None):
        super().__init__(
            id=id,
            especialidade_id=especialidade_id,
            enunciado=enunciado,
            tipo="pratica",
            alternativas=None,
            resposta_correta=None,
            criado_em=criado_em
        )

    def cadastrar(self) -> bool:
        """
        Insere a questão prática no banco.
        """
        query = """
            INSERT INTO questoes (especialidade_id, enunciado, tipo, alternativas, resposta_correta)
            VALUES (?, ?, 'pratica', NULL, NULL)
        """
        params = (self.especialidade_id, self.enunciado)

        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            self.id = cursor.lastrowid
            return True

    @staticmethod
    def buscar_por_id(questao_id: int):
        """
        Recupera uma questão prática por ID.
        """
        query = """
            SELECT id, especialidade_id, enunciado, criado_em
            FROM questoes
            WHERE id = ? AND tipo = 'pratica'
        """
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (questao_id,))
            row = cursor.fetchone()

        if row:
            return QuestaoPratica(
                id=row[0],
                especialidade_id=row[1],
                enunciado=row[2],
                criado_em=row[3]
            )
        return None

    def gerar_campo_assinatura(self) -> str:
        """
        Retorna uma string com linhas para assinatura e data.
        """
        return "\nAss.: ______________________\nData: __ / __ / ____"
