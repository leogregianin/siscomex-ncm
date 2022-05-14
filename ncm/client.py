import json
import urllib3
from datetime import datetime

from ncm.exceptions import NcmDownloadException
from ncm.entities import Ncm, NcmList


CACHE_FILE = 'ncm.json'
NCM_URL = 'https://portalunico.siscomex.gov.br/classif/api/publico/nomenclatura/download/json?perfil=PUBLICO'  # noqa
HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'  # noqa
}


class FetchNcm(object):
    """
    Fetch data from Siscomex API

    @param only_ncm_8_digits: If True, only return Ncm with 8 digits

    """
    def __init__(self):
        self.json_data = self.load_json()
        self.only_ncm_8_digits = False

    def download_json(self, url=NCM_URL):
        """
        Download json from Siscomex API

        @param url: URL to download json
        """
        http = urllib3.PoolManager()
        response = http.request('GET', url, headers=HEADERS)
        if response.status != 200:
            raise NcmDownloadException(message=response.data.decode('utf-8'))

        return json.loads(response.data)

    def save_json(self, json_data):
        """
        Save json to file

        @param json_data: json data to save
        """
        with open(CACHE_FILE, 'w') as f:
            json.dump(json_data, f)

        return True

    def load_json(self) -> dict:
        """
        Load json from file

        @return: json data
        """
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            json_data = self.download_json()
            self.save_json(json_data)
            return json_data

    def get_all(self) -> NcmList:
        """
        Get all Ncm from json

        @return: NcmList
        """
        json_data = self.json_data['Nomenclaturas']
        list_ncm = []
        for item in json_data:
            data_inicio = datetime.strptime(item['Data_Inicio'], '%d/%m/%Y')  # noqa
            data_fim = datetime.strptime(item['Data_Fim'], '%d/%m/%Y')
            codigo_ncm = item['Codigo'].replace('.', '')

            added_ncm = True
            if self.only_ncm_8_digits:
                if len(codigo_ncm) != 8:
                    added_ncm = False

            if added_ncm:
                list_ncm.append(
                    Ncm(
                        codigo_ncm=item['Codigo'],
                        descricao_ncm=item['Descricao'],
                        data_inicio=data_inicio,
                        data_fim=data_fim,
                        tipo_ato=item['Tipo_Ato'],
                        numero_ato=item['Numero_Ato'],
                        ano_ato=item['Ano_Ato']
                    )
                )

        return NcmList(ncm_list=list_ncm)

    def get_codigo_ncm(self, codigo_ncm: str) -> Ncm:
        """
        Get Ncm by codigo_ncm

        @param codigo_ncm: codigo_ncm to search
        @return: Ncm
        """
        json_data = self.json_data['Nomenclaturas']
        for item in json_data:
            codigo_ncm_json = item['Codigo'].replace('.', '')

            if codigo_ncm_json == codigo_ncm:
                data_inicio = datetime.strptime(item['Data_Inicio'], '%d/%m/%Y')  # noqa
                data_fim = datetime.strptime(item['Data_Fim'], '%d/%m/%Y')

                return Ncm(
                    codigo_ncm=codigo_ncm_json,
                    descricao_ncm=item['Descricao'],
                    data_inicio=data_inicio,
                    data_fim=data_fim,
                    tipo_ato=item['Tipo_Ato'],
                    numero_ato=item['Numero_Ato'],
                    ano_ato=item['Ano_Ato']
                )

        return Ncm(
            codigo_ncm='',
            descricao_ncm='',
            data_inicio=datetime.now(),
            data_fim=datetime.now(),
            tipo_ato='',
            numero_ato='',
            ano_ato=0,
        )
