# Backend/Models/usuario.py
import hashlib
from Backend.Database.connection import DatabaseConnection

class Usuario:
    def __init__(self, id=None, nome=None, email=None, senha_hash=None, criado_em=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.criado_em = criado_em

    @staticmethod
    def hash_senha(senha: str) -> str:
        """Criptografa a senha usando SHA-256"""
        return hashlib.sha256(senha.encode("utf-8")).hexdigest()

    def cadastrar(self, senha: str):
        """Cadastra o usuário no banco"""
        self.senha_hash = self.hash_senha(senha)
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO usuarios (nome, email, senha_hash)
                VALUES (?, ?, ?)
                """,
                (self.nome, self.email, self.senha_hash)
            )
            self.id = cursor.lastrowid

    @staticmethod
    def listar_todos():
        """Retorna uma lista de objetos Usuario"""
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios ORDER BY id")
            resultados = cursor.fetchall()
            usuarios = []
            for row in resultados:
                usuarios.append(
                    Usuario(
                        id=row["id"],
                        nome=row["nome"],
                        email=row["email"],
                        senha_hash=row["senha_hash"],
                        criado_em=row["criado_em"]
                    )
                )
            return usuarios

    @staticmethod
    def buscar_por_id(usuario_id):
        """Busca um usuário pelo ID"""
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))
            row = cursor.fetchone()
            if row:
                return Usuario(
                    id=row["id"],
                    nome=row["nome"],
                    email=row["email"],
                    senha_hash=row["senha_hash"],
                    criado_em=row["criado_em"]
                )
            return None
