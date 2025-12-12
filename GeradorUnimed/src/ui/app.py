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
from src.logic import PasswordGenerator, SettingsManager, check_pwned, PasswordValidator
from src.ui.analyzer_tab import AnalyzerTab
from src.ui.components import PassphraseTab, PasswordTab, AdvancedPasswordOptionsWindow
from src.ui.utils import Tooltip, UnimedWordAnimator

# 6. CLASSE PRINCIPAL DA APLICAÇÃO
# Orquestra todos os componentes.

class UnimedPasswordGeneratorApp(customtkinter.CTk):
    """Classe principal que constrói e gerencia a aplicação."""
    def __init__(self):
        super().__init__()

        # --- Inicialização de Módulos ---
        self.settings_manager = SettingsManager()
        self.password_generator = PasswordGenerator()
        self.settings = self.settings_manager.load_settings()
        self.password_history = []
        self.advanced_options_window = None


        # --- Configuração do Tema e Janela ---
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        self.title("Gerador de Senhas - Unimed")
        self.configure(bg="black") # FUNDAÇÃO: Fundo preto

        # GARANTIA DE JANELA MAXIMIZADA
        self.geometry("1280x720")

        # O DECRETO DE MAXIMIZAÇÃO (SOLUÇÃO FINAL)
        # Garante que a maximização ocorra após a janela estar pronta.
        self.after(100, lambda: self.wm_state('zoomed'))

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
        self.animation_canvas = customtkinter.CTkCanvas(self, bg="black", highlightthickness=0)
        self.animation_canvas.place(relwidth=1, relheight=1)

        # --- Configuração do Grid Central ---
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- EFEITO DE SOMBRA (3D) ---
        # 1. O frame externo "sombra" é ligeiramente maior e mais escuro
        shadow_frame = customtkinter.CTkFrame(self, fg_color="#1a1a1a", corner_radius=10)
        shadow_frame.grid(row=0, column=0)

        # 2. O frame interno "conteúdo" tem a cor padrão e um pequeno padding
        content_frame = customtkinter.CTkFrame(shadow_frame, corner_radius=10)
        content_frame.grid(row=0, column=0, padx=2, pady=2)
        content_frame.grid_columnconfigure(0, weight=1)

        # O SISTEMA DE ESPAÇAMENTO RÍTMICO
        # Linha 1 (Conteúdo da Aba / Notebook) terá o maior peso para ocupar o espaço.
        content_frame.grid_rowconfigure(1, weight=1)

        # --- Linha 0: CABEÇALHO ---
        self.header_label = customtkinter.CTkLabel(
            content_frame,
            text="Gerador de Senhas - Unimed",
            font=customtkinter.CTkFont(size=24, weight="bold")
        )
        self.header_label.grid(row=0, column=0, pady=(20, 10))

        # O Animator agora usa o canvas preto e o novo header
        self.animator = UnimedWordAnimator(self.animation_canvas, self.header_label)

        # --- Linha 1: ABAS (NOTEBOOK) ---
        # Esta linha (1) tem weight=1 para expandir verticalmente.
        notebook = customtkinter.CTkTabview(content_frame, width=550, height=450)
        notebook.grid(row=1, column=0, sticky="nsew", pady=10)
        # ESTABILIDADE ABSOLUTA: Impede o notebook de redimensionar com o conteúdo das abas
        notebook.grid_propagate(False)

        senha_tab = notebook.add("  SENHA  ")
        frase_tab = notebook.add("  FRASE-SENHA  ")
        analyzer_tab = notebook.add("  ANALISADOR  ")

        self.tab_senha = PasswordTab(senha_tab, self)
        self.tab_frase = PassphraseTab(frase_tab, self)
        self.tab_analyzer = AnalyzerTab(analyzer_tab)

        self.create_footer(content_frame)

    def create_footer(self, parent_frame):
        """Cria o rodapé com o botão de configurações."""
        # No grid do content_frame, esta é a linha 2.
        footer_frame = customtkinter.CTkFrame(parent_frame, fg_color="transparent")
        footer_frame.grid(row=2, column=0, sticky="ew", pady=(10, 20), padx=16)
        footer_frame.grid_columnconfigure(0, weight=1) # Centraliza o conteúdo do rodapé

        # Frame interno para agrupar o label e o botão
        inner_footer_frame = customtkinter.CTkFrame(footer_frame, fg_color="transparent")
        inner_footer_frame.grid(row=0, column=0)

        author_label = customtkinter.CTkLabel(
            inner_footer_frame,
            text="Desenvolvido por Victor Viana",
            font=customtkinter.CTkFont(size=14, weight="bold"),
            text_color="gray70"
        )
        author_label.grid(row=0, column=0, sticky="e", padx=(0, 8))

        try:
            script_dir = os.path.dirname(__file__)
            icon_path = os.path.abspath(os.path.join(script_dir, '..', 'assets', 'gear_icon.png'))
            gear_image_pil = Image.open(icon_path)
            self.gear_image = customtkinter.CTkImage(light_image=gear_image_pil, dark_image=gear_image_pil, size=(24, 24))

            settings_button = customtkinter.CTkButton(
                inner_footer_frame,
                text="",
                image=self.gear_image,
                fg_color="transparent",
                width=24,
                height=24,
                command=self.open_advanced_options
            )
            settings_button.grid(row=0, column=1, sticky="w")
            Tooltip(settings_button, "Opções Avançadas")
        except FileNotFoundError:
            settings_button = customtkinter.CTkButton(
                inner_footer_frame,
                text="Opções",
                command=self.open_advanced_options,
                font=customtkinter.CTkFont(size=14)
            )
            settings_button.grid(row=0, column=1, sticky="w")
            Tooltip(settings_button, "Configurações e Preferências")

    def open_advanced_options(self):
        """Abre a janela de opções avançadas."""
        if self.advanced_options_window is None or not self.advanced_options_window.winfo_exists():
            self.advanced_options_window = AdvancedPasswordOptionsWindow(self, self)
        self.advanced_options_window.focus()

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


        # A lógica da barra de entropia foi removida do novo design.
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

        # A lógica da barra de entropia foi removida do novo design.
        # A verificação de pwned também pode ser acionada aqui, se desejado.
        is_pwned = check_pwned(choice)
        if is_pwned:
            self.tab_senha.status_frame.configure(fg_color="red")
            self.tab_senha.status_label.configure(text="ALERTA: SENHA VAZADA!")
        else:
            self.tab_senha.status_frame.configure(fg_color="green")
            self.tab_senha.status_label.configure(text="SENHA SEGURA")


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
