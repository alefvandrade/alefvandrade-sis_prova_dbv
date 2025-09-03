# Backend/Services/prova_service.py
from Backend.Models.prova import Prova
from Backend.Models.questoes_prova import QuestaoProva
from Backend.Services.pdf_generator import gerar_doc_prova

def gerar_prova_completa(usuario_id, especialidade_id, questoes):
    """
    Cria uma prova completa com lista de questões e gera o PDF + gabarito.
    """
    # Criar prova
    prova = Prova(usuario_id=usuario_id, especialidade_id=especialidade_id)
    prova.cadastrar()

    # Adicionar questões à prova
    for ordem, questao in enumerate(questoes, start=1):
        QuestaoProva.adicionar_questao(prova.id, questao.id, ordem)

    # Gerar PDF e gabarito
    gerar_doc_prova(prova.id)

    return prova
