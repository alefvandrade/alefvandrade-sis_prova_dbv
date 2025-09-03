# Backend/Controllers/questao_controller.py
from Backend.Models.multipla import QuestaoMultipla
from Backend.Models.dissertativa import QuestaoDissertativa
from Backend.Models.pratica import QuestaoPratica
from Backend.Services.ia_client import gerar_questao_ia

class QuestaoController:

    @staticmethod
    def criar_questao_multipla(especialidade_id: int, enunciado: str, alternativas: list, resposta_correta: str):
        q = QuestaoMultipla(especialidade_id, enunciado, alternativas, resposta_correta)
        q.cadastrar()
        return q

    @staticmethod
    def criar_questao_dissertativa(especialidade_id: int, enunciado: str, linhas: int = 5):
        q = QuestaoDissertativa(especialidade_id, enunciado, linhas)
        q.cadastrar()
        return q

    @staticmethod
    def criar_questao_pratica(especialidade_id: int, enunciado: str):
        q = QuestaoPratica(especialidade_id, enunciado)
        q.cadastrar()
        return q

    @staticmethod
    def criar_questao_ia(tipo: str, especialidade_id: int, tema: str, dificuldade: str = "media"):
        """
        Chama a IA para gerar a questão e cadastra automaticamente.
        """
        resultado = gerar_questao_ia(tipo=tipo, tema=tema, dificuldade=dificuldade)

        if tipo == "multipla":
            return QuestaoMultipla(especialidade_id, resultado["enunciado"], resultado["alternativas"], resultado["resposta_correta"]).cadastrar()
        elif tipo == "dissertativa":
            return QuestaoDissertativa(especialidade_id, resultado["enunciado"]).cadastrar()
        elif tipo == "pratica":
            return QuestaoPratica(especialidade_id, resultado["enunciado"]).cadastrar()
        else:
            return None
