# -*- coding: utf-8 -*-
"""
Módulo de Configuração

Este arquivo centraliza todas as constantes do projeto,
como cores, fontes e configurações padrão, para fácil manutenção.
"""

# 2. MÓDULO DE CONFIGURAÇÃO (CONSTANTES)
# Agrupar constantes melhora a manutenção e a clareza do código.
CONFIG = {
    "CORES": {
        "VERDE_UNIMED": "#00995c",
        "FUNDO": "#0D0208", # Fundo quase preto para a animação
        "FRAME_PRINCIPAL": "#FFFFFF",
        "VERDE_PRIMARIO": "#00995c",
        "VERDE_HOVER": "#007a49",
        "VERDE_ANIMACAO_SCRAMBLE": "#004d26",
        "VERDE_ANIMACAO_FINAL": "#004d26",
        "BOTAO_TEXTO": "#ffffff",
        "TEXTO_PRINCIPAL": "#000000",
        "TEXTO_CAMPO": "#000000",
        "CAMPO_FUNDO": "#F0F0F0",
        "TOOLTIP_FUNDO": "#ffffe0",
        "BOTAO_COPIADO": "#007a49",
    },
    "FONTES": {
        "PRINCIPAL": ("Segoe UI", 10),
        "SENHA": ("Consolas", 16, "bold"),
        "BOTAO": ("Segoe UI", 10, "bold"),
        "CABECALHO": ("Segoe UI", 18, "bold"),
        "LABEL_FRAME": ("Segoe UI", 9, "bold"),
        "TOOLTIP": ("Segoe UI", 8, "normal"),
        "ANIMACAO": ("Consolas", 18, "bold"),
    },
    "DEFAULTS": {
        "comprimento": 16,
        "incluir_maiusculas": True,
        "incluir_minusculas": True,
        "incluir_numeros": True,
        "incluir_especiais": True,
        "excluir_ambiguos": False,
        "animacao_ativa": True,
        "caracteres_especiais": "!@#$%^&*",
        "num_palavras": 4,
        "separador": "-",
        "lista_palavras_selecionada": "Português (Básico)",
    }
}
