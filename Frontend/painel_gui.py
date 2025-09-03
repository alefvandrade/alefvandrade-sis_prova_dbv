# Frontend/painel_gui.py
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QInputDialog, QListWidget, QMessageBox
)
from Backend.Controllers.usuario_controller import UsuarioController
from Backend.Controllers.especialidade_controller import EspecialidadeController
from Backend.Services.pdf_service import extrair_texto_pdf
from Backend.Services.questao_service import gerar_questoes_do_texto
from Backend.Services.prova_service import gerar_prova_completa

PDF_INPUT_FOLDER = "Data/Input"

class PainelGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Painel Sistema de Provas")
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()

        self.label = QLabel("Selecione uma ação:")
        layout.addWidget(self.label)

        # Botões
        botoes = [
            ("Cadastrar Usuário", self.cadastrar_usuario),
            ("Listar Usuários", self.listar_usuarios),
            ("Cadastrar Especialidade", self.cadastrar_especialidade),
            ("Listar Especialidades", self.listar_especialidades),
            ("Enviar PDF", self.enviar_pdf),
            ("Listar PDFs Disponíveis", self.listar_pdfs),
            ("Gerar Prova a partir de PDF", self.gerar_prova)
        ]

        for nome, func in botoes:
            btn = QPushButton(nome)
            btn.clicked.connect(func)
            layout.addWidget(btn)

        self.setLayout(layout)

    # ---------------------------
    # Funções de cada botão
    # ---------------------------
    def cadastrar_usuario(self):
        nome, ok = QInputDialog.getText(self, "Cadastrar Usuário", "Nome:")
        if not ok or not nome:
            return
        email, ok = QInputDialog.getText(self, "Cadastrar Usuário", "Email:")
        if not ok or not email:
            return
        senha, ok = QInputDialog.getText(self, "Cadastrar Usuário", "Senha:")
        if not ok or not senha:
            return
        usuario = UsuarioController.criar_usuario(nome, email, senha)
        QMessageBox.information(self, "Sucesso", f"Usuário cadastrado: ID {usuario.id}")

    def listar_usuarios(self):
        usuarios = UsuarioController.listar_usuarios()
        msg = "\n".join([f"{u.id} - {u.nome} ({u.email})" for u in usuarios])
        QMessageBox.information(self, "Usuários", msg or "Nenhum usuário cadastrado.")

    def cadastrar_especialidade(self):
        codigo, ok = QInputDialog.getText(self, "Cadastrar Especialidade", "Código:")
        if not ok or not codigo:
            return
        nome, ok = QInputDialog.getText(self, "Cadastrar Especialidade", "Nome:")
        if not ok or not nome:
            return
        esp = EspecialidadeController.criar_especialidade(codigo, nome)
        QMessageBox.information(self, "Sucesso", f"Especialidade cadastrada: ID {esp.id}")

    def listar_especialidades(self):
        especialidades = EspecialidadeController.listar_especialidades()
        msg = "\n".join([f"{e.id} - {e.nome} ({e.codigo})" for e in especialidades])
        QMessageBox.information(self, "Especialidades", msg or "Nenhuma especialidade cadastrada.")

    def enviar_pdf(self):
        if not os.path.exists(PDF_INPUT_FOLDER):
            os.makedirs(PDF_INPUT_FOLDER)
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar PDF", "", "PDF Files (*.pdf)")
        if not file_path:
            return
        destino = os.path.join(PDF_INPUT_FOLDER, os.path.basename(file_path))
        with open(file_path, "rb") as src, open(destino, "wb") as dst:
            dst.write(src.read())
        QMessageBox.information(self, "Sucesso", f"PDF enviado para {destino}")

    def listar_pdfs(self):
        arquivos = [f for f in os.listdir(PDF_INPUT_FOLDER) if f.endswith(".pdf")]
        msg = "\n".join(arquivos)
        QMessageBox.information(self, "PDFs Disponíveis", msg or "Nenhum PDF disponível.")

    def gerar_prova(self):
        # Selecionar usuário
        usuarios = UsuarioController.listar_usuarios()
        if not usuarios:
            QMessageBox.warning(self, "Aviso", "Nenhum usuário cadastrado.")
            return
        items = [f"{u.id} - {u.nome}" for u in usuarios]
        item, ok = QInputDialog.getItem(self, "Selecionar Usuário", "Usuário:", items, 0, False)
        if not ok:
            return
        usuario_id = int(item.split(" - ")[0])

        # Selecionar especialidade
        especialidades = EspecialidadeController.listar_especialidades()
        if not especialidades:
            QMessageBox.warning(self, "Aviso", "Nenhuma especialidade cadastrada.")
            return
        items = [f"{e.id} - {e.nome}" for e in especialidades]
        item, ok = QInputDialog.getItem(self, "Selecionar Especialidade", "Especialidade:", items, 0, False)
        if not ok:
            return
        especialidade_id = int(item.split(" - ")[0])

        # Selecionar PDF
        arquivos = [f for f in os.listdir(PDF_INPUT_FOLDER) if f.endswith(".pdf")]
        if not arquivos:
            QMessageBox.warning(self, "Aviso", "Nenhum PDF disponível.")
            return
        item, ok = QInputDialog.getItem(self, "Selecionar PDF", "PDF:", arquivos, 0, False)
        if not ok:
            return
        caminho_pdf = os.path.join(PDF_INPUT_FOLDER, item)

        # Selecionar tipos de questões
        tipos_map = {"Múltipla": "multipla", "Dissertativa": "dissertativa", "Prática": "pratica"}
        tipo, ok = QInputDialog.getItem(self, "Tipo de Questão", "Escolha tipo de questão:", list(tipos_map.keys()), 0, False)
        if not ok:
            return
        tipo_selecionado = tipos_map[tipo]

        qtd, ok = QInputDialog.getInt(self, "Quantidade", f"Quantas questões de {tipo} gerar?", 1, 1, 50)
        if not ok:
            return

        # Extrair texto e gerar questões
        texto = extrair_texto_pdf(caminho_pdf)
        questoes = gerar_questoes_do_texto(especialidade_id, texto, tipo_selecionado, qtd=qtd)

        # Gerar prova completa
        prova = gerar_prova_completa(usuario_id, especialidade_id, questoes)
        QMessageBox.information(self, "Sucesso", f"Prova gerada!\nPDF: {prova.arquivo_pdf}\nGabarito: {prova.arquivo_gabarito}")


# Função para iniciar GUI
def iniciar_painel():
    app = QApplication(sys.argv)
    gui = PainelGUI()
    gui.show()
    sys.exit(app.exec_())
