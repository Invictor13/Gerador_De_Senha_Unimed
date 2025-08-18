# -*- coding: utf-8 -*-
"""
Módulo de Lógica (Backend)

Este arquivo contém as classes responsáveis pela lógica de negócio
da aplicação, como a geração de senhas e o gerenciamento de configurações.
Não há código de interface gráfica aqui.
"""

import hashlib
import json
import math
import os
import secrets
import string

import requests

from src.config import CONFIG

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


class PasswordValidator:
    """Valida a força de uma senha com base em um conjunto de regras."""
    COMMON_NAMES = ['joao', 'maria', 'ana', 'pedro', 'paulo', 'unimed']

    def _has_minimum_length(self, password: str) -> bool:
        """Verifica se a senha tem o comprimento mínimo de 10 caracteres."""
        return len(password) >= 10

    def _has_upper_and_lower_case(self, password: str) -> bool:
        """Verifica se a senha contém caracteres maiúsculos e minúsculos."""
        return any(c.isupper() for c in password) and any(c.islower() for c in password)

    def _has_number(self, password: str) -> bool:
        """Verifica se a senha contém pelo menos um número."""
        return any(c.isdigit() for c in password)

    def _has_symbol(self, password: str) -> bool:
        """Verifica se a senha contém pelo menos um caractere de pontuação."""
        return any(c in string.punctuation for c in password)

    def _has_no_common_names(self, password: str) -> bool:
        """Verifica se a senha não contém nomes próprios comuns."""
        password_lower = password.lower()
        return not any(name in password_lower for name in self.COMMON_NAMES)

    def analyze(self, password: str) -> dict:
        """
        Analisa a senha e retorna um dicionário com os resultados da validação.
        """
        return {
            'length_ok': self._has_minimum_length(password),
            'case_ok': self._has_upper_and_lower_case(password),
            'has_number': self._has_number(password),
            'has_symbol': self._has_symbol(password),
            'no_common_names': self._has_no_common_names(password),
        }


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

def check_pwned(password: str) -> bool:
    """
    Verifica se a senha aparece em vazamentos de dados usando a API Pwned Passwords.

    Args:
        password: A senha para verificar.

    Returns:
        True se a senha foi encontrada em um vazamento, False caso contrário.
    """
    if not password:
        return False
    try:
        sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix, suffix = sha1_password[:5], sha1_password[5:]
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=5)
        response.raise_for_status()  # Lança exceção para códigos de erro HTTP
        # A resposta é uma lista de sufixos de hash e suas contagens
        # Ex: 0018A45C4D1DEF81644B54AB7F969B88D65:1
        return any(line.startswith(suffix) for line in response.text.splitlines())
    except requests.RequestException:
        # Em caso de erro de rede ou timeout, consideramos a senha como segura
        # para não impedir o usuário de usar a senha.
        return False
