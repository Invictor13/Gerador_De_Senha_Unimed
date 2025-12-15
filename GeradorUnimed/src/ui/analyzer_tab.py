# -*- coding: utf-8 -*-
"""
Módulo da Aba Analisador de Senha (UI)
"""

import customtkinter as ctk
from src.logic import PasswordValidator
from src.config import CONFIG

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

        # Garante que o frame principal da aba se expanda para preencher o espaço
        self.pack(expand=True, fill="both")

    def _create_widgets(self):
        """Cria os widgets da aba."""
        # --- Frame de Entrada ---
        entry_frame = ctk.CTkFrame(self)
        entry_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        entry_frame.grid_columnconfigure(0, weight=1)

        self.password_entry = ctk.CTkEntry(
            entry_frame,
            placeholder_text="Digite a senha para analisar...",
            show="*",
            font=ctk.CTkFont(size=14)
        )
        self.password_entry.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="ew")

        self.reveal_checkbox = ctk.CTkCheckBox(
            entry_frame,
            text="Revelar Senha",
            command=self._toggle_password_visibility,
            font=ctk.CTkFont(size=14)
        )
        self.reveal_checkbox.grid(row=0, column=1, padx=10, pady=10)

        # Barra de Força da Senha
        self.strength_bar = ctk.CTkProgressBar(self, orientation="horizontal")
        self.strength_bar.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.strength_bar.set(0)
        self.strength_bar.configure(progress_color="red")

        # --- Frame de Critérios ---
        criteria_frame = ctk.CTkFrame(self, fg_color="transparent")
        criteria_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        criteria_frame.grid_columnconfigure(0, weight=1)

        # HIERARQUIA TIPOGRÁFICA: Título em negrito
        title_label = ctk.CTkLabel(
            criteria_frame,
            text="Critérios de Segurança",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=5, pady=(0, 10), sticky="w")

        self.criteria_labels = {
            "length_ok": self._create_criterion_label(criteria_frame, "Pelo menos 10 caracteres"),
            "case_ok": self._create_criterion_label(criteria_frame, "Letras maiúsculas e minúsculas"),
            "has_number": self._create_criterion_label(criteria_frame, "Inclusão de números (0-9)"),
            "has_symbol": self._create_criterion_label(criteria_frame, "Inclusão de símbolos (!@#$)"),
            "no_common_names": self._create_criterion_label(criteria_frame, "Não contém nomes comuns (ex: 'unimed')")
        }

        # Posiciona os labels no grid, começando da linha 1
        for i, label in enumerate(self.criteria_labels.values()):
            label.grid(row=i + 1, column=0, padx=5, pady=2, sticky="w")

    def _create_criterion_label(self, parent, text):
        """Cria um label para um critério de validação."""
        label = ctk.CTkLabel(
            parent,
            text=f"❌ {text}",
            text_color="red",
            font=ctk.CTkFont(size=14)
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

        score = 0
        total_criteria = len(results)

        for key, is_valid in results.items():
            label = self.criteria_labels[key]
            if is_valid:
                score += 1
                original_text = label.cget("text")[2:] # Remove o ícone antigo
                label.configure(text=f"✔ {original_text}", text_color="green")
            else:
                original_text = label.cget("text")[2:] # Remove o ícone antigo
                label.configure(text=f"❌ {original_text}", text_color="red")

        # Atualiza a barra de progresso
        if not password:
            self.strength_bar.set(0)
            self.strength_bar.configure(progress_color="red")
            return

        normalized_score = score / total_criteria
        self.strength_bar.set(normalized_score)

        if normalized_score < 0.4:
            self.strength_bar.configure(progress_color="red")
        elif normalized_score < 0.8:
            self.strength_bar.configure(progress_color="orange")
        else:
            self.strength_bar.configure(progress_color=CONFIG["CORES"]["VERDE_UNIMED"])
