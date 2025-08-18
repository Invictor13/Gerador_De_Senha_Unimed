# -*- coding: utf-8 -*-
"""
Ponto de Entrada da Aplicação

Este script é o ponto de entrada principal para executar o Gerador de Senhas UNIMED.
Ele instancia e inicia a aplicação.
"""

import sys
import os
import tkinter as tk

# Adiciona o diretório do projeto (pai do 'src') ao sys.path
# Garante que 'from src...' funcione em qualquer ambiente
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_path)

from src.ui.app import UnimedPasswordGeneratorApp

# 7. PONTO DE ENTRADA (MAIN)
if __name__ == "__main__":
    try:
        app = UnimedPasswordGeneratorApp()
        app.mainloop()
    except tk.TclError as e:
        # Erro comum em ambientes sem GUI (headless), como em testes automatizados.
        if "no display name" in str(e):
            print("Aplicação não pode ser iniciada: ambiente sem display gráfico (headless).")
            # Em um cenário de teste, isso pode ser considerado um "sucesso" de inicialização.
        else:
            raise e # Lança outras exceções TclError
    except (KeyboardInterrupt):
        print("\nAplicação encerrada pelo usuário.")
