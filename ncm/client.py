import json
import os
import urllib3
from datetime import datetime, timedelta
from functools import lru_cache
from typing import Dict

from ncm.exceptions import NcmDownloadException
from ncm.entities import Ncm, NcmList


CACHE_FILE = 'ncm.json'
NCM_URL = 'https://portalunico.siscomex.gov.br/classif/api/publico/nomenclatura/download/json?perfil=PUBLICO'  # noqa
HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'  # noqa
}
DATE_FORMAT = '%d/%m/%Y'
CACHE_EXPIRATION_DAYS = 7  # Cache expira após 7 dias


class FetchNcm:
    """
    Fetch data from Siscomex API

    Attributes:
        json_data: Dictionary with NCM data
        ncm_index: Dictionary for fast NCM lookup by code
        only_ncm_8_digits: If True, only return Ncm with 8 digits
    """
    def __init__(self):
        self.json_data = None
        self.ncm_index = None
        self.only_ncm_8_digits = False
        self._load_data()

    def download_json(self, url: str = NCM_URL) -> dict:
        """
        Download json from Siscomex API

        Args:
            url: URL to download json

        Returns:
            Dictionary with JSON data

        Raises:
            NcmDownloadException: If API returns non-200 status
        """
        try:
            http = urllib3.PoolManager(timeout=10.0, retries=3)
            response = http.request('GET', url, headers=HEADERS)
            if response.status != 200:
                raise NcmDownloadException(
                    message=response.data.decode('utf-8')
                )

            return json.loads(response.data)
        except urllib3.exceptions.HTTPError as e:
            raise NcmDownloadException(
                message=f"Erro de conexão: {str(e)}"
            )
        except json.JSONDecodeError as e:
            raise NcmDownloadException(
                message=f"Erro ao decodificar JSON: {str(e)}"
            )

    def save_json(self, json_data: dict) -> bool:
        """
        Save json to file

        Args:
            json_data: json data to save

        Returns:
            True if successful
        """
        try:
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Erro ao salvar cache: {str(e)}")
            return False

    def _is_cache_valid(self) -> bool:
        """
        Check if cache file is valid and not expired

        Returns:
            True if cache is valid, False otherwise
        """
        if not os.path.exists(CACHE_FILE):
            return False

        # Verifica se o arquivo é mais recente que CACHE_EXPIRATION_DAYS
        file_modified_time = datetime.fromtimestamp(
            os.path.getmtime(CACHE_FILE)
        )
        expiration_time = datetime.now() - timedelta(
            days=CACHE_EXPIRATION_DAYS
        )

        return file_modified_time > expiration_time

    def _load_data(self) -> None:
        """
        Load JSON data and build index
        """
        if self._is_cache_valid():
            try:
                with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                    self.json_data = json.load(f)
            except (json.JSONDecodeError, IOError):
                # Se o arquivo estiver corrompido, baixa novamente
                self.json_data = self.download_json()
                self.save_json(self.json_data)
        else:
            self.json_data = self.download_json()
            self.save_json(self.json_data)

        # Constrói o índice para acesso rápido por código NCM
        self.ncm_index = self._build_ncm_index()

    def _build_ncm_index(self) -> Dict[str, dict]:
        """
        Build index for fast NCM lookup

        Returns:
            Dictionary with NCM codes as keys
        """
        index = {}
        for item in self.json_data['Nomenclaturas']:
            codigo_ncm = item['Codigo'].replace('.', '')
            index[codigo_ncm] = {
                'descricao_ncm': item['Descricao'],
                'data_inicio': datetime.strptime(
                    item['Data_Inicio'], DATE_FORMAT
                ),
                'data_fim': datetime.strptime(
                    item['Data_Fim'], DATE_FORMAT
                ),
                'tipo_ato': item['Tipo_Ato_Ini'],
                'numero_ato': item['Numero_Ato_Ini'],
                'ano_ato': item['Ano_Ato_Ini']
            }
        return index

    def get_all(self, only_ncm_8_digits: bool = False) -> NcmList:
        """
        Get all Ncm from json

        Args:
            only_ncm_8_digits: If True, only return Ncm with 8 digits

        Returns:
            NcmList object with all NCMs
        """
        list_ncm = []

        # Usa o índice pré-construído para maior eficiência
        for codigo_ncm, data in self.ncm_index.items():
            if not only_ncm_8_digits or len(codigo_ncm) == 8:
                list_ncm.append(
                    Ncm(
                        codigo_ncm=codigo_ncm,
                        descricao_ncm=data['descricao_ncm'],
                        data_inicio=data['data_inicio'],
                        data_fim=data['data_fim'],
                        tipo_ato=data['tipo_ato'],
                        numero_ato=data['numero_ato'],
                        ano_ato=data['ano_ato']
                    )
                )
        return NcmList(ncm_list=list_ncm)

    @lru_cache(maxsize=512)
    def get_codigo_ncm(self, codigo_ncm: str) -> Ncm:
        """
        Get Ncm by codigo_ncm with caching for repeated lookups

        Args:
            codigo_ncm: codigo_ncm to search

        Returns:
            Ncm object or empty Ncm if not found
        """
        if codigo_ncm not in self.ncm_index:
            return Ncm(
                codigo_ncm='',
                descricao_ncm='',
                data_inicio=datetime.now(),
                data_fim=datetime.now(),
                tipo_ato='',
                numero_ato='',
                ano_ato=0,
            )

        data = self.ncm_index[codigo_ncm]
        return Ncm(
            codigo_ncm=codigo_ncm,
            descricao_ncm=data['descricao_ncm'],
            data_inicio=data['data_inicio'],
            data_fim=data['data_fim'],
            tipo_ato=data['tipo_ato'],
            numero_ato=data['numero_ato'],
            ano_ato=data['ano_ato']
        )

    def refresh_data(self) -> bool:
        """
        Force refresh of NCM data from API

        Returns:
            True if successful
        """
        try:
            self.json_data = self.download_json()
            success = self.save_json(self.json_data)
            if success:
                # Limpa o cache de consultas anteriores
                self.get_codigo_ncm.cache_clear()
                # Reconstrói o índice
                self.ncm_index = self._build_ncm_index()
            return success
        except Exception:
            return False
