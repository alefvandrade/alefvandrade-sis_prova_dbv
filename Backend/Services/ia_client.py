# Backend/Services/pdf_generator.py
import os
from fpdf import FPDF
from Backend.Models.prova import Prova
from Backend.Models.questoes_prova import QuestaoProva  # associação questão x prova

OUTPUT_FOLDER = "Data/Output"

def gerar_doc_prova(prova_id):
    """
    Gera PDF da prova e gabarito.
    Salva arquivos em Data/Output.
    """
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    prova = Prova.buscar_por_id(prova_id)
    questoes_prova = QuestaoProva.listar_por_prova(prova_id)

    # Criar PDF da prova
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Prova ID: {prova.id}", ln=True)
    pdf.cell(0, 10, f"Especialidade: {prova.especialidade_id}", ln=True)
    pdf.ln(10)

    # Escrever questões
    for qp in questoes_prova:
        q = qp.questao
        pdf.set_font("Arial", "B", 12)
        pdf.multi_cell(0, 8, f"{qp.ordem}. {q.enunciado}")
        pdf.ln(2)
        # Se for múltipla, escrever alternativas
        if hasattr(q, "alternativas") and q.alternativas:
            for i, alt in enumerate(q.alternativas, start=1):
                pdf.set_font("Arial", "", 12)
                pdf.multi_cell(0, 8, f"{chr(64+i)}. {alt}")
            pdf.ln(2)
        # Se prática, incluir linha de assinatura
        if hasattr(q, "tipo") and q.tipo == "pratica":
            pdf.multi_cell(0, 8, "Ass.: _____________________  Data: ___/___/_____")
            pdf.ln(4)

    arquivo_pdf = os.path.join(OUTPUT_FOLDER, f"prova_{prova.id}.pdf")
    pdf.output(arquivo_pdf)
    prova.arquivo_pdf = arquivo_pdf

    # Criar gabarito
    pdf_gab = FPDF()
    pdf_gab.add_page()
    pdf_gab.set_font("Arial", "B", 16)
    pdf_gab.cell(0, 10, f"Gabarito Prova ID: {prova.id}", ln=True)
    pdf_gab.ln(10)

    for qp in questoes_prova:
        q = qp.questao
        if hasattr(q, "resposta_correta") and q.resposta_correta:
            pdf_gab.set_font("Arial", "B", 12)
            pdf_gab.multi_cell(0, 8, f"{qp.ordem}. {q.resposta_correta}")

    arquivo_gab = os.path.join(OUTPUT_FOLDER, f"gabarito_{prova.id}.pdf")
    pdf_gab.output(arquivo_gab)
    prova.arquivo_gabarito = arquivo_gab

    # Salvar caminhos no DB
    prova.atualizar_arquivos_pdf()

def gerar_questao_ia(tipo, tema, dificuldade="media"):
    """
    Gera uma questão usando a API Vicuna via AimlAPI.
    Retorna dicionário com enunciado, alternativas e resposta correta.
    """
    import openai
    import configparser

    config = configparser.ConfigParser()
    config.read("Frontend/config.ini")

    API_KEY = config["VICUNA"]["API_KEY"]
    BASE_URL = config["VICUNA"]["BASE_URL"]
    MODEL = config["VICUNA"]["MODEL"]

    openai.api_key = API_KEY
    openai.api_base = BASE_URL

    prompt = f"Crie uma questão do tipo '{tipo}' sobre o tema: {tema}. Dificuldade: {dificuldade}."

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Você é um assistente que cria questões de prova."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    message = response.choices[0].message.content

    alternativas = None
    resposta_correta = None
    if tipo.lower() == "multipla":
        linhas = message.split("\n")
        enunciado = linhas[0]
        alternativas = [l for l in linhas[1:] if l.strip()]
        resposta_correta = alternativas[0] if alternativas else None
    else:
        enunciado = message

    return {"enunciado": enunciado, "alternativas": alternativas, "resposta_correta": resposta_correta}
