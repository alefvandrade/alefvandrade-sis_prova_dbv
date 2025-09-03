# Backend/Services/pdf_generator.py
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from Backend.Controllers.prova_controller import ProvaController
from Backend.Controllers.gabarito_controller import GabaritoController

OUTPUT_FOLDER = "Data/Output"

def gerar_doc_prova(prova_id: int, incluir_gabarito: bool = False) -> str:
    """
    Gera o PDF da prova com todas as questões.
    Se incluir_gabarito=True, adiciona o gabarito no final.
    Retorna o caminho do arquivo PDF.
    """
    # Buscar prova e questões
    prova = ProvaController.buscar_prova(prova_id)
    questoes = ProvaController.listar_questoes(prova_id)

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    arquivo_pdf = os.path.join(OUTPUT_FOLDER, f"prova_{prova_id}.pdf")
    c = canvas.Canvas(arquivo_pdf, pagesize=A4)
    largura, altura = A4
    y = altura - 50

    # Título da prova
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"Prova ID: {prova.id}")
    y -= 30
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Especialidade: {prova.especialidade_id}")
    y -= 30

    # Inserir questões
    for idx, q in enumerate(questoes, start=1):
        c.setFont("Helvetica-Bold", 12)
        enunciado = f"{idx}. {q.enunciado}"
        y = escrever_texto(c, enunciado, y)
        
        # Questão múltipla
        if hasattr(q, "alternativas") and q.alternativas:
            for alt in q.alternativas:
                y = escrever_texto(c, f"   {alt}", y)
        
        # Questão prática
        if hasattr(q, "gerar_campo_assinatura"):
            assinatura = q.gerar_campo_assinatura()
            y = escrever_texto(c, assinatura, y)

        y -= 20
        if y < 100:
            c.showPage()
            y = altura - 50

    # Incluir gabarito se necessário
    if incluir_gabarito:
        c.showPage()
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, altura - 50, "Gabarito")
        y = altura - 80

        gabarito = GabaritoController.gerar_gabarito(prova_id)
        for idx, item in enumerate(gabarito.itens, start=1):
            enun, resp = item[1], item[2]
            y = escrever_texto(c, f"{idx}. {enun}\nResposta: {resp}", y)
            y -= 10
            if y < 100:
                c.showPage()
                y = altura - 50

    c.save()
    return arquivo_pdf


def escrever_texto(canvas_obj, texto: str, y: float, margem_esq: int = 50, linha_altura: int = 15) -> float:
    """
    Escreve texto no PDF, quebrando em linhas se necessário.
    """
    largura_max = 500
    palavras = texto.split()
    linha = ""
    for palavra in palavras:
        if canvas_obj.stringWidth(linha + " " + palavra) < largura_max:
            linha += " " + palavra
        else:
            canvas_obj.drawString(margem_esq, y, linha.strip())
            y -= linha_altura
            linha = palavra
    if linha:
        canvas_obj.drawString(margem_esq, y, linha.strip())
        y -= linha_altura
    return y
