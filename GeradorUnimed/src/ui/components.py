# -*- coding: utf-8 -*-
"""
Módulo de Componentes da UI

Este arquivo define as classes para os componentes de interface,
como as abas de geração de senha e frase-senha.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext

from src.config import CONFIG
from src.ui.utils import Tooltip

# 5. CLASSES DE INTERFACE (COMPONENTES DA UI)
# Cada classe representa uma parte da UI, tornando o código mais limpo.

class PasswordTab(ttk.Frame):
    """Aba para geração de senhas tradicionais."""
    def __init__(self, parent, app_controller):
        super().__init__(parent, padding=10)
        self.app = app_controller
        self.create_widgets()

    def create_widgets(self):
        # --- Frame de Resultado ---
        resultado_frame = ttk.Frame(self)
        resultado_frame.pack(fill="x", pady=5)

        self.senha_entry = ttk.Entry(resultado_frame, textvariable=self.app.vars["senha_gerada"], font=CONFIG["FONTES"]["SENHA"], justify="center")
        self.senha_entry.pack(side="left", fill="x", expand=True, ipady=5)

        self.copiar_btn = ttk.Button(resultado_frame, text="Copiar", command=lambda: self.app.copy_to_clipboard(self.app.vars["senha_gerada"].get(), self.copiar_btn), cursor="hand2")
        self.copiar_btn.pack(side="right", padx=(10, 0))

        # --- Frame de Informações (Histórico e Entropia) ---
        info_frame = ttk.Frame(self)
        info_frame.pack(fill="x", pady=5)

        self.history_menu = ttk.Combobox(info_frame, values=[], state="readonly", width=15, font=CONFIG["FONTES"]["PRINCIPAL"])
        self.history_menu.set("Histórico")
        self.history_menu.pack(side="left")
        self.history_menu.bind("<<ComboboxSelected>>", self.app.on_history_select)

        self.entropy_label = ttk.Label(info_frame, text="Entropia: 0 bits", anchor="e")
        self.entropy_label.pack(side="right", fill="x", expand=True)

        # --- Frame de Opções ---
        opcoes_frame = ttk.LabelFrame(self, text=" Opções da Senha ", padding=15)
        opcoes_frame.pack(fill="x", pady=10, expand=True)

        self.comprimento_label = ttk.Label(opcoes_frame, text=f"Comprimento: {self.app.vars['comprimento_var'].get()}")
        self.comprimento_label.pack(anchor="w")

        ttk.Scale(opcoes_frame, from_=8, to_=64, orient="horizontal", variable=self.app.vars['comprimento_var'], command=lambda v: self.comprimento_label.config(text=f"Comprimento: {int(float(v))}")).pack(fill="x", pady=(5, 10))

        ttk.Checkbutton(opcoes_frame, text="Incluir Letras Maiúsculas (A-Z)", variable=self.app.vars['incluir_maiusculas']).pack(anchor="w", pady=1)
        ttk.Checkbutton(opcoes_frame, text="Incluir Letras Minúsculas (a-z)", variable=self.app.vars['incluir_minusculas']).pack(anchor="w", pady=1)
        ttk.Checkbutton(opcoes_frame, text="Incluir Números (0-9)", variable=self.app.vars['incluir_numeros']).pack(anchor="w", pady=1)
        ttk.Checkbutton(opcoes_frame, text="Incluir Caracteres Especiais", variable=self.app.vars['incluir_especiais']).pack(anchor="w", pady=1)

        especiais_frame = ttk.Frame(opcoes_frame)
        especiais_frame.pack(fill="x", padx=(20,0))
        ttk.Entry(especiais_frame, textvariable=self.app.vars['caracteres_especiais_var'], font=CONFIG["FONTES"]["PRINCIPAL"]).pack(fill="x")

        cb_ambiguos = ttk.Checkbutton(opcoes_frame, text="Excluir Caracteres Ambíguos", variable=self.app.vars['excluir_ambiguos'])
        cb_ambiguos.pack(anchor="w", pady=(10,0))
        Tooltip(cb_ambiguos, "Exclui: I, l, 1, O, 0, o")

        # --- Botão de Gerar ---
        self.gerar_senha_btn = ttk.Button(self, text="GERAR NOVA SENHA", command=self.generate_password, cursor="hand2", style="Gerar.TButton")
        self.gerar_senha_btn.pack(fill="x", ipady=5, pady=(10,0))

    def generate_password(self):
        self.app.animate_generation(
            button=self.gerar_senha_btn,
            target_var=self.app.vars["senha_gerada"],
            length=self.app.vars["comprimento_var"].get(),
            final_callback=self.app.finalize_password_generation
        )

class PassphraseTab(ttk.Frame):
    """Aba para geração de frases-senha."""
    def __init__(self, parent, app_controller):
        super().__init__(parent, padding=10)
        self.app = app_controller
        self.create_widgets()
        self.on_wordlist_select() # Initialize text area

    def create_widgets(self):
        # --- Frame de Resultado ---
        resultado_frame = ttk.Frame(self)
        resultado_frame.pack(fill="x", pady=5)

        self.frase_entry = ttk.Entry(resultado_frame, textvariable=self.app.vars["frase_gerada"], font=CONFIG["FONTES"]["SENHA"], justify="center")
        self.frase_entry.pack(side="left", fill="x", expand=True, ipady=5)

        self.copiar_btn = ttk.Button(resultado_frame, text="Copiar", command=lambda: self.app.copy_to_clipboard(self.app.vars["frase_gerada"].get(), self.copiar_btn), cursor="hand2")
        self.copiar_btn.pack(side="right", padx=(10, 0))

        self.entropy_label = ttk.Label(self, text="Entropia: 0 bits", anchor="center")
        self.entropy_label.pack(fill="x", pady=5)

        # --- Frame de Opções ---
        opcoes_frame = ttk.LabelFrame(self, text=" Opções da Frase-Senha ", padding=15)
        opcoes_frame.pack(fill="both", expand=True, pady=10)

        selecao_lista_frame = ttk.Frame(opcoes_frame)
        selecao_lista_frame.pack(fill="x", pady=5)
        ttk.Label(selecao_lista_frame, text="Fonte das Palavras:").pack(side="left")
        self.wordlist_combo = ttk.Combobox(selecao_lista_frame, textvariable=self.app.vars['lista_palavras_selecionada_var'], values=list(CONFIG["WORDLISTS"].keys()), state="readonly", font=CONFIG["FONTES"]["PRINCIPAL"])
        self.wordlist_combo.pack(side="right", fill="x", expand=True)
        self.wordlist_combo.bind("<<ComboboxSelected>>", self.on_wordlist_select)

        palavras_frame = ttk.Frame(opcoes_frame)
        palavras_frame.pack(fill="x", pady=5)
        ttk.Label(palavras_frame, text="Número de Palavras:").pack(side="left")
        ttk.Spinbox(palavras_frame, from_=3, to_=10, textvariable=self.app.vars['num_palavras_var'], width=5, font=CONFIG["FONTES"]["PRINCIPAL"]).pack(side="right")

        separador_frame = ttk.Frame(opcoes_frame)
        separador_frame.pack(fill="x", pady=5)
        ttk.Label(separador_frame, text="Caractere Separador:").pack(side="left")
        ttk.Entry(separador_frame, textvariable=self.app.vars['separador_var'], width=5, font=CONFIG["FONTES"]["PRINCIPAL"]).pack(side="right")

        self.wordlist_text = scrolledtext.ScrolledText(opcoes_frame, height=8, wrap=tk.WORD, font=CONFIG["FONTES"]["PRINCIPAL"], bg=CONFIG["CORES"]["CAMPO_FUNDO"], fg=CONFIG["CORES"]["TEXTO_CAMPO"], relief="solid", borderwidth=1)
        self.wordlist_text.pack(fill="both", expand=True, pady=(5,0))

        # --- Botão de Gerar ---
        self.gerar_frase_btn = ttk.Button(self, text="GERAR NOVA FRASE", command=self.generate_passphrase, cursor="hand2", style="Gerar.TButton")
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
            Tooltip(self.wordlist_text, "Cole sua lista de palavras aqui, uma por linha.")
