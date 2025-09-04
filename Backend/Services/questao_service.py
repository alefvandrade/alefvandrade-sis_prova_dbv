from Backend.Models.questao import Questao
from ..Models.multipla import QuestaoMultipla
from ..Models.dissertativa import QuestaoDissertativa
from ..Models.pratica import QuestaoPratica

from Backend.Services.ia_client import gerar_questao_ia

def gerar_questoes_do_texto(especialidade_id: int, texto: str, tipo: str, qtd: int = 5):
    """
    Gera questões com base em um texto fornecido usando a IA.
    Retorna lista de instâncias de Questao.
    """
    questoes = []

    for i in range(qtd):
        print(f"[LOG] Gerando questão {i+1}/{qtd}...")

        resultado = gerar_questao_ia(tipo, texto, dificuldade="media")

        if "erro" in resultado:
            print(f"[ERRO] Falha ao gerar questão {i+1}: {resultado['erro']}")
            continue

        print(f"[DEBUG QUESTÃO {i+1} JSON]: {resultado}")

        # Cria instância da questão conforme tipo
        if tipo == "objetiva":
            q = QuestaoMultipla(
                especialidade_id=especialidade_id,
                enunciado=resultado.get("enunciado", ""),
                alternativas=resultado.get("alternativas", []),
                resposta_correta=resultado.get("resposta_correta", "")
            )
        elif tipo == "dissertativa":
            q = QuestaoDissertativa(
                especialidade_id=especialidade_id,
                enunciado=resultado.get("enunciado", ""),
                resposta_esperada=resultado.get("resposta_esperada", "")
            )
        elif tipo == "pratica":
            q = QuestaoPratica(
                especialidade_id=especialidade_id,
                enunciado=resultado.get("enunciado", ""),
                descricao_tarefa=resultado.get("descricao_tarefa", "")
            )
        else:
            print(f"[ERRO] Tipo de questão inválido: {tipo}")
            continue

        q.salvar()
        questoes.append(q)

        print(f"[LOG] Questão {i+1} salva com sucesso.")

    return questoes
