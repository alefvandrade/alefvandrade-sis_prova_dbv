from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QComboBox, QSpinBox, QTextEdit, QFileDialog, QMessageBox, QDialog,
    QFormLayout, QLineEdit, QDialogButtonBox, QListWidget
)
from PyQt5.QtCore import Qt
import os
from Backend.Controllers.usuario_controller import UsuarioController
from Backend.Controllers.especialidade_controller import EspecialidadeController
from Backend.Controllers.prova_controller import ProvaController
from Backend.Services.questao_service import gerar_questoes_do_texto
from Backend.Services.prova_service import gerar_prova_completa
from Backend.Services.pdf_generator import extrair_texto_pdf

class CadastroDialog(QDialog):
    def __init__(self, parent=None, tipo="usuário"):
        super().__init__(parent)
        self.setWindowTitle(f"Cadastrar Novo {tipo.capitalize()}")
        self.layout = QFormLayout(self)
        
        self.nome_input = QLineEdit(self)
        self.layout.addRow(f"Nome do {tipo}:", self.nome_input)
        
        if tipo == "especialidade":
            self.codigo_input = QLineEdit(self)
            self.layout.addRow("Código:", self.codigo_input)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)
    
    def get_data(self, tipo):
        if tipo == "usuário":
            return {"nome": self.nome_input.text(), "email": ""}  # Email temporário, pode ser expandido
        else:
            return {"nome": self.nome_input.text(), "codigo": self.codigo_input.text()}

class PainelGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Geração de Provas")
        self.setGeometry(100, 100, 900, 600)

        self.pdf_path = None
        self.texto_extraido = ""
        self.usuarios = self.carregar_usuarios()
        self.especialidades = self.carregar_especialidades()
        self.provas = self.carregar_provas()

        # Widget principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Frame superior (seleção de PDF e botões principais)
        self.frame_top = QWidget()
        self.top_layout = QHBoxLayout(self.frame_top)
        
        self.btn_pdf = QPushButton("Selecionar PDF")
        self.btn_pdf.clicked.connect(self.selecionar_pdf)
        self.top_layout.addWidget(self.btn_pdf)
        
        self.btn_gerar = QPushButton("Gerar Prova")
        self.btn_gerar.clicked.connect(self.gerar_prova)
        self.top_layout.addWidget(self.btn_gerar)
        
        self.btn_sair = QPushButton("Sair")
        self.btn_sair.setStyleSheet("color: red")
        self.btn_sair.clicked.connect(self.close)
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.btn_sair)
        
        self.layout.addWidget(self.frame_top)

        # Frame para parâmetros da prova
        self.frame_params = QWidget()
        self.params_layout = QHBoxLayout(self.frame_params)
        
        self.label_usuario = QLabel("Usuário:")
        self.params_layout.addWidget(self.label_usuario)
        self.usuario_combo = QComboBox()
        self.usuario_combo.addItems([f"{u.nome} (ID: {u.id})" for u in self.usuarios])
        self.params_layout.addWidget(self.usuario_combo)
        
        self.btn_cad_usuario = QPushButton("Cadastrar Usuário")
        self.btn_cad_usuario.clicked.connect(lambda: self.cadastrar("usuário"))
        self.params_layout.addWidget(self.btn_cad_usuario)
        
        self.label_especialidade = QLabel("Especialidade:")
        self.params_layout.addWidget(self.label_especialidade)
        self.especialidade_combo = QComboBox()
        self.especialidade_combo.addItems([f"{e.nome} (Código: {e.codigo})" for e in self.especialidades])
        self.params_layout.addWidget(self.especialidade_combo)
        
        self.btn_cad_especialidade = QPushButton("Cadastrar Especialidade")
        self.btn_cad_especialidade.clicked.connect(lambda: self.cadastrar("especialidade"))
        self.params_layout.addWidget(self.btn_cad_especialidade)
        
        self.label_qtd = QLabel("Quantidade de Questões:")
        self.params_layout.addWidget(self.label_qtd)
        self.qtd_spin = QSpinBox()
        self.qtd_spin.setRange(1, 50)
        self.qtd_spin.setValue(1)
        self.params_layout.addWidget(self.qtd_spin)
        
        self.params_layout.addStretch()
        self.layout.addWidget(self.frame_params)

        # Frame para listar PDFs gerados
        self.frame_provas = QWidget()
        self.provas_layout = QHBoxLayout(self.frame_provas)
        self.label_provas = QLabel("Provas Geradas:")
        self.provas_layout.addWidget(self.label_provas)
        self.provas_list = QListWidget()
        if self.provas:
            # Filtra apenas provas com arquivo_pdf válido
            provas_com_pdf = [p for p in self.provas if p.arquivo_pdf and os.path.exists(p.arquivo_pdf)]
            if provas_com_pdf:
                self.provas_list.addItems([f"Prova ID: {p.id} - {p.arquivo_pdf.split('/')[-1]}" for p in provas_com_pdf])
            else:
                self.provas_list.addItem("Nenhuma prova com PDF gerado.")
        else:
            self.provas_list.addItem("Nenhuma prova gerada.")
        self.provas_list.itemDoubleClicked.connect(self.abrir_pdf)
        self.provas_layout.addWidget(self.provas_list)
        self.layout.addWidget(self.frame_provas)

        # Frame para exibir texto do PDF
        self.label_texto = QLabel("Texto do PDF")
        self.layout.addWidget(self.label_texto)
        
        self.text_box = QTextEdit()
        self.text_box.setReadOnly(True)
        self.layout.addWidget(self.text_box)

    def carregar_usuarios(self):
        return UsuarioController.listar_usuarios()

    def carregar_especialidades(self):
        return EspecialidadeController.listar_especialidades()

    def carregar_provas(self):
        return ProvaController.listar_provas()

    def salvar_dados(self, tipo, dados):
        if tipo == "usuário":
            usuario = UsuarioController.criar_usuario(dados["nome"], dados["email"], "senha_padrao")  # Senha padrão temporária
            self.usuarios = self.carregar_usuarios()
            self.usuario_combo.clear()
            self.usuario_combo.addItems([f"{u.nome} (ID: {u.id})" for u in self.usuarios])
        else:
            especialidade = EspecialidadeController.criar_especialidade(dados["codigo"], dados["nome"])
            self.especialidades = self.carregar_especialidades()
            self.especialidade_combo.clear()
            self.especialidade_combo.addItems([f"{e.nome} (Código: {e.codigo})" for e in self.especialidades])

    def cadastrar(self, tipo):
        dialog = CadastroDialog(self, tipo)
        if dialog.exec_() == QDialog.Accepted:
            dados = dialog.get_data(tipo)
            if dados["nome"] and (tipo == "usuário" or dados["codigo"]):
                self.salvar_dados(tipo, dados)
            else:
                QMessageBox.warning(self, "Aviso", "Preencha todos os campos.")

    def closeEvent(self, event):
        event.accept()  # A conexão é gerenciada por DatabaseConnection

    def selecionar_pdf(self):
        """Seleciona um PDF e extrai o texto automaticamente."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecione um arquivo PDF", "", "Arquivos PDF (*.pdf)"
        )
        if not file_path:
            return

        self.pdf_path = file_path
        try:
            self.texto_extraido = extrair_texto_pdf(file_path)
            self.text_box.setText(self.texto_extraido)
            QMessageBox.information(self, "Sucesso", "Texto do PDF extraído com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao extrair texto do PDF:\n{e}")

    def gerar_prova(self):
        """Gera a prova a partir do texto extraído do PDF."""
        if not self.texto_extraido.strip():
            QMessageBox.warning(self, "Aviso", "Nenhum texto foi extraído do PDF.")
            return

        try:
            usuario_id = self.usuarios[self.usuario_combo.currentIndex()].id
            especialidade_id = self.especialidades[self.especialidade_combo.currentIndex()].id
            tipo = "objetiva"  # Simplificado; pode ser expandido
            qtd = self.qtd_spin.value()

            questoes = []
            for i in range(qtd):
                q = gerar_questoes_do_texto(int(especialidade_id), self.texto_extraido, tipo, qtd=1)
                questoes.extend(q)
                print(f"[LOG] Questão {i+1} gerada")

            prova = gerar_prova_completa(int(usuario_id), int(especialidade_id), questoes)
            self.provas = self.carregar_provas()
            self.provas_list.clear()
            if self.provas:
                provas_com_pdf = [p for p in self.provas if p.arquivo_pdf and os.path.exists(p.arquivo_pdf)]
                if provas_com_pdf:
                    self.provas_list.addItems([f"Prova ID: {p.id} - {p.arquivo_pdf.split('/')[-1]}" for p in provas_com_pdf])
                else:
                    self.provas_list.addItem("Nenhuma prova com PDF gerado.")
            else:
                self.provas_list.addItem("Nenhuma prova gerada.")
            QMessageBox.information(self, "Sucesso", f"Prova gerada com sucesso!\nArquivo: {prova.arquivo_pdf}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao gerar a prova:\n{e}")

    def abrir_pdf(self, item):
        """Abre o PDF selecionado ao dar duplo clique na lista."""
        if not self.provas:
            return
        prova_id = int(item.text().split(" - ")[0].replace("Prova ID: ", ""))
        prova = next((p for p in self.provas if p.id == prova_id), None)
        if prova and prova.arquivo_pdf and os.path.exists(prova.arquivo_pdf):
            os.startfile(prova.arquivo_pdf)  # Windows; para outros SO, ajustar com subprocess
        else:
            QMessageBox.warning(self, "Aviso", "Arquivo PDF não encontrado ou inválido.")