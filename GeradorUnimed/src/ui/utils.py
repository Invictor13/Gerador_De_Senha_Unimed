# -*- coding: utf-8 -*-
"""
Módulo de Utilitários da UI

Este arquivo contém classes auxiliares que fornecem funcionalidades
específicas para a interface, como tooltips e as animações de fundo.
"""

import math
import random
import tkinter as tk
import customtkinter

from src.config import CONFIG

# 4. CLASSES DE UTILITÁRIOS (HELPERS)
# Classes auxiliares para funcionalidades específicas da UI.

class Tooltip:
    """Cria uma dica de ajuda (tooltip) para um widget."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = customtkinter.CTkLabel(self.tooltip_window, text=self.text, justify='left',
                         fg_color=CONFIG["CORES"]["TOOLTIP_FUNDO"], corner_radius=5)
        label.pack(ipadx=1)

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
        self.tooltip_window = None

class AnimatedWord:
    """Representa a palavra 'UNIMED' que aparece e se anima na tela."""
    def __init__(self, canvas):
        self.canvas = canvas
        self.word = "UNIMED"
        self.chars = "日ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍ01"
        self.font = (CONFIG["FONTES"]["FAMILIA"], CONFIG["FONTES"]["TAMANHO_ANIMACAO"])
        self.font_size = self.font[1]
        self.symbols = []
        self.state = "hidden"  # States: hidden, scrambling, visible
        self.cycle_counter = 0
        self._create_symbols()
        self.reset()

    def _create_symbols(self):
        """Cria os objetos de texto uma única vez para reutilização."""
        for _ in self.word:
            symbol = self.canvas.create_text(-100, -100, font=self.font, anchor="n")
            self.symbols.append(symbol)

    def reset(self):
        """Move a palavra para uma nova posição e prepara para animar."""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width < 100 or height < 100: # Evita erro se a janela for muito pequena
            self.hide()
            return

        x = random.randint(self.font_size * 2, width - (self.font_size * 2))
        y = random.randint(self.font_size, height - (self.font_size * (len(self.word) + 2)))

        self.state = "scrambling"
        self.cycle_counter = 0

        for i, symbol_id in enumerate(self.symbols):
            self.canvas.moveto(symbol_id, x, y + (i * self.font_size))
            self.canvas.itemconfig(symbol_id, fill=CONFIG["CORES"]["VERDE_ANIMACAO_SCRAMBLE"])

    def hide(self):
        """Move os símbolos para fora da tela."""
        for symbol_id in self.symbols:
            self.canvas.moveto(symbol_id, -100, -100)
        self.state = "hidden"

    def animate(self):
        """Controla o ciclo de vida da animação da palavra."""
        if self.state == "hidden":
            # Aumentada a chance de reaparecer a cada ciclo
            if random.random() < 0.05:
                self.reset()
            return

        self.cycle_counter += 1

        if self.state == "scrambling":
            # Anima as letras aleatoriamente
            for symbol_id in self.symbols:
                self.canvas.itemconfig(symbol_id, text=random.choice(self.chars))

            # Após alguns ciclos, revela a palavra final
            if self.cycle_counter > random.randint(8, 15):
                self.state = "visible"
                self.cycle_counter = 0
                for i, symbol_id in enumerate(self.symbols):
                    self.canvas.itemconfig(symbol_id, text=self.word[i], fill=CONFIG["CORES"]["VERDE_ANIMACAO_FINAL"])

        elif self.state == "visible":
            # Permanece visível por um tempo, depois some (tempo reduzido)
            if self.cycle_counter > random.randint(20, 40):
                self.hide()

class UnimedWordAnimator:
    """Controla a animação de fundo de forma otimizada."""
    def __init__(self, canvas, header_label):
        self.canvas = canvas
        self.header_label = header_label
        self.is_running = False
        self.words = []
        self.title_animation_step = 0

    def start(self):
        if not self.is_running:
            self.is_running = True
            # Cria um número fixo de palavras para animar
            if not self.words:
                for _ in range(12): # Aumentado para 12 palavras na tela
                    self.words.append(AnimatedWord(self.canvas))
            self.animate()

    def stop(self):
        self.is_running = False
        for word in self.words:
            for symbol_id in word.symbols:
                self.canvas.delete(symbol_id)
        self.words.clear()

    def animate(self):
        if not self.is_running: return

        # Animação do título principal
        self.title_animation_step += 0.05
        pulse = (math.sin(self.title_animation_step) + 1) / 2
        new_color = self.fade_color("#FFFFFF", CONFIG["CORES"]["VERDE_PRIMARIO"], pulse)
        self.header_label.configure(text_color=new_color)

        # Anima cada palavra
        for word in self.words:
            word.animate()

        # Taxa de atualização mais lenta para baixo consumo de CPU
        self.canvas.after(100, self.animate)

    def fade_color(self, start_hex, end_hex, fraction):
        start_rgb = tuple(int(start_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        end_rgb = tuple(int(end_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        new_rgb = [int(start_rgb[i] + (end_rgb[i] - start_rgb[i]) * fraction) for i in range(3)]
        return f"#{new_rgb[0]:02x}{new_rgb[1]:02x}{new_rgb[2]:02x}"
