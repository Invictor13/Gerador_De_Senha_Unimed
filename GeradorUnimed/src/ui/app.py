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
import customtkinter

import pyperclip
from PIL import Image

from src.config import CONFIG
from src.logic import PasswordGenerator, SettingsManager, check_pwned
from src.ui.components import PassphraseTab, PasswordTab
from src.ui.utils import Tooltip, UnimedWordAnimator

# 6. CLASSE PRINCIPAL DA APLICAÇÃO
# Orquestra todos os componentes.

class UnimedPasswordGeneratorApp(customtkinter.CTk):
    """Classe principal que constrói e gerencia a aplicação."""
    def __init__(self):
        super().__init__()

        # --- Cálculo de Dimensões Proporcionais ---
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.frame_width = screen_width * 0.5
        self.frame_height = screen_height * 0.6

        # --- Inicialização de Módulos ---
        self.settings_manager = SettingsManager()
        self.password_generator = PasswordGenerator()
        self.settings = self.settings_manager.load_settings()
        self.password_history = []

        # --- Configuração do Tema ---
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        self.title("Gerador de Senhas e Frases - UNIMED (Refatorado)")

        # --- Configuração da Janela ---
        self.wm_state('zoomed') # Inicia maximizado
        self.bind("<Escape>", self.exit_fullscreen)

        self.minsize(700, 650)   # Tamanho mínimo para evitar quebra de layout
        self.resizable(True, True) # Permite redimensionamento

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self._init_vars()
        self.create_main_widgets()

        if self.vars["animacao_ativa"].get():
            # A animação precisa de um pequeno delay para obter o tamanho correto do canvas
            self.after(100, self.animator.start)

        # --- Eventos de Foco para Otimização ---
        self.bind("<FocusIn>", self.handle_focus_in)
        self.bind("<FocusOut>", self.handle_focus_out)

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

    def create_main_widgets(self):
        """Cria a estrutura principal da UI."""
        self.animation_canvas = customtkinter.CTkCanvas(self, highlightthickness=0)
        self.animation_canvas.place(relwidth=1, relheight=1)

        # --- Configuração do Grid Central ---
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Frame Principal com Tamanho Fixo e Proporcional ---
        main_labelframe = customtkinter.CTkFrame(self, corner_radius=10, width=self.frame_width, height=self.frame_height)
        main_labelframe.grid(row=0, column=0)

        # O frame interno agora controla o padding e o conteúdo, mas não o tamanho total
        content_frame = customtkinter.CTkFrame(main_labelframe, fg_color="transparent", corner_radius=10)
        content_frame.pack(padx=10, pady=5, ipadx=20, ipady=10, expand=True, fill="both")
        content_frame.grid_propagate(False) # Impede que os filhos alterem o tamanho do frame
        content_frame.grid_rowconfigure(2, weight=1) # Permite que o notebook expanda
        content_frame.grid_columnconfigure(0, weight=1)


        header_font_config = CONFIG["FONTES"]["CABECALHO"]
        self.header_label = customtkinter.CTkLabel(content_frame, text="Gerador de Senhas", font=customtkinter.CTkFont(family=header_font_config[0], size=header_font_config[1], weight=header_font_config[2]))
        self.header_label.grid(row=0, column=0, pady=(0, 10))

        self.animator = UnimedWordAnimator(self.animation_canvas, self.header_label)

        try:
            # Constrói o caminho para o logo a partir da localização deste script
            script_dir = os.path.dirname(__file__)
            logo_path = os.path.abspath(os.path.join(script_dir, '..', '..', 'assets', 'logo.png'))
            img_aberta = Image.open(logo_path)
            self.logo_image = customtkinter.CTkImage(light_image=img_aberta, dark_image=img_aberta, size=(100, int(100 * img_aberta.size[1] / img_aberta.size[0])))
            logo_widget = customtkinter.CTkLabel(content_frame, image=self.logo_image, text="")
            logo_widget.grid(row=1, column=0, pady=(0, 20))
        except Exception:
            logo_widget = customtkinter.CTkLabel(content_frame, text="UNIMED", font=customtkinter.CTkFont(size=24, weight="bold"))
            logo_widget.grid(row=1, column=0, pady=10)

        # --- Abas ---
        notebook = customtkinter.CTkTabview(content_frame)
        notebook.grid(row=2, column=0, sticky="nsew", pady=(0, 15))

        senha_tab = notebook.add("SENHA")
        frase_tab = notebook.add("FRASE-SENHA")

        # Força as abas a terem a mesma altura mínima
        # A altura é um valor empírico para acomodar a aba de Frase-Senha que é maior
        senha_tab.configure(height=350)
        frase_tab.configure(height=350)

        self.tab_senha = PasswordTab(senha_tab, self)
        self.tab_frase = PassphraseTab(frase_tab, self)

        self.create_common_widgets(content_frame)

    def create_common_widgets(self, parent_frame):
        """Cria widgets comuns a toda a aplicação."""
        settings_frame = customtkinter.CTkFrame(parent_frame, fg_color="transparent")
        settings_frame.grid(row=3, column=0, sticky="ew", pady=(10, 0))

        cb_animacao = customtkinter.CTkCheckBox(settings_frame, text="Ativar animação de fundo", variable=self.vars["animacao_ativa"], command=self.toggle_animation)
        cb_animacao.pack(anchor="w")
        # Tooltip(cb_animacao, "Pode consumir mais CPU.") # Tooltip needs to be adapted for CTk

    def animate_generation(self, button, target_var, length, final_callback):
        """Anima o campo de texto antes de mostrar o resultado final."""
        button.configure(state="disabled")
        # Reset security seal before generating a new password
        if "senha" in str(target_var):
            self.tab_senha.status_frame.configure(fg_color="transparent")
            self.tab_senha.status_label.configure(text="Verificando...")

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
                button.configure(state="normal")

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

        # --- Verificação de Vazamento ---
        is_pwned = check_pwned(senha)
        if is_pwned:
            self.tab_senha.status_frame.configure(fg_color="red")
            self.tab_senha.status_label.configure(text="ALERTA: SENHA VAZADA!")
        else:
            self.tab_senha.status_frame.configure(fg_color="green")
            self.tab_senha.status_label.configure(text="SENHA SEGURA")


        # --- Lógica da Barra de Entropia ---
        max_entropy = 128.0
        normalized_entropy = min(entropia / max_entropy, 1.0)

        self.tab_senha.entropy_bar.set(normalized_entropy)

        if entropia < 40:
            color = "#FF4141" # Vermelho
        elif entropia < 80:
            color = "#FFDB58" # Amarelo
        else:
            color = "#00A34D" # Verde

        self.tab_senha.entropy_bar.configure(progress_color=color)
        self.tab_senha.entropy_label.configure(text=f"Entropia: {entropia:.2f} bits")
        self.update_history(senha)


    def finalize_passphrase_generation(self):
        """Chama o gerador e atualiza a UI com a nova frase-senha."""
        user_wordlist = self.tab_frase.wordlist_text.get("1.0", "end-1c").split()
        frase, entropia = self.password_generator.generate_passphrase(
            self.vars["num_palavras_var"].get(), self.vars["separador_var"].get(), user_wordlist
        )
        self.vars["frase_gerada"].set(frase)
        self.tab_frase.entropy_label.configure(text=f"Entropia: {entropia:.2f} bits")

    def copy_to_clipboard(self, text, button):
        """Copia o texto para a área de transferência e dá feedback visual."""
        if text and "Sua" not in text and "Gerando" not in text and "Selecione" not in text:
            pyperclip.copy(text)
            original_text = button.cget("text")
            button.configure(text="Copiado!", state="disabled")
            self.after(1500, lambda: button.configure(text=original_text, state="normal"))

    def update_history(self, password):
        """Atualiza o histórico de senhas geradas."""
        if "Selecione" in password: return
        if password in self.password_history:
            self.password_history.remove(password)
        self.password_history.insert(0, password)
        self.password_history = self.password_history[:10]
        self.tab_senha.history_menu.configure(values=self.password_history)
        self.tab_senha.history_menu.set("Histórico")

    def on_history_select(self, choice):
        """Lida com a seleção de uma senha do histórico."""
        self.vars["senha_gerada"].set(choice)
        entropia = self.password_generator.analyze_password(choice, self.vars["caracteres_especiais_var"].get())

        # --- Lógica da Barra de Entropia (Repetida para o Histórico) ---
        max_entropy = 128.0
        normalized_entropy = min(entropia / max_entropy, 1.0)
        self.tab_senha.entropy_bar.set(normalized_entropy)

        if entropia < 40:
            color = "#FF4141"
        elif entropia < 80:
            color = "#FFDB58"
        else:
            color = "#00A34D"

        self.tab_senha.entropy_bar.configure(progress_color=color)
        self.tab_senha.entropy_label.configure(text=f"Entropia: {entropia:.2f} bits")


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

    def handle_focus_in(self, event):
        """Reinicia a animação quando a janela ganha foco."""
        if self.vars["animacao_ativa"].get():
            self.animator.start()

    def handle_focus_out(self, event):
        """Pausa a animação quando a janela perde foco para economizar CPU."""
        self.animator.stop()

    def exit_fullscreen(self, event=None):
        """Sai do modo de tela cheia."""
        self.attributes('-fullscreen', False)
