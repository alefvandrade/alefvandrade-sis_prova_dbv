import os
import configparser
import requests
import json

# Caminho do config.ini
CONFIG_PATH = os.path.join("config.ini")
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

# Lendo configuração
API_KEY = None
BASE_URL = "https://api.aimlapi.com/v1"
MODEL = "lmsys/vicuna-13b-v1.5"

if "VICUNA" in config:
    API_KEY = config["VICUNA"].get("API_KEY")
    BASE_URL = config["VICUNA"].get("BASE_URL", BASE_URL)
    MODEL = config["VICUNA"].get("MODEL", MODEL)

if not API_KEY:
    print(f"[ERRO] API_KEY não encontrada no {CONFIG_PATH}. Verifique o arquivo config.ini.")


def gerar_questao_ia(tipo: str, tema: str, dificuldade="media") -> dict:
    """
    Gera uma questão via API Vicuna no formato JSON estruturado.
    Retorna dict conforme o tipo de questão.
    """
    if not API_KEY:
        return {"erro": "API_KEY não configurada."}

    # Prompt estruturado forçando JSON válido
    if tipo == "objetiva":
        prompt = f"""
        Gere uma questão de múltipla escolha sobre o tema '{tema}' com dificuldade {dificuldade}.
        Retorne SOMENTE um JSON no seguinte formato, sem explicações adicionais:

        {{
          "enunciado": "string",
          "alternativas": ["A) ...", "B) ...", "C) ...", "D) ..."],
          "resposta_correta": "A"
        }}
        """
    elif tipo == "dissertativa":
        prompt = f"""
        Gere uma questão dissertativa sobre o tema '{tema}' com dificuldade {dificuldade}.
        Retorne SOMENTE um JSON no seguinte formato, sem explicações adicionais:

        {{
          "enunciado": "string",
          "resposta_esperada": "string"
        }}
        """
    elif tipo == "pratica":
        prompt = f"""
        Gere uma questão prática sobre o tema '{tema}' com dificuldade {dificuldade}.
        Retorne SOMENTE um JSON no seguinte formato, sem explicações adicionais:

        {{
          "enunciado": "string",
          "descricao_tarefa": "string"
        }}
        """
    else:
        return {"erro": f"Tipo de questão inválido: {tipo}"}

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Você é um gerador de questões de prova. Responda sempre em JSON válido."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[IA CLIENT ERROR] Falha na chamada da API: {e}")
        return {"erro": str(e)}

    try:
        result = response.json()
        mensagem = result["choices"][0]["message"]["content"].strip()

        # Debug bruto
        print("\n[DEBUG IA RAW RESPONSE]:")
        print(mensagem)
        print("------------------------------------------------\n")

        # Força JSON válido (remove trechos extras caso venham em ```json ... ```)
        if mensagem.startswith("```"):
            mensagem = mensagem.strip("```json").strip("```")

        dados = json.loads(mensagem)
        return dados

    except (KeyError, json.JSONDecodeError) as e:
        print(f"[IA CLIENT ERROR] Erro ao processar resposta da API: {e}")
        return {"erro": str(e)}
