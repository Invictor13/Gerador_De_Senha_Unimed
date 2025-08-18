# -*- coding: utf-8 -*-
"""
Módulo de Componentes da UI

Este arquivo define as classes para os componentes de interface,
como as abas de geração de senha e frase-senha.
"""

import tkinter as tk
import customtkinter
from tkinter import scrolledtext
import os

from src.config import CONFIG
from src.ui.utils import Tooltip

# 5. CLASSES DE INTERFACE (COMPONENTES DA UI)
# Cada classe representa uma parte da UI, tornando o código mais limpo.

class AdvancedPasswordOptionsWindow(customtkinter.CTkToplevel):
    """Janela Toplevel para configurações avançadas de senha."""
    def __init__(self, parent, app_controller):
        super().__init__(parent)
        self.app = app_controller

        self.title("Opções Avançadas")
        self.geometry("400x450")
        self.transient(parent)
        self.grab_set()

        self.create_widgets()

    def create_widgets(self):
        """Cria os widgets de configuração na janela."""
        main_frame = customtkinter.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Frame de Opções ---
        opcoes_frame = customtkinter.CTkFrame(main_frame)
        opcoes_frame.pack(fill="x", pady=10, expand=True)

        self.comprimento_label = customtkinter.CTkLabel(opcoes_frame, text=f"Comprimento: {self.app.vars['comprimento_var'].get()}")
        self.comprimento_label.pack(anchor="w", padx=10, pady=(5,0))

        customtkinter.CTkSlider(opcoes_frame, from_=8, to=64, variable=self.app.vars['comprimento_var'], command=lambda v: self.comprimento_label.configure(text=f"Comprimento: {int(v)}")).pack(fill="x", pady=(0, 10), padx=10)

        customtkinter.CTkCheckBox(opcoes_frame, text="Incluir Letras Maiúsculas (A-Z)", variable=self.app.vars['incluir_maiusculas']).pack(anchor="w", pady=2, padx=10)
        customtkinter.CTkCheckBox(opcoes_frame, text="Incluir Letras Minúsculas (a-z)", variable=self.app.vars['incluir_minusculas']).pack(anchor="w", pady=2, padx=10)
        customtkinter.CTkCheckBox(opcoes_frame, text="Incluir Números (0-9)", variable=self.app.vars['incluir_numeros']).pack(anchor="w", pady=2, padx=10)

        especiais_check = customtkinter.CTkCheckBox(opcoes_frame, text="Incluir Caracteres Especiais", variable=self.app.vars['incluir_especiais'])
        especiais_check.pack(anchor="w", pady=2, padx=10)

        especiais_frame = customtkinter.CTkFrame(opcoes_frame, fg_color="transparent")
        especiais_frame.pack(fill="x", padx=(30,10))
        customtkinter.CTkEntry(especiais_frame, textvariable=self.app.vars['caracteres_especiais_var']).pack(fill="x")

        cb_ambiguos = customtkinter.CTkCheckBox(opcoes_frame, text="Excluir Caracteres Ambíguos", variable=self.app.vars['excluir_ambiguos'])
        cb_ambiguos.pack(anchor="w", pady=(10,5), padx=10)

        # --- Botão de Fechar ---
        unimed_color = CONFIG["CORES"]["VERDE_UNIMED"]
        close_button = customtkinter.CTkButton(main_frame, text="Fechar", command=self.destroy, fg_color=unimed_color, hover_color=unimed_color)
        close_button.pack(pady=(10,0), side="bottom")


class PasswordTab(customtkinter.CTkFrame):
    """Aba para geração de senhas tradicionais."""
    def __init__(self, parent, app_controller):
        super().__init__(parent, fg_color="transparent")
        self.app = app_controller
        self.advanced_options_window = None
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Configuração do grid principal da aba
        self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(0, weight=1) # Senha
        # self.grid_rowconfigure(1, weight=0) # Status
        # self.grid_rowconfigure(2, weight=0) # Barra de Entropia
        # self.grid_rowconfigure(3, weight=1) # Painel de Ações

        # --- 1. Senha em Destaque ---
        senha_font_config = ("Consolas", 24, "bold")
        self.senha_entry = customtkinter.CTkEntry(
            self,
            textvariable=self.app.vars["senha_gerada"],
            font=senha_font_config,
            justify="center"
        )
        self.senha_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=20, ipady=10)

        # --- 2. Banner de Status ---
        self.status_frame = customtkinter.CTkFrame(self, fg_color="transparent", corner_radius=6)
        self.status_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.status_label = customtkinter.CTkLabel(self.status_frame, text="Status da Senha", font=customtkinter.CTkFont(weight="bold", size=14))
        self.status_label.pack(expand=True, fill="both")

        # --- Barra de Entropia ---
        self.entropy_bar = customtkinter.CTkProgressBar(self, height=15, corner_radius=8)
        self.entropy_bar.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        self.entropy_bar.set(0)

        # --- Frame de Informações (Histórico e Entropia Label) ---
        info_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        info_frame.grid(row=3, column=0, sticky="ew", padx=10)
        info_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_columnconfigure(1, weight=1)

        self.history_menu = customtkinter.CTkComboBox(info_frame, values=[], state="readonly", width=120, command=self.app.on_history_select)
        self.history_menu.set("Histórico")
        self.history_menu.grid(row=0, column=0, sticky="w")

        self.entropy_label = customtkinter.CTkLabel(info_frame, text="Entropia: 0.00 bits", anchor="e")
        self.entropy_label.grid(row=0, column=1, sticky="e")


        # --- 3. Painel de Ação Unificado ---
        action_panel = customtkinter.CTkFrame(self, fg_color="transparent")
        action_panel.grid(row=4, column=0, sticky="ew", pady=(10, 0))
        action_panel.grid_columnconfigure((0, 1, 2), weight=1) # Três colunas de larguras iguais

        unimed_color = CONFIG["CORES"]["VERDE_UNIMED"]
        hover_color = CONFIG["CORES"]["VERDE_HOVER"]

        # Botão Gerar
        self.gerar_senha_btn = customtkinter.CTkButton(
            action_panel,
            text="GERAR NOVA SENHA",
            command=self.generate_password,
            cursor="hand2",
            height=40,
            font=customtkinter.CTkFont(weight="bold"),
            fg_color=unimed_color,
            hover_color=hover_color
        )
        self.gerar_senha_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        # Botão Copiar
        self.copiar_btn = customtkinter.CTkButton(
            action_panel,
            text="Copiar",
            command=lambda: self.app.copy_to_clipboard(self.app.vars["senha_gerada"].get(), self.copiar_btn),
            cursor="hand2",
            height=40,
            fg_color=unimed_color,
            hover_color=hover_color
        )
        self.copiar_btn.grid(row=0, column=1, sticky="ew", padx=5)

        # Botão Opções Avançadas
        advanced_options_btn = customtkinter.CTkButton(
            action_panel,
            text="Opções Avançadas",
            command=self.open_advanced_options,
            height=40,
            fg_color=unimed_color,
            hover_color=hover_color
        )
        advanced_options_btn.grid(row=0, column=2, sticky="ew", padx=(5, 0))

    def open_advanced_options(self):
        """Abre a janela de opções avançadas."""
        if self.advanced_options_window is None or not self.advanced_options_window.winfo_exists():
            self.advanced_options_window = AdvancedPasswordOptionsWindow(self, self.app)
        self.advanced_options_window.focus()

    def generate_password(self):
        self.app.animate_generation(
            button=self.gerar_senha_btn,
            target_var=self.app.vars["senha_gerada"],
            length=self.app.vars["comprimento_var"].get(),
            final_callback=self.app.finalize_password_generation
        )

class PassphraseTab(customtkinter.CTkFrame):
    """Aba para geração de frases-senha."""
    def __init__(self, parent, app_controller):
        super().__init__(parent, fg_color="transparent")
        self.app = app_controller
        self.wordlists = {} # Mapeia nome amigável para caminho do arquivo
        self.pack(fill="both", expand=True)

        self._load_wordlist_options()
        self.create_widgets()
        self.on_wordlist_select() # Garante estado inicial correto

    def _load_wordlist_options(self):
        """Carrega as opções de wordlist do diretório de assets."""
        self.wordlists.clear()
        # Mapeamento de nome de arquivo para nome de exibição amigável
        friendly_names = {
            "portugues_basico.txt": "Português (Básico)",
            "ingles_basico.txt": "Inglês (Básico)",
            "animais_pt_br.txt": "Animais (PT-BR)"
        }
        try:
            script_dir = os.path.dirname(__file__)
            wordlists_path = os.path.abspath(os.path.join(script_dir, '..', 'assets', 'wordlists'))

            if os.path.exists(wordlists_path):
                for filename in os.listdir(wordlists_path):
                    if filename.endswith(".txt"):
                        display_name = friendly_names.get(filename, filename)
                        self.wordlists[display_name] = os.path.join(wordlists_path, filename)
        except Exception as e:
            # Em caso de erro, não quebra a aplicação
            print(f"Erro ao carregar as wordlists: {e}")

        self.wordlists["Personalizado..."] = None # Adiciona a opção personalizada


    def create_widgets(self):
        # --- Frame de Resultado ---
        resultado_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        resultado_frame.pack(fill="x", pady=5)

        frase_font_config = CONFIG["FONTES"]["SENHA"]
        self.frase_entry = customtkinter.CTkEntry(resultado_frame, textvariable=self.app.vars["frase_gerada"], font=customtkinter.CTkFont(family=frase_font_config[0], size=frase_font_config[1], weight=frase_font_config[2]), justify="center")
        self.frase_entry.pack(side="left", fill="x", expand=True, ipady=5)

        unimed_color = CONFIG["CORES"]["VERDE_UNIMED"]
        self.copiar_btn = customtkinter.CTkButton(resultado_frame, text="Copiar", command=lambda: self.app.copy_to_clipboard(self.app.vars["frase_gerada"].get(), self.copiar_btn), cursor="hand2", fg_color=unimed_color, hover_color=unimed_color)
        self.copiar_btn.pack(side="right", padx=(10, 0))

        self.entropy_label = customtkinter.CTkLabel(self, text="Entropia: 0 bits", anchor="center")
        self.entropy_label.pack(fill="x", pady=5)

        # --- Frame de Opções ---
        opcoes_frame = customtkinter.CTkFrame(self)
        opcoes_frame.pack(fill="both", expand=True, pady=10)

        # --- Linha 1: Fonte das Palavras ---
        selecao_lista_frame = customtkinter.CTkFrame(opcoes_frame, fg_color="transparent")
        selecao_lista_frame.pack(fill="x", pady=5, padx=10)
        customtkinter.CTkLabel(selecao_lista_frame, text="Fonte das Palavras:").pack(side="left")
        self.wordlist_combo = customtkinter.CTkComboBox(selecao_lista_frame, variable=self.app.vars['lista_palavras_selecionada_var'], values=list(self.wordlists.keys()), state="readonly", command=self.on_wordlist_select)
        self.wordlist_combo.pack(side="right", fill="x", expand=True, padx=(10,0))

        # --- Linha 2: Número de Palavras e Separador ---
        config_line_frame = customtkinter.CTkFrame(opcoes_frame, fg_color="transparent")
        config_line_frame.pack(fill="x", pady=5, padx=10)

        customtkinter.CTkLabel(config_line_frame, text="Nº de Palavras:").pack(side="left")
        customtkinter.CTkOptionMenu(config_line_frame, variable=self.app.vars['num_palavras_var'], values=[str(i) for i in range(3,11)], width=70).pack(side="left", padx=(5,20))

        customtkinter.CTkLabel(config_line_frame, text="Separador:").pack(side="left")
        customtkinter.CTkEntry(config_line_frame, textvariable=self.app.vars['separador_var'], width=70).pack(side="left", padx=(5,0))

        # --- Área de Texto para Lista de Palavras ---
        self.wordlist_text = scrolledtext.ScrolledText(opcoes_frame, height=8, wrap=tk.WORD, font=CONFIG["FONTES"]["PRINCIPAL"], relief="solid", borderwidth=1)
        self.wordlist_text.pack(fill="both", expand=True, pady=(5,0), padx=10)

        # --- Botão de Gerar ---
        unimed_color = CONFIG["CORES"]["VERDE_UNIMED"]
        self.gerar_frase_btn = customtkinter.CTkButton(self, text="GERAR NOVA FRASE", command=self.generate_passphrase, cursor="hand2", height=40, font=customtkinter.CTkFont(weight="bold"), fg_color=unimed_color, hover_color=unimed_color)
        self.gerar_frase_btn.pack(fill="x", ipady=5, pady=(10,0))

    def generate_passphrase(self):
        self.app.animate_generation(
            button=self.gerar_frase_btn,
            target_var=self.app.vars["frase_gerada"],
            length=10, # Placeholder for animation
            final_callback=self.app.finalize_passphrase_generation
        )

    def on_wordlist_select(self, event=None):
        """Lida com a seleção de uma nova wordlist, carregando-a do arquivo."""
        selection = self.app.vars['lista_palavras_selecionada_var'].get()
        filepath = self.wordlists.get(selection)

        self.wordlist_text.config(state="normal")
        self.wordlist_text.delete("1.0", tk.END)

        word_string = ""
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    word_string = f.read()
            except Exception as e:
                word_string = f"Erro ao ler o arquivo:\n{e}"

        self.wordlist_text.insert("1.0", word_string.replace(" ", "\n"))

        if selection != "Personalizado...":
            self.wordlist_text.config(state="disabled")
        else:
            # Tooltip(self.wordlist_text, "Cole sua lista de palavras aqui, uma por linha.")
            pass
