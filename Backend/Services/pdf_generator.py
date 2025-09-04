# Backend/Services/pdf_generator.py
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from Backend.Models.prova import Prova
from Backend.Models.especialidade import Especialidade  # <-- precisamos ter essa model
from datetime import datetime

class PDFGenerator:
    """Gera o PDF da prova a partir das questões."""

    def __init__(self, output_dir="data/pdfs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def gerar_pdf(self, prova_id: int, questoes: list):
        """
        Gera um PDF da prova com base no ID da prova e lista de questões.
        """
        # Buscar prova no banco
        prova = Prova.buscar_por_id(prova_id)
        if not prova:
            raise ValueError(f"Prova com ID {prova_id} não encontrada.")

        # Buscar nome da especialidade associada
        especialidade_nome = None
        try:
            especialidade = Especialidade.buscar_por_id(prova.especialidade_id)
            if especialidade:
                especialidade_nome = especialidade.nome
        except Exception:
            especialidade_nome = f"Especialidade {prova.especialidade_id}"

        # Nome do arquivo
        nome_arquivo = f"prova_{prova.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        caminho_arquivo = os.path.join(self.output_dir, nome_arquivo)

        # Criar PDF
        c = canvas.Canvas(caminho_arquivo, pagesize=A4)
        largura, altura = A4

        # Cabeçalho
        c.setFont("Helvetica-Bold", 16)
        titulo = f"Prova {prova.id}"
        if especialidade_nome:
            titulo += f" - {especialidade_nome}"
        c.drawString(100, altura - 80, titulo)

        c.setFont("Helvetica", 12)
        c.drawString(100, altura - 110, f"Data de Criação: {prova.data_criacao or datetime.now().strftime('%d/%m/%Y')}")

        # Questões
        y = altura - 160
        for i, questao in enumerate(questoes, start=1):
            texto = f"{i}) {questao.enunciado}"
            c.drawString(80, y, texto)
            y -= 40
            if y < 100:
                c.showPage()
                y = altura - 80

        c.save()

        return caminho_arquivo


