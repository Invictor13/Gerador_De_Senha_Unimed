# -*- coding: utf-8 -*-
"""
Módulo Principal da Aplicação (UI)

Este arquivo define a classe principal da aplicação,
que herda de tk.Tk e gerencia a janela principal,
orquestrando todos os componentes e a lógica do programa.
"""

import os
import secrets
import string
import tkinter as tk
from tkinter import ttk

import pyperclip
from PIL import Image, ImageTk

from src.config import CONFIG
from src.logic import PasswordGenerator, SettingsManager
from src.ui.components import PassphraseTab, PasswordTab
from src.ui.utils import Tooltip, UnimedWordAnimator

# 6. CLASSE PRINCIPAL DA APLICAÇÃO
# Orquestra todos os componentes.

class UnimedPasswordGeneratorApp(tk.Tk):
    """Classe principal que constrói e gerencia a aplicação."""
    def __init__(self):
        super().__init__()

        # --- Inicialização de Módulos ---
        self.settings_manager = SettingsManager()
        self.password_generator = PasswordGenerator()
        self.settings = self.settings_manager.load_settings()
        self.password_history = []

        self.title("Gerador de Senhas e Frases - UNIMED (Refatorado)")

        # --- Configuração da Janela ---
        self.state('zoomed') # Inicia em tela cheia
        self.minsize(700, 650)   # Tamanho mínimo para evitar quebra de layout
        self.resizable(True, True) # Permite redimensionamento

        self.configure(bg=CONFIG["CORES"]["FUNDO"])
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self._init_vars()
        self._configure_styles()
        self.create_main_widgets()

        if self.vars["animacao_ativa"].get():
            # A animação precisa de um pequeno delay para obter o tamanho correto do canvas
            self.after(100, self.animator.start)

    def _init_vars(self):
        """Inicializa as variáveis do Tkinter com os valores das configurações."""
        self.vars = {
            "senha_gerada": tk.StringVar(value="Sua senha segura aqui..."),
            "frase_gerada": tk.StringVar(value="Sua frase segura aqui..."),
            "comprimento_var": tk.IntVar(value=self.settings["comprimento"]),
            "num_palavras_var": tk.IntVar(value=self.settings["num_palavras"]),
            "separador_var": tk.StringVar(value=self.settings["separador"]),
            "incluir_maiusculas": tk.BooleanVar(value=self.settings["incluir_maiusculas"]),
            "incluir_minusculas": tk.BooleanVar(value=self.settings["incluir_minusculas"]),
            "incluir_numeros": tk.BooleanVar(value=self.settings["incluir_numeros"]),
            "incluir_especiais": tk.BooleanVar(value=self.settings["incluir_especiais"]),
            "excluir_ambiguos": tk.BooleanVar(value=self.settings["excluir_ambiguos"]),
            "animacao_ativa": tk.BooleanVar(value=self.settings["animacao_ativa"]),
            "caracteres_especiais_var": tk.StringVar(value=self.settings["caracteres_especiais"]),
            "lista_palavras_selecionada_var": tk.StringVar(value=self.settings["lista_palavras_selecionada"])
        }

    def _configure_styles(self):
        """Configura a aparência de todos os widgets ttk."""
        style = ttk.Style(self)
        style.theme_use('clam')

        # Cores
        C = CONFIG["CORES"]
        F = CONFIG["FONTES"]

        style.configure(".", background=C["FRAME_PRINCIPAL"], foreground=C["TEXTO_PRINCIPAL"], font=F["PRINCIPAL"])
        style.configure("TFrame", background=C["FRAME_PRINCIPAL"])
        style.configure("TLabel", background=C["FRAME_PRINCIPAL"], foreground=C["TEXTO_PRINCIPAL"])
        style.configure("TCheckbutton", background=C["FRAME_PRINCIPAL"], foreground=C["TEXTO_PRINCIPAL"])
        style.map("TCheckbutton", background=[('active', C["FRAME_PRINCIPAL"])])
        style.configure("TLabelframe", background=C["FRAME_PRINCIPAL"], bordercolor="#CCCCCC")
        style.configure("TLabelframe.Label", background=C["FRAME_PRINCIPAL"], foreground=C["TEXTO_PRINCIPAL"], font=F["LABEL_FRAME"])
        style.configure("TEntry", fieldbackground=C["CAMPO_FUNDO"], foreground=C["TEXTO_CAMPO"], borderwidth=1, relief="solid")
        style.configure("TSpinbox", fieldbackground=C["CAMPO_FUNDO"], foreground=C["TEXTO_CAMPO"], arrowcolor=C["TEXTO_PRINCIPAL"], borderwidth=1, relief="solid")
        style.map("TSpinbox", background=[('active', C["FRAME_PRINCIPAL"]), ('!active', C["FRAME_PRINCIPAL"])])
        style.configure("TCombobox", fieldbackground=C["CAMPO_FUNDO"], foreground=C["TEXTO_CAMPO"], arrowcolor=C["TEXTO_PRINCIPAL"], borderwidth=0)
        style.configure("TNotebook", background=C["FRAME_PRINCIPAL"], borderwidth=0)
        style.configure("TNotebook.Tab", background="#E0E0E0", foreground=C["TEXTO_PRINCIPAL"], font=("Segoe UI", 9, "bold"), padding=[10, 5], borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", C["VERDE_PRIMARIO"])], foreground=[("selected", C["BOTAO_TEXTO"])])
        style.configure("TButton", background=C["VERDE_PRIMARIO"], foreground=C["BOTAO_TEXTO"], font=F["BOTAO"], padding=(8, 4), borderwidth=0)
        style.map("TButton", background=[('active', C["VERDE_HOVER"]), ('hover', C["VERDE_HOVER"])])
        style.configure("Gerar.TButton", font=F["BOTAO"], padding=(20, 10))

    def create_main_widgets(self):
        """Cria a estrutura principal da UI."""
        self.animation_canvas = tk.Canvas(self, bg=CONFIG["CORES"]["FUNDO"], highlightthickness=0)
        self.animation_canvas.place(relwidth=1, relheight=1)

        # Container para centralizar o conteúdo principal
        center_container = ttk.Frame(self, style="TFrame")
        center_container.configure(style="Blank.TFrame") # Estilo para ser transparente
        style = ttk.Style(self)
        style.configure("Blank.TFrame", background=CONFIG["CORES"]["FUNDO"])
        center_container.place(relx=0.5, rely=0.5, anchor="center")

        main_labelframe = ttk.LabelFrame(center_container, text=" Gerador de Senhas e Frases UNIMED ", style="Content.TLabelframe")
        main_labelframe.pack()

        content_frame = ttk.Frame(main_labelframe, padding=(30, 15))
        content_frame.pack(padx=10, pady=5) # Padding para não colar nas bordas

        self.header_label = tk.Label(content_frame, text="Gerador de Senhas", font=CONFIG["FONTES"]["CABECALHO"], bg=CONFIG["CORES"]["FRAME_PRINCIPAL"], fg=CONFIG["CORES"]["TEXTO_PRINCIPAL"])
        self.header_label.pack(pady=(0, 10))

        self.animator = UnimedWordAnimator(self.animation_canvas, self.header_label)

        try:
            # Constrói o caminho para o logo a partir da localização deste script
            script_dir = os.path.dirname(__file__)
            logo_path = os.path.abspath(os.path.join(script_dir, '..', '..', 'assets', 'logo.png'))
            img_aberta = Image.open(logo_path)
            img_redimensionada = img_aberta.resize((100, int(100 * img_aberta.size[1] / img_aberta.size[0])))
            self.logo_image = ImageTk.PhotoImage(img_redimensionada)
            logo_widget = tk.Label(content_frame, image=self.logo_image, bg=CONFIG["CORES"]["FRAME_PRINCIPAL"])
            logo_widget.pack(pady=(0, 20))
        except Exception:
            logo_widget = tk.Label(content_frame, text="UNIMED", font=("Segoe UI", 24, "bold"), bg=CONFIG["CORES"]["FRAME_PRINCIPAL"], fg=CONFIG["CORES"]["VERDE_PRIMARIO"])
            logo_widget.pack(pady=10)

        notebook = ttk.Notebook(content_frame)
        notebook.pack(expand=True, fill="both", pady=(0, 15))

        self.tab_senha = PasswordTab(notebook, self)
        self.tab_frase = PassphraseTab(notebook, self)

        notebook.add(self.tab_senha, text="SENHA")
        notebook.add(self.tab_frase, text="FRASE-SENHA")

        self.create_common_widgets(content_frame)

    def create_common_widgets(self, parent_frame):
        """Cria widgets comuns a toda a aplicação."""
        settings_frame = ttk.LabelFrame(parent_frame, text=" Configurações Gerais ", padding=10)
        settings_frame.pack(side="bottom", fill="x", pady=(10, 0))

        cb_animacao = ttk.Checkbutton(settings_frame, text="Ativar animação de fundo", variable=self.vars["animacao_ativa"], command=self.toggle_animation)
        cb_animacao.pack(anchor="w")
        Tooltip(cb_animacao, "Pode consumir mais CPU.")

    def animate_generation(self, button, target_var, length, final_callback):
        """Anima o campo de texto antes de mostrar o resultado final."""
        button.config(state="disabled")
        char_pool = string.ascii_letters + string.digits + string.punctuation

        def animate_step(steps_left):
            if steps_left > 0:
                if "frase" in str(target_var):
                    dots = "." * (4 - (steps_left % 4))
                    temp_text = f"Gerando{dots}"
                else:
                    temp_text = "".join(secrets.choice(char_pool) for _ in range(length))
                target_var.set(temp_text)
                self.after(50, lambda: animate_step(steps_left - 1))
            else:
                final_callback()
                button.config(state="normal")

        animate_step(10)

    def finalize_password_generation(self):
        """Chama o gerador e atualiza a UI com a nova senha."""
        senha, entropia = self.password_generator.generate(
            self.vars["comprimento_var"].get(), self.vars["incluir_maiusculas"].get(),
            self.vars["incluir_minusculas"].get(), self.vars["incluir_numeros"].get(),
            self.vars["incluir_especiais"].get(), self.vars["excluir_ambiguos"].get(),
            self.vars["caracteres_especiais_var"].get()
        )
        self.vars["senha_gerada"].set(senha)
        self.tab_senha.entropy_label.config(text=f"Entropia: {entropia:.2f} bits")
        self.update_history(senha)

    def finalize_passphrase_generation(self):
        """Chama o gerador e atualiza a UI com a nova frase-senha."""
        user_wordlist = self.tab_frase.wordlist_text.get("1.0", "end-1c").split()
        frase, entropia = self.password_generator.generate_passphrase(
            self.vars["num_palavras_var"].get(), self.vars["separador_var"].get(), user_wordlist
        )
        self.vars["frase_gerada"].set(frase)
        self.tab_frase.entropy_label.config(text=f"Entropia: {entropia:.2f} bits")

    def copy_to_clipboard(self, text, button):
        """Copia o texto para a área de transferência e dá feedback visual."""
        if text and "Sua" not in text and "Gerando" not in text and "Selecione" not in text:
            pyperclip.copy(text)
            original_text = button.cget("text")
            button.config(text="Copiado!", state="disabled")
            self.after(1500, lambda: button.config(text=original_text, state="normal"))

    def update_history(self, password):
        """Atualiza o histórico de senhas geradas."""
        if "Selecione" in password: return
        if password in self.password_history:
            self.password_history.remove(password)
        self.password_history.insert(0, password)
        self.password_history = self.password_history[:10]
        self.tab_senha.history_menu['values'] = self.password_history
        self.tab_senha.history_menu.set("Histórico")

    def on_history_select(self, event=None):
        """Lida com a seleção de uma senha do histórico."""
        selected_password = self.tab_senha.history_menu.get()
        if not selected_password: return
        self.vars["senha_gerada"].set(selected_password)
        entropia = self.password_generator.analyze_password(selected_password, self.vars["caracteres_especiais_var"].get())
        self.tab_senha.entropy_label.config(text=f"Entropia: {entropia:.2f} bits")

    def toggle_animation(self):
        """Ativa ou desativa a animação de fundo."""
        if self.vars["animacao_ativa"].get():
            self.animator.start()
        else:
            self.animator.stop()

    def on_closing(self):
        """Salva as configurações ao fechar a aplicação."""
        current_settings = {
            key: var.get() for key, var in self.vars.items() if key != "senha_gerada" and key != "frase_gerada"
        }
        self.settings_manager.save_settings(current_settings)
        self.destroy()
