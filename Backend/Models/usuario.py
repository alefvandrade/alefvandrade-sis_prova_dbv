# Backend/Models/usuario.py
import bcrypt
from Backend.Database.connection import DatabaseConnection

class Usuario:
    """
    Representa um usuário do sistema.
    Usa bcrypt para armazenar senhas com segurança.
    """
    def __init__(self, nome: str, email: str, senha_hash: str = None, id: int = None, criado_em: str = None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash  # sempre hash (bcrypt)
        self.criado_em = criado_em

    # ---------------------------
    # Métodos de senha
    # ---------------------------
    @staticmethod
    def gerar_hash(senha: str) -> str:
        """
        Gera um hash seguro para a senha usando bcrypt.
        """
        return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verificar_senha(self, senha: str) -> bool:
        """
        Verifica se a senha informada corresponde ao hash armazenado.
        """
        return bcrypt.checkpw(senha.encode("utf-8"), self.senha_hash.encode("utf-8"))

    # ---------------------------
    # CRUD
    # ---------------------------
    def cadastrar(self, senha: str) -> bool:
        """
        Cadastra o usuário no banco. A senha passada será criptografada.
        """
        self.senha_hash = self.gerar_hash(senha)

        query = """
            INSERT INTO usuarios (nome, email, senha_hash)
            VALUES (?, ?, ?)
        """
        params = (self.nome, self.email, self.senha_hash)

        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            self.id = cursor.lastrowid
            return True

    @staticmethod
    def buscar_por_id(usuario_id: int):
        query = "SELECT id, nome, email, senha_hash, criado_em FROM usuarios WHERE id = ?"
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (usuario_id,))
            row = cursor.fetchone()

        if row:
            return Usuario(id=row[0], nome=row[1], email=row[2], senha_hash=row[3], criado_em=row[4])
        return None

    @staticmethod
    def listar_todos() -> list:
        query = "SELECT id, nome, email, senha_hash, criado_em FROM usuarios"
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

        return [Usuario(id=row[0], nome=row[1], email=row[2], senha_hash=row[3], criado_em=row[4]) for row in rows]

    def atualizar(self, senha: str = None) -> bool:
        """
        Atualiza os dados do usuário. Se senha for passada, gera novo hash.
        """
        if not self.id:
            raise ValueError("Usuário precisa ter um ID para ser atualizado.")

        if senha:
            self.senha_hash = self.gerar_hash(senha)

        query = """
            UPDATE usuarios
            SET nome = ?, email = ?, senha_hash = ?
            WHERE id = ?
        """
        params = (self.nome, self.email, self.senha_hash, self.id)

        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0

    def excluir(self) -> bool:
        if not self.id:
            raise ValueError("Usuário precisa ter um ID para ser excluído.")

        query = "DELETE FROM usuarios WHERE id = ?"
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (self.id,))
            conn.commit()
            return cursor.rowcount > 0
