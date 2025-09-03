# Backend/Models/gabarito.py
from Backend.Models.prova import Prova
from Backend.Models.questao import Questao
import json

class Gabarito:
    """
    Representa o gabarito de uma prova.
    Organiza as respostas de todas as questões da prova.
    """
    def __init__(self, prova: Prova):
        self.prova = prova
        self.itens = []  # lista de tuplas (ordem, enunciado, resposta)

    def gerar(self):
        """
        Preenche a lista de itens do gabarito a partir das questões da prova.
        """
        self.itens = []
        questoes = self.prova.listar_questoes()
        for idx, questao in enumerate(questoes, start=1):
            if questao.tipo == "objetiva":
                resposta = questao.resposta_correta
            elif questao.tipo == "dissertativa":
                resposta = f"[Resposta esperada em {getattr(questao, 'linhas', 5)} linhas]"
            elif questao.tipo == "pratica":
                resposta = "Execução prática / Assinatura"
            else:
                resposta = "Tipo desconhecido"

            self.itens.append((idx, questao.enunciado, resposta))

    def imprimir(self):
        """
        Retorna uma string formatada do gabarito.
        """
        if not self.itens:
            self.gerar()

        linhas = []
        for ordem, enunciado, resposta in self.itens:
            linhas.append(f"{ordem}. {enunciado}\nResposta: {resposta}\n")
        return "\n".join(linhas)

    def exportar_txt(self, caminho_arquivo: str):
        """
        Salva o gabarito em arquivo TXT.
        """
        conteudo = self.imprimir()
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            f.write(conteudo)
        return True
