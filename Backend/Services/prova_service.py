from Backend.Controllers.prova_controller import ProvaController
from Backend.Services.pdf_generator import PDFGenerator
from Backend.Models.questao import Questao

# Instanciar a classe
pdf_generator = PDFGenerator()

# Usar o método gerar_pdf
pdf_generator.gerar_pdf(prova_id, questoes)

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
    PDFGenerator(prova.id)

    return prova
