import os
import fitz  # PyMuPDF
from fpdf import FPDF
from pdf2image import convert_from_path
import pytesseract

from Backend.Controllers.prova_controller import ProvaController

# Configurar manualmente o caminho do executável Tesseract (se não está no PATH)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extrair_texto_pdf(pdf_path):
    """
    Extrai texto de um PDF.
    - Primeiro tenta extrair texto digital (PDF pesquisável).
    - Se não encontrar texto, faz OCR página por página.
    """
    texto_final = ""

    # 1) Tentar extrair texto digital
    doc = fitz.open(pdf_path)
    for page in doc:
        texto_final += page.get_text()

    if texto_final.strip():  # Se encontrou texto, retorna
        return texto_final

    # 2) Se não encontrou, usar OCR
    print("[INFO] Nenhum texto encontrado, usando OCR...")
    pages = convert_from_path(pdf_path)
    for page in pages:
        texto_final += pytesseract.image_to_string(page, lang="por") + "\n"

    return texto_final


def gerar_doc_prova(prova_id):
    """
    Gera o PDF da prova a partir do ID da prova e suas questões.
    """
    prova = ProvaController.buscar_prova(prova_id)
    if not prova:
        raise ValueError(f"Prova com ID {prova_id} não encontrada.")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, f"Prova: {prova.nome}", ln=True, align="C")
    pdf.ln(10)

    # Buscar questões relacionadas
    questoes = ProvaController.listar_questoes(prova.id)

    pdf.set_font("Arial", "", 12)
    for i, q in enumerate(questoes, start=1):
        pdf.multi_cell(0, 10, f"{i}) {q.enunciado}")
        if q.tipo == "objetiva" and q.alternativas:
            alternativas = eval(q.alternativas)  # armazenadas como JSON string
            for letra, alt in zip("ABCDE", alternativas):
                pdf.multi_cell(0, 10, f"   {letra}) {alt}")
        elif q.tipo == "pratica":
            pdf.ln(5)
            pdf.multi_cell(0, 10, "Ass.: _______________________   Data: ____/____/________")
        pdf.ln(8)

    # Salvar arquivo
    output_dir = "Data/Output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"prova_{prova.id}.pdf")
    pdf.output(output_path)

    # Atualizar caminho no banco
    prova.arquivo_pdf = output_path
    prova.atualizar()
    return output_path


def gerar_gabarito(prova_id):
    """
    Gera o gabarito separado da prova.
    """
    prova = ProvaController.buscar_prova(prova_id)
    if not prova:
        raise ValueError(f"Prova com ID {prova_id} não encontrada.")

    questoes = ProvaController.listar_questoes(prova.id)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, f"Gabarito - {prova.nome}", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    for i, q in enumerate(questoes, start=1):
        resposta = q.resposta_correta if q.resposta_correta else "—"
        pdf.multi_cell(0, 10, f"{i}) {resposta}")

    # Salvar arquivo
    output_dir = "Data/Output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"gabarito_{prova.id}.pdf")
    pdf.output(output_path)

    # Atualizar caminho no banco
    prova.arquivo_gabarito = output_path
    prova.atualizar()
    return output_path