# Backend/Controllers/especialidade_controller.py
from Backend.Models.especialidade import Especialidade

class EspecialidadeController:

    @staticmethod
    def criar_especialidade(codigo: str, nome: str):
        esp = Especialidade(codigo=codigo, nome=nome)
        esp.cadastrar()
        return esp

    @staticmethod
    def buscar_especialidade(esp_id: int):
        return Especialidade.buscar_por_id(esp_id)

    @staticmethod
    def listar_especialidades():
        return Especialidade.listar_todas()

    @staticmethod
    def atualizar_especialidade(esp_id: int, codigo: str = None, nome: str = None):
        esp = Especialidade.buscar_por_id(esp_id)
        if not esp:
            return None
        if codigo:
            esp.codigo = codigo
        if nome:
            esp.nome = nome
        esp.atualizar()
        return esp

    @staticmethod
    def excluir_especialidade(esp_id: int):
        esp = Especialidade.buscar_por_id(esp_id)
        if esp:
            return esp.excluir()
        return False
