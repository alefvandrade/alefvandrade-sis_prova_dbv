# Backend/Models/questao.py
import json
from Backend.Database.connection import DatabaseConnection

class Questao:
    """
    Classe base para representar questões.
    Pode ser especializada em Objetiva, Dissertativa ou Prática.
    """
    def __init__(self, especialidade_id: int, enunciado: str, tipo: str = "objetiva",
                 alternativas: list = None, resposta_correta: str = None,
                 id: int = None, criado_em: str = None):
        self.id = id
        self.especialidade_id = especialidade_id
        self.enunciado = enunciado
        self.tipo = tipo
        self.alternativas = alternativas or []
        self.resposta_correta = resposta_correta
        self.criado_em = criado_em

    # ---------------------------
    # CRUD
    # ---------------------------

    def cadastrar(self) -> bool:
        """
        Insere a questão no banco de dados.
        """
        query = """
            INSERT INTO questoes (especialidade_id, enunciado, tipo, alternativas, resposta_correta)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (
            self.especialidade_id,
            self.enunciado,
            self.tipo,
            json.dumps(self.alternativas) if self.alternativas else None,
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
        query = "SELECT id, especialidade_id, enunciado, tipo, alternativas, resposta_correta, criado_em FROM questoes WHERE id = ?"
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (questao_id,))
            row = cursor.fetchone()

        if row:
            return Questao(
                id=row[0],
                especialidade_id=row[1],
                enunciado=row[2],
                tipo=row[3],
                alternativas=json.loads(row[4]) if row[4] else [],
                resposta_correta=row[5],
                criado_em=row[6]
            )
        return None

    @staticmethod
    def listar_todas() -> list:
        query = "SELECT id, especialidade_id, enunciado, tipo, alternativas, resposta_correta, criado_em FROM questoes"
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

        return [
            Questao(
                id=row[0],
                especialidade_id=row[1],
                enunciado=row[2],
                tipo=row[3],
                alternativas=json.loads(row[4]) if row[4] else [],
                resposta_correta=row[5],
                criado_em=row[6]
            )
            for row in rows
        ]

    def atualizar(self) -> bool:
        if not self.id:
            raise ValueError("Questão precisa ter um ID para ser atualizada.")

        query = """
            UPDATE questoes
            SET especialidade_id = ?, enunciado = ?, tipo = ?, alternativas = ?, resposta_correta = ?
            WHERE id = ?
        """
        params = (
            self.especialidade_id,
            self.enunciado,
            self.tipo,
            json.dumps(self.alternativas) if self.alternativas else None,
            self.resposta_correta,
            self.id
        )

        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0

    def excluir(self) -> bool:
        if not self.id:
            raise ValueError("Questão precisa ter um ID para ser excluída.")

        query = "DELETE FROM questoes WHERE id = ?"
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (self.id,))
            conn.commit()
            return cursor.rowcount > 0
