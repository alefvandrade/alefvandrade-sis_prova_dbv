# Backend/Models/especialidade.py
from Backend.Database.connection import DatabaseConnection

class Especialidade:
    """
    Representa uma especialidade (área de conhecimento).
    """
    def __init__(self, codigo: str, nome: str, id: int = None, criado_em: str = None):
        self.id = id
        self.codigo = codigo
        self.nome = nome
        self.criado_em = criado_em

    # ---------------------------
    # CRUD
    # ---------------------------

    def cadastrar(self) -> bool:
        """
        Insere uma nova especialidade no banco de dados.
        """
        query = """
            INSERT INTO especialidades (codigo, nome)
            VALUES (?, ?)
        """
        params = (self.codigo, self.nome)

        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            self.id = cursor.lastrowid
            return True

    @staticmethod
    def buscar_por_id(especialidade_id: int):
        """
        Busca uma especialidade pelo ID.
        """
        query = "SELECT id, codigo, nome, criado_em FROM especialidades WHERE id = ?"

        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (especialidade_id,))
            row = cursor.fetchone()

        if row:
            return Especialidade(id=row[0], codigo=row[1], nome=row[2], criado_em=row[3])
        return None

    @staticmethod
    def listar_todas() -> list:
        """
        Lista todas as especialidades cadastradas.
        """
        query = "SELECT id, codigo, nome, criado_em FROM especialidades"

        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

        return [Especialidade(id=row[0], codigo=row[1], nome=row[2], criado_em=row[3]) for row in rows]

    def atualizar(self) -> bool:
        """
        Atualiza uma especialidade existente.
        """
        if not self.id:
            raise ValueError("Especialidade precisa ter um ID para ser atualizada.")

        query = """
            UPDATE especialidades
            SET codigo = ?, nome = ?
            WHERE id = ?
        """
        params = (self.codigo, self.nome, self.id)

        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0

    def excluir(self) -> bool:
        """
        Exclui uma especialidade do banco.
        """
        if not self.id:
            raise ValueError("Especialidade precisa ter um ID para ser excluída.")

        query = "DELETE FROM especialidades WHERE id = ?"

        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (self.id,))
            conn.commit()
            return cursor.rowcount > 0
