# Gerador de Senhas e Frases - UNIMED

Ferramenta corporativa para geração de senhas seguras, verificação de vazamentos e criação de frases-senha memoráveis, desenvolvida em Python com interface moderna (CustomTkinter).

## 🚀 O que este programa faz?

1.  **Gera Senhas Fortes:** Cria senhas complexas com critérios personalizáveis (letras, números, símbolos, remoção de ambíguos).
2.  **Verifica Vazamentos:** Consulta a API *Have I Been Pwned* para alertar se a senha gerada já vazou na internet.
3.  **Gera Frases-Senha:** Cria senhas fáceis de memorizar (ex: `fogo-lago-casa-sol`) baseadas em dicionários (PT-BR, EN, Animais).
4.  **Interface Segura:** Limpa a área de transferência automaticamente após 60 segundos e oculta caracteres enquanto digita.

---

## 💻 Como Executar (Modo Desenvolvedor)

Para testar o código rodando diretamente pelo terminal:

### 1. Preparar o Ambiente
Certifique-se de ter o Python 3.8+ instalado.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
