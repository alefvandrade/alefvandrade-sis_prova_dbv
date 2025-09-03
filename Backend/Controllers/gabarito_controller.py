# Backend/Controllers/gabarito_controller.py
from Backend.Models.prova import Prova
from Backend.Models.gabarito import Gabarito

class GabaritoController:

    @staticmethod
    def gerar_gabarito(prova_id: int):
        prova = Prova.buscar_por_id(prova_id)
        if not prova:
            return None
        gabarito = Gabarito(prova)
        gabarito.gerar()
        return gabarito

    @staticmethod
    def exportar_gabarito_txt(prova_id: int, caminho_arquivo: str):
        gabarito = GabaritoController.gerar_gabarito(prova_id)
        if gabarito:
            return gabarito.exportar_txt(caminho_arquivo)
        return False