# Gerador de Senhas e Frases - UNIMED

Ferramenta corporativa para geração de senhas seguras, verificação de vazamentos e criação de frases-senha memoráveis, desenvolvida em Python com interface moderna (CustomTkinter).

## 🚀 O que este programa faz?

1.  **Gera Senhas Fortes:** Cria senhas complexas com critérios personalizáveis (letras, números, símbolos, remoção de ambíguos).
2.  **Verifica Vazamentos:** Consulta a API *Have I Been Pwned* para alertar se a senha gerada já vazou na internet.
3.  **Gera Frases-Senha:** Cria senhas fáceis de memorizar (ex: `fogo-lago-casa-sol`) baseadas em dicionários (PT-BR, EN, Animais).
4.  **Interface Segura:** Limpa a área de transferência automaticamente após 60 segundos e oculta caracteres enquanto digita.

---
## 🚀 Como Executar o Código

Para rodar o programa diretamente do código-fonte, siga os passos abaixo.

### Pré-requisitos
* Ter o [Python](https://www.python.org/downloads/) instalado.

### Passo a Passo

1.  **Abra o terminal** na pasta do projeto (`GeradorUnimed`).

2.  **Instale as bibliotecas necessárias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Inicie o programa:**
    Execute o comando abaixo (exatamente como está, para carregar os módulos corretamente):
    ```bash
    python -m src.main
    ```

---
*(Nota: Se você ver erros sobre "module not found", certifique-se de estar rodando o comando acima a partir da pasta raiz e não de dentro da pasta `src`)*
