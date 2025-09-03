import sys
import os
import shutil
from Frontend.painel_gui import PainelGUI
from PyQt5.QtWidgets import QApplication

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
    app = QApplication(sys.argv)
    painel = PainelGUI()
    painel.show()
    
    # Executa a GUI
    exit_code = app.exec_()

    # Após fechar a aplicação, apaga todos os __pycache__
    raiz_projeto = os.path.dirname(os.path.abspath(__file__))
    apagar_pycache(raiz_projeto)

    sys.exit(exit_code)
