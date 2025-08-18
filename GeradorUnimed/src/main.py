# -*- coding: utf-8 -*-
"""
Ponto de Entrada da Aplicação

Este script é o ponto de entrada principal para executar o Gerador de Senhas UNIMED.
Ele instancia e inicia a aplicação.
"""

from src.ui.app import UnimedPasswordGeneratorApp

# 7. PONTO DE ENTRADA (MAIN)
if __name__ == "__main__":
    app = UnimedPasswordGeneratorApp()
    app.mainloop()
