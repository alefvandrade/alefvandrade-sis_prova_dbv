# Backend/Models/dissertativa.py
from Backend.Models.questao import Questao
from Backend.Database.connection import DatabaseConnection

class QuestaoDissertativa(Questao):
    """
    Representa uma questão dissertativa.
    Herdada da superclasse Questao.
    """
    def __init__(self, especialidade_id: int, enunciado: str,
                 linhas: int = 5, id: int = None, criado_em: str = None):
        super().__init__(
            id=id,
            especialidade_id=especialidade_id,
            enunciado=enunciado,
            tipo="dissertativa",
            alternativas=None,
            resposta_correta=None,
            criado_em=criado_em
        )
        self.linhas = linhas  # número de linhas esperadas na resposta

    def cadastrar(self) -> bool:
        """
        Insere a questão dissertativa no banco.
        Obs.: como não há alternativas nem resposta, ficam NULL.
        """
        query = """
            INSERT INTO questoes (especialidade_id, enunciado, tipo, alternativas, resposta_correta)
            VALUES (?, ?, 'dissertativa', NULL, NULL)
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
        Recupera uma questão dissertativa por ID.
        """
        query = """
            SELECT id, especialidade_id, enunciado, criado_em
            FROM questoes
            WHERE id = ? AND tipo = 'dissertativa'
        """
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (questao_id,))
            row = cursor.fetchone()

        if row:
            return QuestaoDissertativa(
                id=row[0],
                especialidade_id=row[1],
                enunciado=row[2],
                criado_em=row[3]
            )
        return None

    def gerar_campo_resposta(self) -> str:
        """
        Retorna uma string com linhas em branco para escrita.
        Exemplo:
        ______________________
        ______________________
        """
        return "\n".join(["_" * 50 for _ in range(self.linhas)])
