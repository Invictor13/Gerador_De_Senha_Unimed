# -*- coding: utf-8 -*-
"""
Módulo da Aba Analisador de Senha (UI)
"""

import customtkinter as ctk
from src.logic import PasswordValidator

class AnalyzerTab(ctk.CTkFrame):
    """
    Aba que permite ao usuário analisar a força de uma senha.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.validator = PasswordValidator()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._create_widgets()
        self._bind_events()

    def _create_widgets(self):
        """Cria os widgets da aba."""
        # --- Frame de Entrada ---
        entry_frame = ctk.CTkFrame(self)
        entry_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        entry_frame.grid_columnconfigure(0, weight=1)

        self.password_entry = ctk.CTkEntry(
            entry_frame,
            placeholder_text="Digite a senha para analisar...",
            show="*"
        )
        self.password_entry.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="ew")

        self.reveal_checkbox = ctk.CTkCheckBox(
            entry_frame,
            text="Revelar Senha",
            command=self._toggle_password_visibility
        )
        self.reveal_checkbox.grid(row=0, column=1, padx=10, pady=10)

        # --- Frame de Critérios ---
        criteria_frame = ctk.CTkFrame(self, fg_color="transparent")
        criteria_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        criteria_frame.grid_columnconfigure(0, weight=1)

        self.criteria_labels = {
            "length_ok": self._create_criterion_label(criteria_frame, "Pelo menos 10 caracteres"),
            "case_ok": self._create_criterion_label(criteria_frame, "Letras maiúsculas e minúsculas"),
            "has_number": self._create_criterion_label(criteria_frame, "Inclusão de números (0-9)"),
            "has_symbol": self._create_criterion_label(criteria_frame, "Inclusão de símbolos (!@#$)"),
            "no_common_names": self._create_criterion_label(criteria_frame, "Não contém nomes comuns (ex: 'unimed')")
        }

        # Posiciona os labels no grid
        for i, label in enumerate(self.criteria_labels.values()):
            label.grid(row=i, column=0, padx=5, pady=2, sticky="w")

    def _create_criterion_label(self, parent, text):
        """Cria um label para um critério de validação."""
        label = ctk.CTkLabel(
            parent,
            text=f"❌ {text}",
            text_color="red"
        )
        return label

    def _toggle_password_visibility(self):
        """Alterna a visibilidade da senha no campo de entrada."""
        if self.reveal_checkbox.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def _bind_events(self):
        """Vincula os eventos aos widgets."""
        self.password_entry.bind("<KeyRelease>", self._on_key_release)

    def _on_key_release(self, event=None):
        """
        Callback para o evento de liberação de tecla.
        Analisa a senha e atualiza a UI.
        """
        password = self.password_entry.get()
        results = self.validator.analyze(password)

        for key, is_valid in results.items():
            label = self.criteria_labels[key]
            if is_valid:
                original_text = label.cget("text")[2:] # Remove o ícone antigo
                label.configure(text=f"✔ {original_text}", text_color="green")
            else:
                original_text = label.cget("text")[2:] # Remove o ícone antigo
                label.configure(text=f"❌ {original_text}", text_color="red")
