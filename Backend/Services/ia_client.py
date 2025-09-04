# ia_client.py
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
BASE_URL = "https://api.aimlapi.com/v1"  # Padrão seguro
MODEL = "gpt-3.5-turbo"  # Padrão seguro, ajuste se necessário

if "VICUNA" in config:
    API_KEY = config["VICUNA"].get("API_KEY")
    BASE_URL = config["VICUNA"].get("BASE_URL", BASE_URL)
    MODEL = config["VICUNA"].get("MODEL", MODEL)

if not API_KEY:
    print(f"[ERRO] API_KEY não encontrada no {CONFIG_PATH}. Verifique o arquivo config.ini.")
    exit(1)
else:
    print(f"[DEBUG] API_KEY configurada. BASE_URL: {BASE_URL}, MODEL: {MODEL}")

def gerar_questao_ia(tipo: str, tema: str, dificuldade="media") -> dict:
    """
    Gera uma questão via API (chat ou completion) no formato JSON estruturado.
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

    # Detecta automaticamente se é modelo de chat ou completion
    is_chat_model = any(m in MODEL.lower() for m in ["gpt", "chat", "turbo", "4o", "claude", "vicuna"])

    if is_chat_model:
        endpoint = f"{BASE_URL}/chat/completions"
        data = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "Você é um gerador de questões de prova. Responda sempre em JSON válido."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 512
        }
    else:
        endpoint = f"{BASE_URL}/completions"
        data = {
            "model": MODEL,
            "prompt": prompt,
            "max_tokens": 512,
            "temperature": 0.7
        }

    print(f"[DEBUG] Endpoint: {endpoint}")
    print(f"[DEBUG] Payload: {json.dumps(data)}")

    try:
        response = requests.post(endpoint, headers=headers, json=data, timeout=30)
        response.raise_for_status()  # Levanta exceção para códigos de erro HTTP
        result = response.json()

        print(f"[DEBUG] Response Status: {response.status_code}")
        print(f"[DEBUG] Full Response: {json.dumps(result, indent=2)}")

        # Extrai texto dependendo do tipo de modelo
        if is_chat_model:
            mensagem = result["choices"][0]["message"]["content"].strip()
        else:
            mensagem = result["choices"][0]["text"].strip()

        print("\n[DEBUG IA RAW RESPONSE]:")
        print(mensagem)
        print("------------------------------------------------\n")

        if mensagem.startswith("```"):
            mensagem = mensagem.strip("```json)").strip("```").strip()

        dados = json.loads(mensagem)
        return dados

    except requests.RequestException as e:
        error_msg = f"Falha na chamada da API: {e} (Status: {getattr(e.response, 'status_code', 'N/A')})"
        print(f"[IA CLIENT ERROR] {error_msg}")
        return {"erro": error_msg}
    except (KeyError, json.JSONDecodeError) as e:
        error_msg = f"Erro ao processar resposta da API: {e}"
        print(f"[IA CLIENT ERROR] {error_msg}")
        return {"erro": error_msg}
    except Exception as e:
        error_msg = f"Erro inesperado: {e}"
        print(f"[IA CLIENT ERROR] {error_msg}")
        return {"erro": error_msg}
