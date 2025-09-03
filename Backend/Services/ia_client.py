import os
import configparser
import requests
import json

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
    Gera uma questão via API Vicuna.
    Retorna um dict {'enunciado': str, 'alternativas': list, 'resposta_correta': str}.
    """
    if not API_KEY:
        return {"erro": "API_KEY não configurada."}

    # Criar prompt
    if tipo == "multipla":
        prompt = f"Crie uma questão de múltipla escolha sobre '{tema}' com dificuldade {dificuldade}. Retorne enunciado, 4 alternativas e a resposta correta."
    elif tipo == "dissertativa":
        prompt = f"Crie uma questão dissertativa sobre '{tema}' com dificuldade {dificuldade}. Retorne enunciado."
    elif tipo == "pratica":
        prompt = f"Crie uma questão prática sobre '{tema}'. Inclua enunciado e espaço para assinatura e data."
    else:
        return {"erro": f"Tipo de questão inválido: {tipo}"}

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Você é um assistente especialista em criar questões de prova."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[IA CLIENT ERROR] Falha na chamada da API: {e}")
        return {"erro": str(e)}

    try:
        result = response.json()
        mensagem = result["choices"][0]["message"]["content"]
        return {"conteudo": mensagem}
    except (KeyError, json.JSONDecodeError) as e:
        print(f"[IA CLIENT ERROR] Erro ao processar resposta da API: {e}")
        return {"erro": str(e)}
