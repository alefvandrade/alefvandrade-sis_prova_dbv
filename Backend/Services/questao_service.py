from Backend.Services.ia_client import gerar_questao_ia
from Backend.Models.multipla import QuestaoMultipla
from Backend.Models.dissertativa import QuestaoDissertativa
from Backend.Models.pratica import QuestaoPratica
# from Backend.Models.questao import Questao


def gerar_questoes_do_texto(especialidade_id, texto, tipo, qtd=1):
    """
    Gera múltiplas questões a partir de um texto (extraído do PDF) usando IA.
    Retorna lista de objetos Questao*.
    """
    questoes_geradas = []

    for i in range(qtd):
        print(f"[LOG] Gerando questão {i+1} de {qtd}...")
        resultado = gerar_questao_ia(tipo, texto, dificuldade="media")

        if "erro" in resultado:
            print(f"[LOG] Questão {i+1} falhou: {resultado['erro']}")
            continue  # Continua gerando as demais

        conteudo = resultado.get("conteudo", "")
        if tipo == "multipla":
            questao = QuestaoMultipla(especialidade_id=especialidade_id, enunciado=conteudo, alternativas=[], resposta_correta="")
        elif tipo == "dissertativa":
            questao = QuestaoDissertativa(especialidade_id=especialidade_id, enunciado=conteudo)
        elif tipo == "pratica":
            questao = QuestaoPratica(especialidade_id=especialidade_id, enunciado=conteudo)
        else:
            continue

        questao.cadastrar()
        print(f"[LOG] Questão {i+1} gerada")
        questoes_geradas.append(questao)

    return questoes_geradas
