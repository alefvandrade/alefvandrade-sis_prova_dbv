from Backend.Controllers.prova_controller import ProvaController
from Backend.Services.pdf_generator import PDFGenerator
from Backend.Models.questao import Questao


def gerar_prova_completa(usuario_id, especialidade_id, questoes):
    """
    Cria uma prova, associa as questões e gera o PDF + gabarito.
    """
    # Criar prova
    prova = ProvaController.criar_prova(usuario_id, especialidade_id)

    # Associar questões à prova
    for ordem, q in enumerate(questoes, start=1):
        Questao.associar_com_prova(q.id, prova.id, ordem)

    # Gerar PDF
    pdf_generator = PDFGenerator()
    pdf_path = pdf_generator.gerar_pdf(prova.id, questoes)

    return {
        "prova": prova,
        "pdf_path": pdf_path
    }
