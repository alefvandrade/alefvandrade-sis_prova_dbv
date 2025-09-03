# Backend/Controllers/usuario_controller.py
from Backend.Models.usuario import Usuario

class UsuarioController:

    @staticmethod
    def criar_usuario(nome: str, email: str, senha: str):
        usuario = Usuario(nome=nome, email=email)
        usuario.cadastrar(senha)
        return usuario

    @staticmethod
    def buscar_usuario(usuario_id: int):
        return Usuario.buscar_por_id(usuario_id)

    @staticmethod
    def listar_usuarios():
        return Usuario.listar_todos()

    @staticmethod
    def atualizar_usuario(usuario_id: int, nome: str = None, email: str = None, senha: str = None):
        usuario = Usuario.buscar_por_id(usuario_id)
        if not usuario:
            return None
        if nome:
            usuario.nome = nome
        if email:
            usuario.email = email
        usuario.atualizar(senha)
        return usuario

    @staticmethod
    def excluir_usuario(usuario_id: int):
        usuario = Usuario.buscar_por_id(usuario_id)
        if usuario:
            return usuario.excluir()
        return False
