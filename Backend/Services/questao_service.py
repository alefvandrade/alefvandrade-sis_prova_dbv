# Backend/Services/questao_service.py
from Backend.Services.ia_client import gerar_questao_ia
from Backend.Models.multipla import QuestaoMultipla
from Backend.Models.dissertativa import QuestaoDissertativa
from Backend.Models.pratica import QuestaoPratica

def gerar_questoes_do_texto(especialidade_id: int, texto: str, tipo: str, qtd: int = 1):
    """
    Gera uma lista de questões a partir do texto extraído do PDF.
    Chama a IA para criar cada questão.
    """
    questoes_geradas = []

    for _ in range(qtd):
        resultado = gerar_questao_ia(tipo, texto, dificuldade="media")
        enunciado = resultado.get("enunciado", "")
        alternativas = resultado.get("alternativas", None)
        resposta_correta = resultado.get("resposta_correta", None)

        if tipo.lower() == "multipla":
            questao = QuestaoMultipla(
                especialidade_id=especialidade_id,
                enunciado=enunciado,
                alternativas=alternativas,
                resposta_correta=resposta_correta
            )
        elif tipo.lower() == "dissertativa":
            questao = QuestaoDissertativa(
                especialidade_id=especialidade_id,
                enunciado=enunciado
            )
        elif tipo.lower() == "pratica":
            questao = QuestaoPratica(
                especialidade_id=especialidade_id,
                enunciado=enunciado
            )
        else:
            continue

        questao.cadastrar()
        questoes_geradas.append(questao)

    return questoes_geradas
