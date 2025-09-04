import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

from Backend.Services.questao_service import gerar_questoes_do_texto
from Backend.Services.prova_service import gerar_prova_completa
from Backend.Services.pdf_generator import extrair_texto_pdf


class PainelGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Geração de Provas")
        self.root.geometry("900x600")

        self.pdf_path = None
        self.texto_extraido = ""

        # Frame superior (seleção de PDF e botões principais)
        frame_top = tk.Frame(root, padx=10, pady=10)
        frame_top.pack(fill="x")

        btn_pdf = tk.Button(frame_top, text="Selecionar PDF", command=self.selecionar_pdf)
        btn_pdf.pack(side="left", padx=5)

        btn_gerar = tk.Button(frame_top, text="Gerar Prova", command=self.gerar_prova)
        btn_gerar.pack(side="left", padx=5)

        btn_sair = tk.Button(frame_top, text="Sair", command=self.root.quit, fg="red")
        btn_sair.pack(side="right", padx=5)

        # Frame para parâmetros da prova
        frame_params = tk.Frame(root, padx=10, pady=10)
        frame_params.pack(fill="x")

        tk.Label(frame_params, text="Usuário ID:").grid(row=0, column=0, sticky="w")
        self.usuario_entry = tk.Entry(frame_params)
        self.usuario_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame_params, text="Especialidade ID:").grid(row=0, column=2, sticky="w")
        self.especialidade_entry = tk.Entry(frame_params)
        self.especialidade_entry.grid(row=0, column=3, padx=5)

        tk.Label(frame_params, text="Tipo de Questão:").grid(row=1, column=0, sticky="w")
        self.tipo_combo = ttk.Combobox(frame_params, values=["objetiva", "dissertativa", "pratica"])
        self.tipo_combo.grid(row=1, column=1, padx=5)
        self.tipo_combo.current(0)

        tk.Label(frame_params, text="Quantidade de Questões:").grid(row=1, column=2, sticky="w")
        self.qtd_spin = tk.Spinbox(frame_params, from_=1, to=50, width=5)
        self.qtd_spin.grid(row=1, column=3, padx=5)

        # Frame para exibir texto do PDF
        frame_texto = tk.LabelFrame(root, text="Texto do PDF", padx=10, pady=10)
        frame_texto.pack(fill="both", expand=True, padx=10, pady=10)

        self.text_box = tk.Text(frame_texto, wrap="word", state="disabled")
        self.text_box.pack(fill="both", expand=True)

    def selecionar_pdf(self):
        """Seleciona um PDF e extrai o texto automaticamente."""
        file_path = filedialog.askopenfilename(
            title="Selecione um arquivo PDF",
            filetypes=[("Arquivos PDF", "*.pdf")]
        )
        if not file_path:
            return

        self.pdf_path = file_path
        try:
            self.texto_extraido = extrair_texto_pdf(file_path)
            self._atualizar_texto_box(self.texto_extraido)
            messagebox.showinfo("Sucesso", "Texto do PDF extraído com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao extrair texto do PDF:\n{e}")

    def gerar_prova(self):
        """Gera a prova a partir do texto extraído do PDF."""
        if not self.texto_extraido.strip():
            messagebox.showwarning("Aviso", "Nenhum texto foi extraído do PDF.")
            return

        try:
            usuario_id = int(self.usuario_entry.get())
            especialidade_id = int(self.especialidade_entry.get())
            tipo = self.tipo_combo.get()
            qtd = int(self.qtd_spin.get())

            questoes = []
            for i in range(qtd):
                q = gerar_questoes_do_texto(especialidade_id, self.texto_extraido, tipo, qtd=1)
                questoes.extend(q)
                print(f"[LOG] Questão {i+1} gerada")

            prova = gerar_prova_completa(usuario_id, especialidade_id, questoes)
            messagebox.showinfo("Sucesso", f"Prova gerada com sucesso!\nArquivo: {prova.arquivo_pdf}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar a prova:\n{e}")

    def _atualizar_texto_box(self, texto):
        """Atualiza a caixa de texto do PDF exibido."""
        self.text_box.config(state="normal")
        self.text_box.delete("1.0", tk.END)
        self.text_box.insert(tk.END, texto)
        self.text_box.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = PainelGUI(root)
    root.mainloop()
