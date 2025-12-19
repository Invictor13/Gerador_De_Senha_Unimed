# -*- coding: utf-8 -*-
"""
Editor de Captura de Tela (Screenshot Editor)

Este módulo fornece uma interface para edição rápida de imagens/capturas de tela,
permitindo anotações, destaques e ofuscação antes do compartilhamento.
"""

import math
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageColor, ImageEnhance
import textwrap

from src.config import CONFIG

class ScreenshotEditor(ctk.CTkToplevel):
    """
    Janela de edição de imagem com ferramentas de anotação.
    """

    # Ferramentas
    TOOL_NONE = "none"
    TOOL_CROP = "crop"
    TOOL_RECTANGLE = "rectangle"
    TOOL_SPOTLIGHT = "spotlight"
    TOOL_TEXT = "text"
    TOOL_ARROW = "arrow"

    def __init__(self, parent, image: Image.Image, on_save_callback=None):
        super().__init__(parent)
        self.title("Editor de Evidências - Unimed")
        self.geometry("1100x700")

        # Callbacks e Estado
        self.on_save_callback = on_save_callback
        self.original_image = image.convert("RGBA") # Mantém original para reset se necessário
        self.current_image = self.original_image.copy()
        self.display_image = None # Imagem redimensionada para o canvas (se implementado zoom/fit)

        self.current_tool = self.TOOL_NONE
        self.start_x = None
        self.start_y = None
        self.current_rect_id = None

        # Opções de Texto
        self.text_contrast_bg = tk.BooleanVar(value=True) # Checkbox "Fundo de Contraste"
        self.active_text_widget = None # Widget de texto flutuante atual
        self.active_text_frame = None

        self._setup_ui()
        self._refresh_canvas()

    def _setup_ui(self):
        """Configura a interface gráfica."""

        # 1. Área Principal (Canvas com Scrollbars se necessário, aqui simplificado)
        self.canvas_frame = ctk.CTkFrame(self, fg_color="#2b2b2b")
        self.canvas_frame.pack(fill="both", expand=True, padx=0, pady=0)

        self.canvas = tk.Canvas(self.canvas_frame, bg="#2b2b2b", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Bindings do Canvas
        self.canvas.bind("<ButtonPress-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

        # 2. Barra Superior (Opções da Ferramenta)
        self.top_bar = ctk.CTkFrame(self, height=40, fg_color="#1a1a1a")
        self.top_bar.pack(fill="x", side="top", before=self.canvas_frame)

        # Checkbox para Texto (só visível se Text Tool ativa, ou sempre visível)
        self.chk_contrast = ctk.CTkCheckBox(
            self.top_bar,
            text="Fundo de Contraste",
            variable=self.text_contrast_bg,
            font=ctk.CTkFont(size=12)
        )
        self.chk_contrast.pack(side="right", padx=20, pady=10)

        # 3. Rodapé (Toolbar)
        # Borda verde (#00995D) de 2px no topo do Footer
        self.footer_container = ctk.CTkFrame(self, fg_color="#00995D", height=2) # A borda é o frame container
        self.footer_container.pack(fill="x", side="bottom")

        self.footer = ctk.CTkFrame(self.footer_container, fg_color="#1a1a1a", height=80)
        self.footer.pack(fill="both", expand=True, pady=(2, 0)) # Padding top 2px para mostrar a cor do container

        self._create_toolbar_buttons()

    def _create_toolbar_buttons(self):
        """Cria os botões da toolbar com Ícones Unicode + Texto."""

        tools = [
            ("✂️ CORTE", self.TOOL_CROP),
            ("⬛ RETÂNGULO", self.TOOL_RECTANGLE),
            ("💡 HOLOFOTE", self.TOOL_SPOTLIGHT),
            ("A TEXTO", self.TOOL_TEXT),
            ("➔ SETA", self.TOOL_ARROW)
        ]

        self.buttons = {}

        # Container para centralizar botões
        button_container = ctk.CTkFrame(self.footer, fg_color="transparent")
        button_container.pack(pady=15)

        for text, tool_id in tools:
            btn = ctk.CTkButton(
                button_container,
                text=text,
                command=lambda t=tool_id: self.select_tool(t),
                width=110,
                height=40,
                fg_color="transparent",
                border_width=1,
                border_color="#444444",
                font=ctk.CTkFont(size=12, weight="bold")
            )
            btn.pack(side="left", padx=5)
            self.buttons[tool_id] = btn

        # Ação de Salvar/Concluir
        save_btn = ctk.CTkButton(
            button_container,
            text="💾 SALVAR",
            command=self.save_and_close,
            width=110,
            height=40,
            fg_color=CONFIG["CORES"].get("VERDE_UNIMED", "#00995D"),
            font=ctk.CTkFont(size=12, weight="bold")
        )
        save_btn.pack(side="left", padx=20)

    def select_tool(self, tool):
        """Seleciona a ferramenta ativa e atualiza visual dos botões."""
        self.current_tool = tool

        # Reset visual dos botões
        for t_id, btn in self.buttons.items():
            if t_id == tool:
                btn.configure(fg_color="#333333", border_color=CONFIG["CORES"].get("VERDE_UNIMED", "#00995D"))
            else:
                btn.configure(fg_color="transparent", border_color="#444444")

    def _refresh_canvas(self):
        """Atualiza a imagem exibida no Canvas."""
        self.tk_image = ImageTk.PhotoImage(self.current_image)
        # Ajusta tamanho do canvas se necessário
        self.canvas.config(width=self.current_image.width, height=self.current_image.height)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")

    # --- Eventos do Canvas ---

    def on_canvas_click(self, event):
        if self.active_text_frame:
            # Se clicar fora enquanto edita texto, finaliza edição anterior?
            # Por enquanto, vamos exigir que o usuário clique em "OK" no widget de texto.
            pass

        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        if self.current_tool == self.TOOL_TEXT:
            self.create_floating_text_input(event.x, event.y)

    def on_canvas_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)

        if self.current_tool in [self.TOOL_RECTANGLE, self.TOOL_CROP, self.TOOL_SPOTLIGHT]:
            if self.current_rect_id:
                self.canvas.delete(self.current_rect_id)

            outline = "red" if self.current_tool == self.TOOL_RECTANGLE else "yellow"
            if self.current_tool == self.TOOL_SPOTLIGHT: outline = "white"

            self.current_rect_id = self.canvas.create_rectangle(
                self.start_x, self.start_y, cur_x, cur_y,
                outline=outline, width=2, dash=(4, 4) if self.current_tool == self.TOOL_CROP else None
            )

        elif self.current_tool == self.TOOL_ARROW:
            if self.current_rect_id:
                self.canvas.delete(self.current_rect_id)
            self.current_rect_id = self.canvas.create_line(
                self.start_x, self.start_y, cur_x, cur_y,
                arrow=tk.LAST, fill="red", width=3
            )

    def on_canvas_release(self, event):
        if not self.start_x or not self.start_y: return

        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)

        if self.current_tool == self.TOOL_SPOTLIGHT:
            self.apply_spotlight(self.start_x, self.start_y, end_x, end_y)

        elif self.current_tool == self.TOOL_RECTANGLE:
            self.apply_rectangle(self.start_x, self.start_y, end_x, end_y)

        elif self.current_tool == self.TOOL_ARROW:
            self.apply_arrow(self.start_x, self.start_y, end_x, end_y)

        elif self.current_tool == self.TOOL_CROP:
            self.apply_crop(self.start_x, self.start_y, end_x, end_y)

        # Limpa o preview do canvas
        if self.current_rect_id:
            self.canvas.delete(self.current_rect_id)
            self.current_rect_id = None

        self.start_x = None
        self.start_y = None

    # --- Lógica das Ferramentas ---

    def apply_spotlight(self, x1, y1, x2, y2):
        """Aplica o efeito de Holofote: escurece tudo menos a seleção."""
        # Normaliza coordenadas
        x1, x2 = sorted([x1, x2])
        y1, y2 = sorted([y1, y2])

        # Cria layer preta semi-transparente
        overlay = Image.new('RGBA', self.current_image.size, (0, 0, 0, 150))

        # "Recorta" a área selecionada (torna transparente no overlay)
        draw = ImageDraw.Draw(overlay)
        # Desenha retângulo transparente com modo 'clear' (Pillow não tem Clear mode direto em draw.rectangle facilmente sem mask)
        # Melhor abordagem: Criar mascara.

        mask = Image.new('L', self.current_image.size, 150) # 150 de opacidade
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rectangle([x1, y1, x2, y2], fill=0) # 0 = totalmente transparente

        # Cria a imagem preta sólida
        black_layer = Image.new('RGBA', self.current_image.size, (0, 0, 0, 0))
        black_draw = ImageDraw.Draw(black_layer)
        black_draw.rectangle([0, 0, self.current_image.width, self.current_image.height], fill=(0,0,0))

        # Aplica o alpha da máscara na layer preta
        black_layer.putalpha(mask)

        # Compoe sobre a imagem atual
        self.current_image = Image.alpha_composite(self.current_image.convert("RGBA"), black_layer)
        self._refresh_canvas()

    def apply_rectangle(self, x1, y1, x2, y2):
        draw = ImageDraw.Draw(self.current_image)
        draw.rectangle([x1, y1, x2, y2], outline="red", width=4)
        self._refresh_canvas()

    def apply_crop(self, x1, y1, x2, y2):
        """Recorta a imagem para a área selecionada."""
        # Ordena coordenadas
        left = min(x1, x2)
        top = min(y1, y2)
        right = max(x1, x2)
        bottom = max(y1, y2)

        # Evita cortes de tamanho 0
        if right - left < 5 or bottom - top < 5:
            return

        self.current_image = self.current_image.crop((left, top, right, bottom))
        self._refresh_canvas()

    def apply_arrow(self, x1, y1, x2, y2):
        """Desenha uma seta com cabeça calculada geometricamente."""
        draw = ImageDraw.Draw(self.current_image)

        # Linha principal
        draw.line([x1, y1, x2, y2], fill="red", width=4)

        # Cálculo da cabeça da seta
        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_length = 20
        arrow_angle = math.pi / 6  # 30 graus

        # Pontos da cabeça
        # Ponto 1: (x2, y2) - já temos
        # Ponto 2: (x2 - len*cos(angle - arrow_angle), y2 - len*sin(angle - arrow_angle))
        # Ponto 3: (x2 - len*cos(angle + arrow_angle), y2 - len*sin(angle + arrow_angle))

        p1 = (x2, y2)
        p2 = (
            x2 - arrow_length * math.cos(angle - arrow_angle),
            y2 - arrow_length * math.sin(angle - arrow_angle)
        )
        p3 = (
            x2 - arrow_length * math.cos(angle + arrow_angle),
            y2 - arrow_length * math.sin(angle + arrow_angle)
        )

        # Desenha triângulo preenchido para a cabeça
        draw.polygon([p1, p2, p3], fill="red")

        self._refresh_canvas()

    # --- Ferramenta de Texto (Refatorada) ---

    def create_floating_text_input(self, x, y):
        """Cria widget de texto flutuante sobre o canvas."""
        if self.active_text_frame:
            self.active_text_frame.destroy()

        # Container para o Text + Botão OK
        self.active_text_frame = ctk.CTkFrame(self.canvas, fg_color="transparent")

        # Text Widget (suporta multiline)
        self.active_text_widget = ctk.CTkTextbox(
            self.active_text_frame,
            width=200,
            height=60,
            border_width=2,
            border_color=CONFIG["CORES"].get("VERDE_UNIMED", "#00995D")
        )
        self.active_text_widget.pack(side="top", fill="both", expand=True)
        self.active_text_widget.focus_set()

        # Botão OK
        btn_ok = ctk.CTkButton(
            self.active_text_frame,
            text="OK",
            width=200,
            height=20,
            command=lambda: self.finalize_text(x, y),
            fg_color=CONFIG["CORES"].get("VERDE_UNIMED", "#00995D")
        )
        btn_ok.pack(side="top", pady=2)

        # Posiciona no Canvas
        self.canvas.create_window(x, y, window=self.active_text_frame, anchor="nw")

    def finalize_text(self, x, y):
        """Desenha o texto na imagem e remove o widget."""
        if not self.active_text_widget: return

        text_content = self.active_text_widget.get("1.0", "end-1c").strip()
        if text_content:
            self.draw_text_on_image(x, y, text_content)

        self.active_text_frame.destroy()
        self.active_text_frame = None
        self.active_text_widget = None
        self._refresh_canvas()

    def draw_text_on_image(self, x, y, text):
        draw = ImageDraw.Draw(self.current_image)

        # Tenta carregar fonte, fallback para default
        font_size = 24
        font = None
        try:
            # Tenta fontes comuns no Linux/Windows
            possible_fonts = ["arial.ttf", "LiberationSans-Regular.ttf", "DejaVuSans.ttf", "segoeui.ttf"]
            for font_name in possible_fonts:
                try:
                    font = ImageFont.truetype(font_name, font_size)
                    break
                except IOError:
                    continue

            if not font:
                 font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()

        # Calcular tamanho do texto (multiline)
        lines = text.splitlines()

        # Necessário calcular bbox manualmente para background
        max_width = 0
        total_height = 0
        line_heights = []

        # Simulação simples de bbox
        dummy_draw = ImageDraw.Draw(Image.new("RGB", (1,1)))

        for line in lines:
            bbox = dummy_draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1] + 5 # +5 padding
            max_width = max(max_width, w)
            line_heights.append(h)
            total_height += h

        # Padding
        pad = 10

        if self.text_contrast_bg.get():
            # Desenha retângulo de fundo
            bg_x1 = x
            bg_y1 = y
            bg_x2 = x + max_width + (pad * 2)
            bg_y2 = y + total_height + (pad * 2)

            draw.rectangle([bg_x1, bg_y1, bg_x2, bg_y2], fill="white", outline="black")
            text_color = "black"
        else:
            # Sem fundo, usa cor de destaque
            text_color = "red"
            pad = 0

        current_y = y + pad
        for i, line in enumerate(lines):
            draw.text((x + pad, current_y), line, fill=text_color, font=font)
            current_y += line_heights[i]

    def save_and_close(self):
        """Salva a imagem e fecha."""
        if self.on_save_callback:
            self.on_save_callback(self.current_image)
        self.destroy()

if __name__ == "__main__":
    # Teste rápido
    root = ctk.CTk()
    root.withdraw()

    # Cria imagem dummy
    img = Image.new('RGB', (800, 600), color = 'gray')
    d = ImageDraw.Draw(img)
    d.rectangle([200, 200, 400, 400], fill="blue")

    def on_save(processed_img):
        processed_img.show()
        root.quit()

    editor = ScreenshotEditor(root, img, on_save_callback=on_save)
    root.mainloop()
