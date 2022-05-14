from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass
class Ncm(object):
    """
    Class to represent a Ncm

    Attributes:
        codigo_ncm: str
        descricao_ncm: str
        data_inicio: datetime
        data_fim: datetime
        tipo_ato: str
        numero_ato: str
        ano_ato: str
    """
    codigo_ncm: str
    descricao_ncm: str
    data_inicio: datetime
    data_fim: datetime
    tipo_ato: str
    numero_ato: str
    ano_ato: int


@dataclass
class NcmList(object):
    """
    Class to represent a list of Ncm

    Attributes:
        ncm_list: List of Ncm
    """
    ncm_list: List[Ncm]
