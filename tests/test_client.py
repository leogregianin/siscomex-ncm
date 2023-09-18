from datetime import datetime
from pathlib import Path

from ncm.client import FetchNcm, CACHE_FILE
from ncm.exceptions import NcmDownloadException

import pytest
from unittest.mock import patch


def test_download_json():
    fetch_ncm = FetchNcm()
    json_data = fetch_ncm.download_json()
    assert json_data is not None


def test_download_error():
    ncm = FetchNcm()
    with patch(
        'ncm.client.FetchNcm.download_json',
        side_effect=NcmDownloadException('Error ABC')
    ):
        with pytest.raises(NcmDownloadException) as error:
            ncm.download_json('mock:8080')
        assert str(error.value) == "Error: API not return 200 with the message Error ABC"


def test_save_json():
    fetch_ncm = FetchNcm()
    json_data = fetch_ncm.download_json()
    save_json = fetch_ncm.save_json(json_data)
    assert save_json is True


def test_load_json():
    fetch_ncm = FetchNcm()
    json_data = fetch_ncm.load_json()
    assert json_data is not None


def test_load_json_with_filenotfound():
    fetch_ncm = FetchNcm()

    # delete cache file
    file_to_rem = Path(CACHE_FILE)
    file_to_rem.unlink()

    json_data = fetch_ncm.load_json()
    assert json_data is not None


def test_get_codigo_ncm_correto():
    fetch_ncm = FetchNcm()
    obj_dict = fetch_ncm.get_codigo_ncm('01031000')

    assert obj_dict is not None
    assert obj_dict.codigo_ncm == '01031000'
    assert obj_dict.descricao_ncm == '- Reprodutores de raça pura'
    assert obj_dict.data_inicio == datetime(
        day=1, month=4, year=2022, hour=0, minute=0, second=0
    )
    assert obj_dict.data_fim == datetime(
        day=31, month=12, year=9999, hour=0, minute=0, second=0
    )
    assert obj_dict.tipo_ato == 'Res Camex'
    assert obj_dict.numero_ato == '272'
    assert obj_dict.ano_ato == '2021'


def test_get_codigo_ncm_incorreto():
    fetch_ncm = FetchNcm()
    obj_dict = fetch_ncm.get_codigo_ncm('01012199')
    assert obj_dict.codigo_ncm == ''


def test_get_all_ncm_list():
    fetch_ncm = FetchNcm()
    ncm_list = fetch_ncm.get_all()

    assert ncm_list is not None
    assert len(ncm_list.ncm_list) > 0


def test_get_all_ncm_list_only_8_digits():
    fetch_ncm = FetchNcm()
    fetch_ncm.only_ncm_8_digits = True
    ncm_list = fetch_ncm.get_all()

    assert ncm_list is not None
    assert len(ncm_list.ncm_list) > 0
