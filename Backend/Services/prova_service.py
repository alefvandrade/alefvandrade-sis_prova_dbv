# Backend/Services/prova_service.py
from Backend.Controllers.prova_controller import ProvaController
from Backend.Services.pdf_generator import gerar_doc_prova, gerar_gabarito  # Importa a função diretamente
from Backend.Models.questao import Questao

def gerar_prova_completa(usuario_id, especialidade_id, questoes):
    """
    Cria uma prova, associa as questões e gera o PDF + gabarito.
    """
    # Criar prova
    prova = ProvaController.criar_prova(usuario_id, especialidade_id)

    # Associar questões
    for ordem, q in enumerate(questoes, start=1):
        Questao.associar_com_prova(q.id, prova.id, ordem)

    # Gerar PDF e gabarito
    gerar_doc_prova(prova.id)
    gerar_gabarito(prova.id)    

    return prova