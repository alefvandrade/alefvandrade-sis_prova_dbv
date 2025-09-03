# Backend/Controllers/usuario_controller.py
from Backend.Models.usuario import Usuario

class UsuarioController:

    @staticmethod
    def criar_usuario(nome: str, email: str, senha: str) -> Usuario:
        """
        Cria e cadastra um usuário no banco.
        Retorna o objeto Usuario cadastrado.
        """
        usuario = Usuario(nome=nome, email=email)
        usuario.cadastrar(senha)
        return usuario

    @staticmethod
    def listar_usuarios():
        """
        Retorna uma lista de todos os usuários cadastrados.
        """
        return Usuario.listar_todos()

    @staticmethod
    def buscar_usuario_por_id(usuario_id: int):
        """
        Retorna um usuário pelo ID ou None se não existir.
        """
        return Usuario.buscar_por_id(usuario_id)
