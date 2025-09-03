# Backend/Controllers/prova_controller.py
from Backend.Models.prova import Prova

class ProvaController:

    @staticmethod
    def criar_prova(usuario_id: int, especialidade_id: int):
        prova = Prova(usuario_id, especialidade_id)
        prova.cadastrar()
        return prova

    @staticmethod
    def adicionar_questao(prova_id: int, questao_id: int, ordem: int):
        prova = Prova.buscar_por_id(prova_id)
        if prova:
            return prova.adicionar_questao(questao_id, ordem)
        return False

    @staticmethod
    def listar_questoes(prova_id: int):
        prova = Prova.buscar_por_id(prova_id)
        if prova:
            return prova.listar_questoes()
        return []

    @staticmethod
    def atualizar_prova(prova_id: int, arquivo_pdf: str = None, arquivo_gabarito: str = None):
        prova = Prova.buscar_por_id(prova_id)
        if not prova:
            return None
        if arquivo_pdf:
            prova.arquivo_pdf = arquivo_pdf
        if arquivo_gabarito:
            prova.arquivo_gabarito = arquivo_gabarito
        prova.atualizar()
        return prova
