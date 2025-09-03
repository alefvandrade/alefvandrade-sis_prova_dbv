# Backend/Services/pdf_service.py
import os
from PyPDF2 import PdfReader

def extrair_texto_pdf(caminho_pdf: str) -> str:
    """
    Extrai todo o texto de um arquivo PDF.
    """
    if not os.path.exists(caminho_pdf):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_pdf}")
    
    reader = PdfReader(caminho_pdf)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text() + "\n"
    
    return texto
