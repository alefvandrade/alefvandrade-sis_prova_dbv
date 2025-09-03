import os
from fpdf import FPDF
import fitz  # PyMuPDF para ler PDFs
from Backend.Controllers.prova_controller import ProvaController
from Backend.Controllers.questao_controller import QuestaoController

# -------------------- Função para gerar PDF da prova --------------------
def gerar_doc_prova(prova_id):
    prova = ProvaController.buscar_prova(prova_id)
    if not prova:
        raise ValueError(f"Prova com ID {prova_id} não encontrada.")

    questoes = QuestaoController.listar_questoes_por_prova(prova_id)
    if not questoes:
        raise ValueError("Nenhuma questão associada à prova.")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Prova: {prova.nome}", ln=True, align="C")
    pdf.ln(10)

    for i, q in enumerate(questoes, 1):
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 8, f"{i}. {q.enunciado}")
        if hasattr(q, "alternativas") and q.alternativas:
            for letra, alt in zip(["A", "B", "C", "D", "E"], q.alternativas):
                pdf.multi_cell(0, 8, f"   {letra}) {alt}")
        pdf.ln(5)

    output_path = os.path.join("Data", "Output", f"{prova.nome}.pdf")
    pdf.output(output_path)
    prova.arquivo_pdf = output_path
    ProvaController.atualizar_arquivo(prova_id, output_path)
    return output_path

# -------------------- Função para extrair texto de PDF --------------------
def extrair_texto_pdf(caminho_pdf):
    """
    Lê um PDF e retorna todo o texto contido nele como uma string.
    """
    if not os.path.exists(caminho_pdf):
        raise FileNotFoundError(f"PDF não encontrado: {caminho_pdf}")

    texto = ""
    doc = fitz.open(caminho_pdf)
    for pagina in doc:
        texto += pagina.get_text()
    doc.close()
    return texto