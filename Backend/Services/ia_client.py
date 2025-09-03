# Backend/Services/ia_client.py
import os
import requests

class VicunaClient:
    """
    Cliente central para comunicação com a API da Vicuna.
    Permite envio de prompts e gerenciamento de autenticação.
    """

    def __init__(self, api_key: str = None, base_url: str = None, timeout: int = 30):
        self.api_key = api_key or os.getenv("VICUNA_API_KEY", "SUA_CHAVE_API_VICUNA")
        self.base_url = base_url or os.getenv("VICUNA_BASE_URL", "https://api.vicuna.ai/v1")
        self.timeout = timeout

        if not self.api_key:
            raise ValueError("Chave de API da Vicuna não encontrada. Defina VICUNA_API_KEY.")

    def send_prompt(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> dict:
        """
        Envia um prompt para a API da Vicuna e retorna a resposta em JSON.
        """
        url = f"{self.base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "vicuna-7b",  # pode ser ajustado se precisar
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            # Estrutura esperada da resposta
            if "choices" in data and len(data["choices"]) > 0:
                return {
                    "content": data["choices"][0]["message"]["content"],
                    "raw": data
                }
            else:
                return {
                    "error": "Resposta inesperada da API",
                    "raw": data
                }

        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def health_check(self) -> bool:
        """
        Verifica se a API está acessível.
        """
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except Exception:
            return False


# Exemplo de uso isolado
if __name__ == "__main__":
    client = VicunaClient()
    prompt = "Gere uma questão de matemática básica sobre frações, nível fácil."
    resposta = client.send_prompt(prompt)
    print(resposta)
