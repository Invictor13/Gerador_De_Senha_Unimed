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
