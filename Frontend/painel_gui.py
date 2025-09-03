import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QComboBox, QSpinBox, QDialog,
    QProgressBar, QFileDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from Backend.Controllers.usuario_controller import UsuarioController
from Backend.Controllers.especialidade_controller import EspecialidadeController
from Backend.Services.questao_service import gerar_questoes_do_texto
from Backend.Services.prova_service import gerar_prova_completa
from Backend.Services.pdf_generator import extrair_texto_pdf

# -------------------- Janela de Tabela --------------------
class TabelaDialog(QDialog):
    def __init__(self, titulo, dados, colunas):
        super().__init__()
        self.setWindowTitle(titulo)
        self.resize(600, 400)
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(len(colunas))
        self.table.setHorizontalHeaderLabels(colunas)
        self.table.setRowCount(len(dados))

        for i, linha in enumerate(dados):
            for j, valor in enumerate(linha):
                self.table.setItem(i, j, QTableWidgetItem(str(valor)))

        layout.addWidget(self.table)
        self.setLayout(layout)

# -------------------- Thread de Geração --------------------
class GerarQuestaoThread(QThread):
    terminado = pyqtSignal(list)

    def __init__(self, especialidade_id, texto, tipo, qtd):
        super().__init__()
        self.especialidade_id = especialidade_id
        self.texto = texto
        self.tipo = tipo
        self.qtd = qtd

    def run(self):
        questoes = gerar_questoes_do_texto(self.especialidade_id, self.texto, self.tipo, self.qtd)
        self.terminado.emit(questoes)

# -------------------- Janela Principal --------------------
class PainelGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Provas")
        self.resize(700, 600)
        layout = QVBoxLayout()

        # -------------------- Botões Usuários --------------------
        self.btn_usuarios = QPushButton("Listar Usuários")
        self.btn_usuarios.clicked.connect(self.listar_usuarios)
        layout.addWidget(self.btn_usuarios)

        self.btn_especialidades = QPushButton("Listar Especialidades")
        self.btn_especialidades.clicked.connect(self.listar_especialidades)
        layout.addWidget(self.btn_especialidades)

        # -------------------- Seleção de PDF --------------------
        self.btn_pdf = QPushButton("Selecionar PDF")
        self.btn_pdf.clicked.connect(self.selecionar_pdf)
        layout.addWidget(self.btn_pdf)

        self.caminho_pdf_label = QLabel("Nenhum PDF selecionado")
        layout.addWidget(self.caminho_pdf_label)

        # -------------------- Configuração da Prova --------------------
        layout.addWidget(QLabel("Tipo de questão:"))
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["multipla", "dissertativa", "pratica"])
        layout.addWidget(self.tipo_combo)

        layout.addWidget(QLabel("Quantidade de questões:"))
        self.qtd_spin = QSpinBox()
        self.qtd_spin.setMinimum(1)
        self.qtd_spin.setMaximum(20)
        layout.addWidget(self.qtd_spin)

        layout.addWidget(QLabel("Especialidade:"))
        self.especialidade_combo = QComboBox()
        self.atualizar_combo_especialidades()
        layout.addWidget(self.especialidade_combo)

        self.btn_gerar = QPushButton("Gerar Prova")
        self.btn_gerar.clicked.connect(self.gerar_prova)
        layout.addWidget(self.btn_gerar)

        self.setLayout(layout)

    # -------------------- Funções --------------------
    def listar_usuarios(self):
        dados = []
        for u in UsuarioController.listar_usuarios():
            dados.append([u.id, u.nome, u.email, u.criado_em])
        dialog = TabelaDialog("Usuários", dados, ["ID", "Nome", "Email", "Criado em"])
        dialog.exec_()

    def listar_especialidades(self):
        dados = []
        for e in EspecialidadeController.listar_especialidades():
            dados.append([e.id, e.codigo, e.nome, e.criado_em])
        dialog = TabelaDialog("Especialidades", dados, ["ID", "Código", "Nome", "Criado em"])
        dialog.exec_()

    def atualizar_combo_especialidades(self):
        self.especialidade_combo.clear()
        for e in EspecialidadeController.listar_especialidades():
            self.especialidade_combo.addItem(f"{e.nome} ({e.id})", e.id)

    def selecionar_pdf(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Selecione o PDF", "Data/Input/", "PDF Files (*.pdf)")
        if caminho:
            self.caminho_pdf_label.setText(caminho)
            self.texto_extraido = extrair_texto_pdf(caminho)
            print("[LOG] PDF carregado e texto extraído.")

    def gerar_prova(self):
        if not hasattr(self, "texto_extraido") or not self.texto_extraido.strip():
            print("[LOG] Nenhum PDF selecionado ou PDF vazio.")
            return

        texto = self.texto_extraido
        tipo = self.tipo_combo.currentText()
        qtd = self.qtd_spin.value()
        especialidade_id = self.especialidade_combo.currentData()

        # Janela de progresso
        self.progress_dialog = QDialog(self)
        self.progress_dialog.setWindowTitle("Gerando questões...")
        self.progress_dialog.resize(400, 100)
        layout = QVBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(qtd)
        layout.addWidget(QLabel("Gerando questões via IA..."))
        layout.addWidget(self.progress_bar)
        self.progress_dialog.setLayout(layout)
        self.progress_dialog.show()

        # Thread de geração
        self.thread = GerarQuestaoThread(especialidade_id, texto, tipo, qtd)
        self.thread.terminado.connect(self.finalizar_geracao)
        self.thread.start()

    def finalizar_geracao(self, questoes):
        self.progress_dialog.close()
        if questoes:
            usuario_id = 1  # Ajuste conforme o usuário logado
            especialidade_id = questoes[0].especialidade_id
            prova = gerar_prova_completa(usuario_id, especialidade_id, questoes)
            print(f"[LOG] Prova gerada com {len(questoes)} questões. PDF: {prova.arquivo_pdf}")
        else:
            print("[LOG] Nenhuma questão foi gerada.")

# -------------------- Executar --------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    painel = PainelGUI()
    painel.show()
    sys.exit(app.exec_())
