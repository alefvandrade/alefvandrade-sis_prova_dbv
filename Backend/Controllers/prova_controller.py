from Backend.Models.prova import Prova

class ProvaController:
    @staticmethod
    def criar_prova(usuario_id, especialidade_id):
        """
        Cria e cadastra uma nova prova.
        """
        prova = Prova(usuario_id=usuario_id, especialidade_id=especialidade_id)
        prova.cadastrar()
        return prova

    @staticmethod
    def buscar_prova(prova_id):
        """
        Busca uma prova pelo ID.
        """
        return Prova.buscar_por_id(prova_id)
