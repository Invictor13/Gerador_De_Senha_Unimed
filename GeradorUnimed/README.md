# Gerador de Senhas e Frases - UNIMED (Versão Refatorada)

Este é um gerador de senhas e frases-senha seguro e configurável, construído com Python e Tkinter. O projeto foi refatorado a partir de um script único para uma estrutura de projeto modular, robusta e de fácil manutenção.

## Funcionalidades

- **Gerador de Senhas:** Crie senhas fortes com opções configuráveis:
  - Comprimento customizável (8-64 caracteres)
  - Inclusão de letras maiúsculas, minúsculas, números e símbolos
  - Opção para excluir caracteres ambíguos (I, l, 1, O, 0, o)
  - Pool de caracteres especiais customizável
- **Gerador de Frases-Senha:** Crie frases-senha memoráveis (passphrases) baseadas em listas de palavras.
  - Listas de palavras pré-definidas (Português, Inglês, Animais)
  - Suporte para lista de palavras personalizada
  - Número de palavras e caractere separador configuráveis
- **Análise de Entropia:** Calcule a força de suas senhas e frases-senha em bits.
- **Interface Gráfica Agradável:** Interface intuitiva com uma animação de fundo opcional inspirada em "The Matrix".
- **Persistência:** Suas configurações são salvas localmente e recarregadas na próxima vez que você abrir o aplicativo.

## Como Executar

### Pré-requisitos

- Python 3.6 ou superior
- Pip (gerenciador de pacotes do Python)

### Instalação

1.  **Clone o repositório (ou baixe o código-fonte):**
    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd GeradorUnimed
    ```

2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    ```
    - No Windows: `venv\Scripts\activate`
    - No macOS/Linux: `source venv/bin/activate`

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

### Executando a Aplicação

Com o ambiente virtual ativado e as dependências instaladas, execute o seguinte comando na raiz do projeto (`/GeradorUnimed/`):

```bash
python -m src.main
```

Isso iniciará a interface gráfica do gerador de senhas.

### Executando os Testes

Para garantir que a lógica principal do projeto está funcionando corretamente, você pode executar os testes unitários com `pytest`:

```bash
pytest
```

## Estrutura do Projeto

O projeto foi organizado de forma modular para separar responsabilidades e facilitar a manutenção e o desenvolvimento de novas funcionalidades.

```
/GeradorUnimed/
├── src/                      # Contém todo o código-fonte da aplicação
│   ├── __init__.py
│   ├── main.py               # Ponto de entrada da aplicação, inicia a UI
│   ├── config.py             # Módulo de constantes (cores, fontes, padrões)
│   ├── logic.py              # Classes de backend (PasswordGenerator, SettingsManager)
│   └── ui/                   # Pacote contendo os módulos da interface gráfica
│       ├── __init__.py
│       ├── app.py            # Classe principal da UI (UnimedPasswordGeneratorApp)
│       ├── components.py     # Classes dos componentes (abas de senha e frase)
│       └── utils.py          # Classes de utilitários da UI (Tooltip, Animator)
├── tests/                    # Contém os testes unitários
│   ├── __init__.py
│   └── test_logic.py         # Testes para o PasswordGenerator
├── assets/                   # Contém recursos estáticos
│   └── logo.png              # Logo da Unimed (adicione o arquivo aqui)
├── .gitignore                # Arquivos e pastas a serem ignorados pelo Git
├── requirements.txt          # Lista de dependências Python do projeto
└── README.md                 # Este arquivo
```
