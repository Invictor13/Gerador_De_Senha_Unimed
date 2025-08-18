# -*- coding: utf-8 -*-
"""
____________________________________________________
        Gerador de Senhas e Frases - UNIMED
      (Versão Refatorada e Otimizada por Codium)
____________________________________________________

  Script originalmente criado por Victor Ladislau Viana,
  agora reestruturado para máxima clareza, modularidade e performance.

  Estrutura do Arquivo:
  1.  Importações de Bibliotecas
  2.  Módulo de Configuração (Cores, Fontes, Padrões)
  3.  Classes de Lógica (Backend)
  4.  Classes de Utilitários (Helpers)
  5.  Classes de Interface (Componentes da UI)
  6.  Classe Principal da Aplicação
  7.  Ponto de Entrada (Main)
"""

# 1. IMPORTAÇÕES DE BIBLIOTECAS
import tkinter as tk
from tkinter import ttk, scrolledtext
import secrets
import string
import pyperclip
import random
import math
import json
import os
from PIL import Image, ImageTk

# 2. MÓDULO DE CONFIGURAÇÃO (CONSTANTES)
# Agrupar constantes melhora a manutenção e a clareza do código.
CONFIG = {
    "CORES": {
        "FUNDO": "#0D0208", # Fundo quase preto para a animação
        "FRAME_PRINCIPAL": "#FFFFFF",
        "VERDE_PRIMARIO": "#00995c",
        "VERDE_HOVER": "#007a49",
        "VERDE_ANIMACAO_SCRAMBLE": "#00A34D",
        "VERDE_ANIMACAO_FINAL": "#E0FBFC",
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
    },
    "WORDLISTS": {
        "Português (Básico)": "abril amigo amor azul barco bom bola casa ceu cor dedo dez dia doce dois festa flor fogo folha gato gelo hoje ideia jogo lago lapis leve livro luz mae mar mato mel mesa mes mil mundo musica nao noite nome novo olho ontem ouro pai pao par paz pedra peixe pena pe piso planta ponte porta pote praia prato quatro quem quer raiz rei rio risada roda rosa rua sal seis sempre sete sim sol som sorte sul tempo terra teste tres tudo um uma verde vermelho vez vida vinho zero",
        "Inglês (Básico)": "apple friend love blue boat good ball house sky color finger ten day sweet two party flower fire leaf cat ice today idea game lake pencil light book sun mother sea honey table month world music no night name new eye gold father bread pair peace stone fish pen foot floor plant bridge door pot beach dish four who want root king river laugh wheel rose street salt six always seven yes sun sound luck south time earth test three all one green red time life wine zero",
        "Animais (PT-BR)": "abelha aguia aranha avestruz baleia barata boi borboleta burro cabra cachorro camelo canguru capivara carneiro cavalo cobra coelho coruja crocodilo dinossauro elefante escorpiao foca formiga frango furao galinha galo gamba ganso garca gato gaviao girafa golfinho gorila grao grilo guaxinim hiena hipopotamo iacare iguana jabuti jacare jaguar javali jiboia joaninha lagarta lagartixa lagosta leao lebre leopardo lesma lhama lobo lula macaco mariposa marisco marreco mico minhoca morcego mosca mosquito ovelha panda pantera papagaio passaro pato pavao peixe perereca peru pica-pau pinguim piolho pombo polvo porco pulga quati ra raposa ratazana rato rena rinoceronte sabiá sagui sapo sardinha serpente siri tamandua tatu tartaruga texugo tigre toupeira touro urso urubu vaca vespa zebra",
        "Personalizado...": ""
    }
}

# 3. CLASSES DE LÓGICA (BACKEND)
# Responsáveis pela lógica de negócio, sem interação com a UI.

class SettingsManager:
    """Gerencia o carregamento e salvamento das configurações em um arquivo JSON."""
    def __init__(self, filename="config.json"):
        self.filename = filename
        self.defaults = CONFIG["DEFAULTS"]

    def load_settings(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    settings = self.defaults.copy()
                    settings.update(json.load(f))
                    return settings
            except (json.JSONDecodeError, IOError):
                return self.defaults
        return self.defaults

    def save_settings(self, settings):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4)
        except IOError as e:
            print(f"Erro ao salvar configurações: {e}")

class PasswordGenerator:
    """Gera e analisa senhas e frases-senha."""
    CARACTERES_AMBIGUOS = "Il1O0o"

    def analyze_password(self, password, special_chars_pool):
        """Calcula a entropia de uma senha em bits."""
        pool = 0
        if any(c.islower() for c in password): pool += 26
        if any(c.isupper() for c in password): pool += 26
        if any(c.isdigit() for c in password): pool += 10
        if any(c in special_chars_pool for c in password): pool += len(special_chars_pool)
        if pool == 0: return 0
        return len(password) * math.log2(pool)

    def generate(self, length, use_upper, use_lower, use_digits, use_special, exclude_ambiguous, special_chars):
        """Gera uma senha aleatória baseada nos critérios fornecidos."""
        alphabet, guaranteed_chars = "", []
        if use_upper: alphabet += string.ascii_uppercase; guaranteed_chars.append(secrets.choice(string.ascii_uppercase))
        if use_lower: alphabet += string.ascii_lowercase; guaranteed_chars.append(secrets.choice(string.ascii_lowercase))
        if use_digits: alphabet += string.digits; guaranteed_chars.append(secrets.choice(string.digits))
        if use_special and special_chars: alphabet += special_chars; guaranteed_chars.append(secrets.choice(special_chars))

        if exclude_ambiguous:
            alphabet = "".join(c for c in alphabet if c not in self.CARACTERES_AMBIGUOS)
            guaranteed_chars = [c for c in guaranteed_chars if c not in self.CARACTERES_AMBIGUOS]

        if not alphabet: return "Selecione uma opção!", 0

        remaining_length = length - len(guaranteed_chars)
        if remaining_length < 0:
            remaining_length = 0
            guaranteed_chars = guaranteed_chars[:length]

        remaining_chars = [secrets.choice(alphabet) for _ in range(remaining_length)]
        password_list = guaranteed_chars + remaining_chars
        secrets.SystemRandom().shuffle(password_list)
        final_password = "".join(password_list)
        entropy = len(final_password) * math.log2(len(alphabet)) if alphabet else 0
        return final_password, entropy

    def generate_passphrase(self, num_words, separator, wordlist):
        """Gera uma frase-senha a partir de uma lista de palavras."""
        if not wordlist: return "A lista de palavras está vazia!", 0
        try:
            chosen_words = [secrets.choice(wordlist) for _ in range(num_words)]
            passphrase = separator.join(chosen_words)
            entropy = num_words * math.log2(len(wordlist))
            return passphrase, entropy
        except IndexError:
            return "Lista de palavras vazia!", 0

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
        label = tk.Label(self.tooltip_window, text=self.text, justify='left',
                         background=CONFIG["CORES"]["TOOLTIP_FUNDO"], relief='solid', borderwidth=1,
                         font=CONFIG["FONTES"]["TOOLTIP"])
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
        self.font = CONFIG["FONTES"]["ANIMACAO"]
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
        self.header_label.config(fg=new_color)

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

# 6. CLASSE PRINCIPAL DA APLICAÇÃO
# Orquestra todos os componentes.

class UnimedPasswordGeneratorApp(tk.Tk):
    """Classe principal que constrói e gerencia a aplicação."""
    def __init__(self):
        super().__init__()
        
        # --- Inicialização de Módulos ---
        self.settings_manager = SettingsManager()
        self.password_generator = PasswordGenerator()
        self.settings = self.settings_manager.load_settings()
        self.password_history = []
        
        self.title("Gerador de Senhas e Frases - UNIMED (Refatorado)")
        
        # --- Configuração da Janela ---
        self.state('zoomed') # Inicia em tela cheia
        self.minsize(700, 650)   # Tamanho mínimo para evitar quebra de layout
        self.resizable(True, True) # Permite redimensionamento
        
        self.configure(bg=CONFIG["CORES"]["FUNDO"])
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self._init_vars()
        self._configure_styles()
        self.create_main_widgets()
        
        if self.vars["animacao_ativa"].get():
            # A animação precisa de um pequeno delay para obter o tamanho correto do canvas
            self.after(100, self.animator.start)

    def _init_vars(self):
        """Inicializa as variáveis do Tkinter com os valores das configurações."""
        self.vars = {
            "senha_gerada": tk.StringVar(value="Sua senha segura aqui..."),
            "frase_gerada": tk.StringVar(value="Sua frase segura aqui..."),
            "comprimento_var": tk.IntVar(value=self.settings["comprimento"]),
            "num_palavras_var": tk.IntVar(value=self.settings["num_palavras"]),
            "separador_var": tk.StringVar(value=self.settings["separador"]),
            "incluir_maiusculas": tk.BooleanVar(value=self.settings["incluir_maiusculas"]),
            "incluir_minusculas": tk.BooleanVar(value=self.settings["incluir_minusculas"]),
            "incluir_numeros": tk.BooleanVar(value=self.settings["incluir_numeros"]),
            "incluir_especiais": tk.BooleanVar(value=self.settings["incluir_especiais"]),
            "excluir_ambiguos": tk.BooleanVar(value=self.settings["excluir_ambiguos"]),
            "animacao_ativa": tk.BooleanVar(value=self.settings["animacao_ativa"]),
            "caracteres_especiais_var": tk.StringVar(value=self.settings["caracteres_especiais"]),
            "lista_palavras_selecionada_var": tk.StringVar(value=self.settings["lista_palavras_selecionada"])
        }
    
    def _configure_styles(self):
        """Configura a aparência de todos os widgets ttk."""
        style = ttk.Style(self)
        style.theme_use('clam')
        
        # Cores
        C = CONFIG["CORES"]
        F = CONFIG["FONTES"]
        
        style.configure(".", background=C["FRAME_PRINCIPAL"], foreground=C["TEXTO_PRINCIPAL"], font=F["PRINCIPAL"])
        style.configure("TFrame", background=C["FRAME_PRINCIPAL"])
        style.configure("TLabel", background=C["FRAME_PRINCIPAL"], foreground=C["TEXTO_PRINCIPAL"])
        style.configure("TCheckbutton", background=C["FRAME_PRINCIPAL"], foreground=C["TEXTO_PRINCIPAL"])
        style.map("TCheckbutton", background=[('active', C["FRAME_PRINCIPAL"])])
        style.configure("TLabelframe", background=C["FRAME_PRINCIPAL"], bordercolor="#CCCCCC")
        style.configure("TLabelframe.Label", background=C["FRAME_PRINCIPAL"], foreground=C["TEXTO_PRINCIPAL"], font=F["LABEL_FRAME"])
        style.configure("TEntry", fieldbackground=C["CAMPO_FUNDO"], foreground=C["TEXTO_CAMPO"], borderwidth=1, relief="solid")
        style.configure("TSpinbox", fieldbackground=C["CAMPO_FUNDO"], foreground=C["TEXTO_CAMPO"], arrowcolor=C["TEXTO_PRINCIPAL"], borderwidth=1, relief="solid")
        style.map("TSpinbox", background=[('active', C["FRAME_PRINCIPAL"]), ('!active', C["FRAME_PRINCIPAL"])])
        style.configure("TCombobox", fieldbackground=C["CAMPO_FUNDO"], foreground=C["TEXTO_CAMPO"], arrowcolor=C["TEXTO_PRINCIPAL"], borderwidth=0)
        style.configure("TNotebook", background=C["FRAME_PRINCIPAL"], borderwidth=0)
        style.configure("TNotebook.Tab", background="#E0E0E0", foreground=C["TEXTO_PRINCIPAL"], font=("Segoe UI", 9, "bold"), padding=[10, 5], borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", C["VERDE_PRIMARIO"])], foreground=[("selected", C["BOTAO_TEXTO"])])
        style.configure("TButton", background=C["VERDE_PRIMARIO"], foreground=C["BOTAO_TEXTO"], font=F["BOTAO"], padding=(8, 4), borderwidth=0)
        style.map("TButton", background=[('active', C["VERDE_HOVER"]), ('hover', C["VERDE_HOVER"])])
        style.configure("Gerar.TButton", font=F["BOTAO"], padding=(20, 10))

    def create_main_widgets(self):
        """Cria a estrutura principal da UI."""
        self.animation_canvas = tk.Canvas(self, bg=CONFIG["CORES"]["FUNDO"], highlightthickness=0)
        self.animation_canvas.place(relwidth=1, relheight=1)
        
        # Container para centralizar o conteúdo principal
        center_container = ttk.Frame(self, style="TFrame")
        center_container.configure(style="Blank.TFrame") # Estilo para ser transparente
        style = ttk.Style(self)
        style.configure("Blank.TFrame", background=CONFIG["CORES"]["FUNDO"])
        center_container.place(relx=0.5, rely=0.5, anchor="center")

        main_labelframe = ttk.LabelFrame(center_container, text=" Gerador de Senhas e Frases UNIMED ", style="Content.TLabelframe")
        main_labelframe.pack()
        
        content_frame = ttk.Frame(main_labelframe, padding=(30, 15))
        content_frame.pack(padx=10, pady=5) # Padding para não colar nas bordas
        
        self.header_label = tk.Label(content_frame, text="Gerador de Senhas", font=CONFIG["FONTES"]["CABECALHO"], bg=CONFIG["CORES"]["FRAME_PRINCIPAL"], fg=CONFIG["CORES"]["TEXTO_PRINCIPAL"])
        self.header_label.pack(pady=(0, 10))
        
        self.animator = UnimedWordAnimator(self.animation_canvas, self.header_label)
        
        try:
            img_aberta = Image.open("logo.png")
            img_redimensionada = img_aberta.resize((100, int(100 * img_aberta.size[1] / img_aberta.size[0])))
            self.logo_image = ImageTk.PhotoImage(img_redimensionada)
            logo_widget = tk.Label(content_frame, image=self.logo_image, bg=CONFIG["CORES"]["FRAME_PRINCIPAL"])
            logo_widget.pack(pady=(0, 20))
        except Exception:
            logo_widget = tk.Label(content_frame, text="UNIMED", font=("Segoe UI", 24, "bold"), bg=CONFIG["CORES"]["FRAME_PRINCIPAL"], fg=CONFIG["CORES"]["VERDE_PRIMARIO"])
            logo_widget.pack(pady=10)
            
        notebook = ttk.Notebook(content_frame)
        notebook.pack(expand=True, fill="both", pady=(0, 15))
        
        self.tab_senha = PasswordTab(notebook, self)
        self.tab_frase = PassphraseTab(notebook, self)
        
        notebook.add(self.tab_senha, text="SENHA")
        notebook.add(self.tab_frase, text="FRASE-SENHA")
        
        self.create_common_widgets(content_frame)

    def create_common_widgets(self, parent_frame):
        """Cria widgets comuns a toda a aplicação."""
        settings_frame = ttk.LabelFrame(parent_frame, text=" Configurações Gerais ", padding=10)
        settings_frame.pack(side="bottom", fill="x", pady=(10, 0))
        
        cb_animacao = ttk.Checkbutton(settings_frame, text="Ativar animação de fundo", variable=self.vars["animacao_ativa"], command=self.toggle_animation)
        cb_animacao.pack(anchor="w")
        Tooltip(cb_animacao, "Pode consumir mais CPU.")
        
    def animate_generation(self, button, target_var, length, final_callback):
        """Anima o campo de texto antes de mostrar o resultado final."""
        button.config(state="disabled")
        char_pool = string.ascii_letters + string.digits + string.punctuation
        
        def animate_step(steps_left):
            if steps_left > 0:
                if "frase" in str(target_var):
                    dots = "." * (4 - (steps_left % 4))
                    temp_text = f"Gerando{dots}"
                else:
                    temp_text = "".join(secrets.choice(char_pool) for _ in range(length))
                target_var.set(temp_text)
                self.after(50, lambda: animate_step(steps_left - 1))
            else:
                final_callback()
                button.config(state="normal")
                
        animate_step(10)

    def finalize_password_generation(self):
        """Chama o gerador e atualiza a UI com a nova senha."""
        senha, entropia = self.password_generator.generate(
            self.vars["comprimento_var"].get(), self.vars["incluir_maiusculas"].get(),
            self.vars["incluir_minusculas"].get(), self.vars["incluir_numeros"].get(),
            self.vars["incluir_especiais"].get(), self.vars["excluir_ambiguos"].get(),
            self.vars["caracteres_especiais_var"].get()
        )
        self.vars["senha_gerada"].set(senha)
        self.tab_senha.entropy_label.config(text=f"Entropia: {entropia:.2f} bits")
        self.update_history(senha)

    def finalize_passphrase_generation(self):
        """Chama o gerador e atualiza a UI com a nova frase-senha."""
        user_wordlist = self.tab_frase.wordlist_text.get("1.0", "end-1c").split()
        frase, entropia = self.password_generator.generate_passphrase(
            self.vars["num_palavras_var"].get(), self.vars["separador_var"].get(), user_wordlist
        )
        self.vars["frase_gerada"].set(frase)
        self.tab_frase.entropy_label.config(text=f"Entropia: {entropia:.2f} bits")

    def copy_to_clipboard(self, text, button):
        """Copia o texto para a área de transferência e dá feedback visual."""
        if text and "Sua" not in text and "Gerando" not in text and "Selecione" not in text:
            pyperclip.copy(text)
            original_text = button.cget("text")
            button.config(text="Copiado!", state="disabled")
            self.after(1500, lambda: button.config(text=original_text, state="normal"))

    def update_history(self, password):
        """Atualiza o histórico de senhas geradas."""
        if "Selecione" in password: return
        if password in self.password_history:
            self.password_history.remove(password)
        self.password_history.insert(0, password)
        self.password_history = self.password_history[:10]
        self.tab_senha.history_menu['values'] = self.password_history
        self.tab_senha.history_menu.set("Histórico")

    def on_history_select(self, event=None):
        """Lida com a seleção de uma senha do histórico."""
        selected_password = self.tab_senha.history_menu.get()
        if not selected_password: return
        self.vars["senha_gerada"].set(selected_password)
        entropia = self.password_generator.analyze_password(selected_password, self.vars["caracteres_especiais_var"].get())
        self.tab_senha.entropy_label.config(text=f"Entropia: {entropia:.2f} bits")

    def toggle_animation(self):
        """Ativa ou desativa a animação de fundo."""
        if self.vars["animacao_ativa"].get():
            self.animator.start()
        else:
            self.animator.stop()

    def on_closing(self):
        """Salva as configurações ao fechar a aplicação."""
        current_settings = {
            key: var.get() for key, var in self.vars.items() if key != "senha_gerada" and key != "frase_gerada"
        }
        self.settings_manager.save_settings(current_settings)
        self.destroy()

# 7. PONTO DE ENTRADA (MAIN)
if __name__ == "__main__":
    app = UnimedPasswordGeneratorApp()
    app.mainloop()
