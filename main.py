import sys
import os
import shutil
from PyQt5.QtWidgets import QApplication
from Frontend.painel_gui import PainelGUI  # Importa a classe PainelGUI do arquivo painel.py

def apagar_pycache(raiz="."):
    """
    Percorre todas as pastas a partir de 'raiz' e apaga qualquer pasta __pycache__.
    """
    for dirpath, dirnames, _ in os.walk(raiz):
        if "__pycache__" in dirnames:
            pycache_path = os.path.join(dirpath, "__pycache__")
            try:
                shutil.rmtree(pycache_path)
                print(f"Apagado: {pycache_path}")
            except Exception as e:
                print(f"Erro ao apagar {pycache_path}: {e}")

if __name__ == "__main__":
    # Inicializa a aplicação PyQt5
    app = QApplication(sys.argv)
    # Cria a instância da janela principal
    painel = PainelGUI()  # PainelGUI agora será uma classe PyQt5 (QWidget)
    painel.show()
    
    # Executa a aplicação
    exit_code = app.exec_()

    # Após fechar a aplicação, apaga todos os __pycache__
    raiz_projeto = os.path.dirname(os.path.abspath(__file__))
    apagar_pycache(raiz_projeto)

    sys.exit(exit_code)