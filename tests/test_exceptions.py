import pytest
from unittest.mock import patch, MagicMock

from ncm.client import FetchNcm
from ncm.exceptions import NcmDownloadException


class TestNcmDownloadError:

    def test_exceptions_download_error(self):
        with patch('ncm.client.FetchNcm._load_data'):  # Evita carregar dados no construtor
            ncm = FetchNcm()

            # Cria uma resposta de erro
            mock_response = MagicMock()
            mock_response.status = 403
            mock_response.data = b'{"erro": "Acesso negado"}'

            # Testa falha de status HTTP
            with patch('urllib3.PoolManager.request', return_value=mock_response):
                with pytest.raises(NcmDownloadException) as error:
                    ncm.download_json('mock:8080')
                assert "not return 200" in str(error.value)


    def test_exceptions_json_decode_error(self):
        with patch('ncm.client.FetchNcm._load_data'):  # Evita carregar dados no construtor
            ncm = FetchNcm()

            # Cria uma resposta com JSON inválido
            mock_response = MagicMock()
            mock_response.status = 200
            mock_response.data = b'{"dados": invalidJson}'

            # Testa erro de decodificação de JSON
            with patch('urllib3.PoolManager.request', return_value=mock_response):
                with pytest.raises(NcmDownloadException) as error:
                    ncm.download_json('mock:8080')
                assert "Erro ao decodificar JSON" in str(error.value)
