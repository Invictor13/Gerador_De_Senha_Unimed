# -*- coding: utf-8 -*-
"""
Módulo de Componentes da UI

Este arquivo define as classes para os componentes de interface,
como as abas de geração de senha e frase-senha.
"""

import tkinter as tk
import customtkinter
from tkinter import scrolledtext

from src.config import CONFIG
from src.ui.utils import Tooltip

# 5. CLASSES DE INTERFACE (COMPONENTES DA UI)
# Cada classe representa uma parte da UI, tornando o código mais limpo.

class PasswordTab(customtkinter.CTkFrame):
    """Aba para geração de senhas tradicionais."""
    def __init__(self, parent, app_controller):
        super().__init__(parent, fg_color="transparent")
        self.app = app_controller
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        # --- Frame de Resultado ---
        resultado_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        resultado_frame.pack(fill="x", pady=5)

        self.senha_entry = customtkinter.CTkEntry(resultado_frame, textvariable=self.app.vars["senha_gerada"], font=customtkinter.CTkFont(size=CONFIG["FONTES"]["TAMANHO_SENHA"]), justify="center")
        self.senha_entry.pack(side="left", fill="x", expand=True, ipady=5)

        self.copiar_btn = customtkinter.CTkButton(resultado_frame, text="Copiar", command=lambda: self.app.copy_to_clipboard(self.app.vars["senha_gerada"].get(), self.copiar_btn), cursor="hand2")
        self.copiar_btn.pack(side="right", padx=(10, 0))

        # --- Frame de Informações (Histórico e Entropia) ---
        info_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        info_frame.pack(fill="x", pady=5, expand=True)

        self.history_menu = customtkinter.CTkComboBox(info_frame, values=[], state="readonly", width=120, command=self.app.on_history_select)
        self.history_menu.set("Histórico")
        self.history_menu.pack(side="left")

        self.entropy_label = customtkinter.CTkLabel(info_frame, text="Entropia: 0.00 bits", anchor="e")
        self.entropy_label.pack(side="right", padx=(10, 0))

        # --- Barra de Entropia ---
        self.entropy_bar = customtkinter.CTkProgressBar(self, height=15, corner_radius=8)
        self.entropy_bar.pack(fill="x", pady=(5, 10), expand=True)
        self.entropy_bar.set(0) # Valor inicial

        # --- Frame de Opções ---
        opcoes_frame = customtkinter.CTkFrame(self)
        opcoes_frame.pack(fill="x", pady=10, expand=True)

        self.comprimento_label = customtkinter.CTkLabel(opcoes_frame, text=f"Comprimento: {self.app.vars['comprimento_var'].get()}")
        self.comprimento_label.pack(anchor="w", padx=10, pady=(5,0))

        customtkinter.CTkSlider(opcoes_frame, from_=8, to_=64, variable=self.app.vars['comprimento_var'], command=lambda v: self.comprimento_label.configure(text=f"Comprimento: {int(v)}")).pack(fill="x", pady=(0, 10), padx=10)

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
        # Tooltip(cb_ambiguos, "Exclui: I, l, 1, O, 0, o")

        # --- Botão de Gerar ---
        self.gerar_senha_btn = customtkinter.CTkButton(self, text="GERAR NOVA SENHA", command=self.generate_password, cursor="hand2", height=40, font=customtkinter.CTkFont(weight="bold"))
        self.gerar_senha_btn.pack(fill="x", ipady=5, pady=(10,0))

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
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.on_wordlist_select() # Initialize text area

    def create_widgets(self):
        # --- Frame de Resultado ---
        resultado_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        resultado_frame.pack(fill="x", pady=5)

        self.frase_entry = customtkinter.CTkEntry(resultado_frame, textvariable=self.app.vars["frase_gerada"], font=customtkinter.CTkFont(size=CONFIG["FONTES"]["TAMANHO_SENHA"]), justify="center")
        self.frase_entry.pack(side="left", fill="x", expand=True, ipady=5)

        self.copiar_btn = customtkinter.CTkButton(resultado_frame, text="Copiar", command=lambda: self.app.copy_to_clipboard(self.app.vars["frase_gerada"].get(), self.copiar_btn), cursor="hand2")
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
        self.wordlist_combo = customtkinter.CTkComboBox(selecao_lista_frame, variable=self.app.vars['lista_palavras_selecionada_var'], values=list(CONFIG["WORDLISTS"].keys()), state="readonly", command=self.on_wordlist_select)
        self.wordlist_combo.pack(side="right", fill="x", expand=True, padx=(10,0))

        # --- Linha 2: Número de Palavras e Separador ---
        config_line_frame = customtkinter.CTkFrame(opcoes_frame, fg_color="transparent")
        config_line_frame.pack(fill="x", pady=5, padx=10)

        customtkinter.CTkLabel(config_line_frame, text="Nº de Palavras:").pack(side="left")
        customtkinter.CTkOptionMenu(config_line_frame, variable=self.app.vars['num_palavras_var'], values=[str(i) for i in range(3,11)], width=70).pack(side="left", padx=(5,20))

        customtkinter.CTkLabel(config_line_frame, text="Separador:").pack(side="left")
        customtkinter.CTkEntry(config_line_frame, textvariable=self.app.vars['separador_var'], width=70).pack(side="left", padx=(5,0))

        # --- Área de Texto para Lista de Palavras ---
        self.wordlist_text = scrolledtext.ScrolledText(opcoes_frame, height=8, wrap=tk.WORD, font=(CONFIG["FONTES"]["FAMILIA"], CONFIG["FONTES"]["TAMANHO_PADRAO"]), relief="solid", borderwidth=1)
        self.wordlist_text.pack(fill="both", expand=True, pady=(5,0), padx=10)

        # --- Botão de Gerar ---
        self.gerar_frase_btn = customtkinter.CTkButton(self, text="GERAR NOVA FRASE", command=self.generate_passphrase, cursor="hand2", height=40, font=customtkinter.CTkFont(weight="bold"))
        self.gerar_frase_btn.pack(fill="x", ipady=5, pady=(10,0))

    def generate_passphrase(self):
        self.app.animate_generation(
            button=self.gerar_frase_btn,
            target_var=self.app.vars["frase_gerada"],
            length=10, # Placeholder for animation
            final_callback=self.app.finalize_passphrase_generation
        )

    def on_wordlist_select(self, event=None):
        selection = self.app.vars['lista_palavras_selecionada_var'].get()
        self.wordlist_text.config(state="normal")
        self.wordlist_text.delete("1.0", tk.END)
        word_string = CONFIG["WORDLISTS"].get(selection, "")
        self.wordlist_text.insert("1.0", word_string.replace(" ", "\n"))

        if selection != "Personalizado...":
            self.wordlist_text.config(state="disabled")
        else:
            # Tooltip(self.wordlist_text, "Cole sua lista de palavras aqui, uma por linha.")
            pass
