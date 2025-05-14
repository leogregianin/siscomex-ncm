from datetime import datetime, timedelta
import json
import os
from pathlib import Path

from ncm.client import FetchNcm, CACHE_FILE, CACHE_EXPIRATION_DAYS
from ncm.exceptions import NcmDownloadException

import pytest
from unittest.mock import patch, MagicMock


def test_download_json():
    fetch_ncm = FetchNcm()
    with patch('ncm.client.FetchNcm._load_data'):  # Evita carregar dados no construtor
        fetch_ncm.json_data = None
        json_data = fetch_ncm.download_json()
        assert json_data is not None


def test_json_decode_error():
    with patch('ncm.client.FetchNcm._load_data'):  # Evita carregar dados no construtor
        ncm = FetchNcm()
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.data = b'invalid json'

        with patch('urllib3.PoolManager.request', return_value=mock_response):
            with pytest.raises(NcmDownloadException) as exc_info:
                ncm.download_json('mock:8080')
            assert "Erro ao decodificar JSON" in str(exc_info.value)


def test_save_json():
    with patch('ncm.client.FetchNcm._load_data'):  # Evita carregar dados no construtor
        fetch_ncm = FetchNcm()
        mock_data = {"test": "data"}

        with patch('builtins.open', MagicMock()):
            with patch('json.dump') as mock_dump:
                save_result = fetch_ncm.save_json(mock_data)
                assert save_result is True
                mock_dump.assert_called_once()


def test_save_json_error():
    with patch('ncm.client.FetchNcm._load_data'):  # Evita carregar dados no construtor
        fetch_ncm = FetchNcm()
        mock_data = {"test": "data"}

        with patch('builtins.open', side_effect=IOError("Erro de escrita")):
            save_result = fetch_ncm.save_json(mock_data)
            assert save_result is False


def test_is_cache_valid_nonexistent():
    with patch('ncm.client.FetchNcm._load_data'):  # Evita carregar dados no construtor
        fetch_ncm = FetchNcm()
        with patch('os.path.exists', return_value=False):
            assert fetch_ncm._is_cache_valid() is False


def test_is_cache_valid_expired():
    with patch('ncm.client.FetchNcm._load_data'):  # Evita carregar dados no construtor
        fetch_ncm = FetchNcm()

        # Simula arquivo antigo (expirado)
        old_time = datetime.now() - timedelta(days=CACHE_EXPIRATION_DAYS + 1)
        old_timestamp = old_time.timestamp()

        with patch('os.path.exists', return_value=True):
            with patch('os.path.getmtime', return_value=old_timestamp):
                assert fetch_ncm._is_cache_valid() is False


def test_is_cache_valid_recent():
    with patch('ncm.client.FetchNcm._load_data'):  # Evita carregar dados no construtor
        fetch_ncm = FetchNcm()

        # Simula arquivo recente (válido)
        recent_time = datetime.now() - timedelta(days=1)
        recent_timestamp = recent_time.timestamp()

        with patch('os.path.exists', return_value=True):
            with patch('os.path.getmtime', return_value=recent_timestamp):
                assert fetch_ncm._is_cache_valid() is True


def test_build_ncm_index():
    with patch('ncm.client.FetchNcm._load_data'):  # Evita carregar dados no construtor
        fetch_ncm = FetchNcm()
        fetch_ncm.json_data = {
            "Nomenclaturas": [
                {
                    "Codigo": "01.03.10.00",
                    "Descricao": "- Reprodutores de raça pura",
                    "Data_Inicio": "01/04/2022",
                    "Data_Fim": "31/12/9999",
                    "Tipo_Ato_Ini": "Res Camex",
                    "Numero_Ato_Ini": "272",
                    "Ano_Ato_Ini": "2021"
                }
            ]
        }

        index = fetch_ncm._build_ncm_index()
        assert "01031000" in index
        assert index["01031000"]["descricao_ncm"] == "- Reprodutores de raça pura"


def test_get_codigo_ncm_correto():
    fetch_ncm = FetchNcm()
    with patch.object(fetch_ncm, 'ncm_index', {
        "01031000": {
            "descricao_ncm": "- Reprodutores de raça pura",
            "data_inicio": datetime(day=1, month=4, year=2022),
            "data_fim": datetime(day=31, month=12, year=9999),
            "tipo_ato": "Res Camex",
            "numero_ato": "272",
            "ano_ato": "2021"
        }
    }):
        # Limpa o cache LRU para garantir que busque nos dados mockados
        fetch_ncm.get_codigo_ncm.cache_clear()

        obj_dict = fetch_ncm.get_codigo_ncm('01031000')
        assert obj_dict is not None
        assert obj_dict.codigo_ncm == '01031000'
        assert obj_dict.descricao_ncm == '- Reprodutores de raça pura'
        assert obj_dict.tipo_ato == 'Res Camex'
        assert obj_dict.numero_ato == '272'
        assert obj_dict.ano_ato == '2021'


def test_get_codigo_ncm_incorreto():
    fetch_ncm = FetchNcm()
    with patch.object(fetch_ncm, 'ncm_index', {}):
        # Limpa o cache LRU para garantir que busque nos dados mockados
        fetch_ncm.get_codigo_ncm.cache_clear()

        obj_dict = fetch_ncm.get_codigo_ncm('12345678')
        assert obj_dict.codigo_ncm == ''


def test_get_all_ncm_list():
    fetch_ncm = FetchNcm()
    mock_index = {
        "01031000": {
            "descricao_ncm": "Item 1",
            "data_inicio": datetime.now(),
            "data_fim": datetime.now(),
            "tipo_ato": "X",
            "numero_ato": "Y",
            "ano_ato": "2022"
        },
        "02031000": {
            "descricao_ncm": "Item 2",
            "data_inicio": datetime.now(),
            "data_fim": datetime.now(),
            "tipo_ato": "X",
            "numero_ato": "Y",
            "ano_ato": "2022"
        }
    }

    with patch.object(fetch_ncm, 'ncm_index', mock_index):
        ncm_list = fetch_ncm.get_all()
        assert ncm_list is not None
        assert len(ncm_list.ncm_list) == 2


def test_get_all_ncm_list_only_8_digits():
    fetch_ncm = FetchNcm()
    mock_index = {
        "01031000": {  # 8 dígitos
            "descricao_ncm": "Item 1",
            "data_inicio": datetime.now(),
            "data_fim": datetime.now(),
            "tipo_ato": "X",
            "numero_ato": "Y",
            "ano_ato": "2022"
        },
        "0203": {  # 4 dígitos
            "descricao_ncm": "Item 2",
            "data_inicio": datetime.now(),
            "data_fim": datetime.now(),
            "tipo_ato": "X",
            "numero_ato": "Y",
            "ano_ato": "2022"
        }
    }

    with patch.object(fetch_ncm, 'ncm_index', mock_index):
        ncm_list = fetch_ncm.get_all(only_ncm_8_digits=True)
        assert ncm_list is not None
        assert len(ncm_list.ncm_list) == 1
        assert ncm_list.ncm_list[0].codigo_ncm == "01031000"


def test_refresh_data():
    with patch('ncm.client.FetchNcm._load_data'):  # Evita carregar dados no construtor
        fetch_ncm = FetchNcm()
        mock_data = {"Nomenclaturas": []}
        
        with patch('ncm.client.FetchNcm.download_json', return_value=mock_data):
            with patch('ncm.client.FetchNcm.save_json', return_value=True):
                with patch('ncm.client.FetchNcm.get_codigo_ncm.cache_clear') as mock_clear:
                    with patch('ncm.client.FetchNcm._build_ncm_index') as mock_build_index:
                        assert fetch_ncm.refresh_data() is True
                        mock_clear.assert_called_once()
                        mock_build_index.assert_called_once()


def test_refresh_data_failure():
    with patch('ncm.client.FetchNcm._load_data'):  # Evita carregar dados no construtor
        fetch_ncm = FetchNcm()
        
        with patch('ncm.client.FetchNcm.download_json', side_effect=Exception("Erro de download")):
            assert fetch_ncm.refresh_data() is False
