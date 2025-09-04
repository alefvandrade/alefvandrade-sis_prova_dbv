# Backend/Models/prova.py
import json
from Backend.Database.connection import DatabaseConnection
from Backend.Models.questao import Questao

class Prova:
    """
    Representa uma prova, associada a um usuário e uma especialidade.
    Pode conter várias questões (via questoes_prova).
    """
    def __init__(self, usuario_id: int, especialidade_id: int,
                 arquivo_pdf: str = None, arquivo_gabarito: str = None,
                 id: int = None, data_criacao: str = None, nome: str = None):
        self.id = id
        self.usuario_id = usuario_id
        self.especialidade_id = especialidade_id
        self.arquivo_pdf = arquivo_pdf
        self.arquivo_gabarito = arquivo_gabarito
        self.data_criacao = data_criacao
        self.nome = nome  # Adicionado o atributo nome

    # ---------------------------
    # CRUD Prova
    # ---------------------------

    def cadastrar(self) -> bool:
        query = """
            INSERT INTO provas (usuario_id, especialidade_id, nome, arquivo_pdf, arquivo_gabarito)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (self.usuario_id, self.especialidade_id, self.nome, self.arquivo_pdf, self.arquivo_gabarito)

        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            self.id = cursor.lastrowid
            return True

    @staticmethod
    def buscar_por_id(prova_id: int):
        query = "SELECT id, usuario_id, especialidade_id, nome, data_criacao, arquivo_pdf, arquivo_gabarito FROM provas WHERE id = ?"
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (prova_id,))
            row = cursor.fetchone()

        if row:
            return Prova(
                id=row[0],
                usuario_id=row[1],
                especialidade_id=row[2],
                nome=row[3],  # Adicionado o campo nome
                data_criacao=row[4],
                arquivo_pdf=row[5],
                arquivo_gabarito=row[6]
            )
        return None

    @staticmethod
    def listar_todas() -> list:
        query = "SELECT id, usuario_id, especialidade_id, nome, data_criacao, arquivo_pdf, arquivo_gabarito FROM provas"
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

        return [
            Prova(
                id=row[0],
                usuario_id=row[1],
                especialidade_id=row[2],
                nome=row[3],  # Adicionado o campo nome
                data_criacao=row[4],
                arquivo_pdf=row[5],
                arquivo_gabarito=row[6]
            )
            for row in rows
        ]

    def atualizar(self) -> bool:
        if not self.id:
            raise ValueError("Prova precisa ter um ID para ser atualizada.")

        query = """
            UPDATE provas
            SET usuario_id = ?, especialidade_id = ?, nome = ?, arquivo_pdf = ?, arquivo_gabarito = ?
            WHERE id = ?
        """
        params = (self.usuario_id, self.especialidade_id, self.nome, self.arquivo_pdf, self.arquivo_gabarito, self.id)

        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0

    def excluir(self) -> bool:
        if not self.id:
            raise ValueError("Prova precisa ter um ID para ser excluída.")

        query = "DELETE FROM provas WHERE id = ?"
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (self.id,))
            conn.commit()
            return cursor.rowcount > 0

    # ---------------------------
    # Associação com Questões
    # ---------------------------

    def adicionar_questao(self, questao_id: int, ordem: int) -> bool:
        """
        Associa uma questão à prova em determinada ordem.
        """
        if not self.id:
            raise ValueError("Prova precisa ser cadastrada antes de adicionar questões.")

        query = """
            INSERT INTO questoes_prova (prova_id, questao_id, ordem)
            VALUES (?, ?, ?)
        """
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (self.id, questao_id, ordem))
            conn.commit()
            return True

    def listar_questoes(self) -> list:
        """
        Retorna as questões associadas à prova, na ordem definida.
        """
        if not self.id:
            return []

        query = """
            SELECT q.id, q.especialidade_id, q.enunciado, q.tipo, q.alternativas, q.resposta_correta, q.criado_em
            FROM questoes_prova qp
            JOIN questoes q ON q.id = qp.questao_id
            WHERE qp.prova_id = ?
            ORDER BY qp.ordem ASC
        """
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (self.id,))
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