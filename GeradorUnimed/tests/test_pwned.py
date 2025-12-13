import pytest
from unittest.mock import Mock
import sys
import os
import requests

# Adiciona o diretório raiz do projeto ao sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.logic import check_pwned

def test_check_pwned_password_is_pwned(mocker):
    """
    Testa se check_pwned retorna True para uma senha que está no vazamento.
    SHA-1 de "password" é 5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8
    Prefixo: 5BAA6
    Sufixo: 1E4C9B93F3F0682250B6CF8331B7EE68FD8
    """
    # Mock da resposta da API
    mock_response = Mock()
    mock_response.status_code = 200
    # A resposta da API inclui o sufixo da nossa senha de teste
    mock_response.text = "1E4C9B93F3F0682250B6CF8331B7EE68FD8:3564034\r\nOTHERHASH:123"
    mocker.patch('requests.get', return_value=mock_response)

    assert check_pwned("password") is True

def test_check_pwned_password_is_not_pwned(mocker):
    """
    Testa se check_pwned retorna False para uma senha que NÃO está no vazamento.
    """
    # Mock da resposta da API
    mock_response = Mock()
    mock_response.status_code = 200
    # A resposta da API NÃO inclui o sufixo da nossa senha de teste
    mock_response.text = "SOMEOTHERHASH:10\r\nANOTHERHASH:2"
    mocker.patch('requests.get', return_value=mock_response)

    # Usa uma senha aleatória e longa que é improvável de estar em vazamentos
    random_password = "a_very_secure_and_random_password_that_should_not_be_pwned_123!@#"
    assert check_pwned(random_password) is False

def test_check_pwned_api_error(mocker):
    """
    Testa se check_pwned retorna None em caso de erro na API (ex: timeout).
    """
    # Mock para simular um erro de requisição
    mocker.patch('requests.get', side_effect=requests.RequestException("Connection Error"))

    assert check_pwned("any_password") is None

def test_check_pwned_empty_password(mocker):
    """
    Testa se check_pwned retorna False para uma senha vazia.
    """
    # Não deve nem tentar fazer a chamada de rede
    mock_get = mocker.patch('requests.get')
    assert check_pwned("") is False
    mock_get.assert_not_called()
