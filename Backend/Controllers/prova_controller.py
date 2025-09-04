from Backend.Models.prova import Prova

class ProvaController:
    @staticmethod
    def criar_prova(usuario_id, especialidade_id):
        # Lógica existente para criar prova
        prova = Prova(usuario_id=usuario_id, especialidade_id=especialidade_id)
        prova.cadastrar()  # Usando o método cadastrar da classe Prova
        return prova

    @staticmethod
    def buscar_prova(prova_id):
        """
        Busca uma prova pelo ID.
        """
        return Prova.buscar_por_id(prova_id)

    @staticmethod
    def listar_provas():
        """
        Lista todas as provas cadastradas.
        """
        return Prova.listar_todas()

    @staticmethod
    def listar_questoes(prova_id):
        # Lógica existente para listar questões
        prova = Prova.buscar_por_id(prova_id)
        if prova:
            return prova.listar_questoes()
        return []