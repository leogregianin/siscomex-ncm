## siscomex-ncm
[![PyPI](https://img.shields.io/pypi/v/siscomex-ncm)](https://pypi.org/project/siscomex-ncm/) ![pyversions](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue) ![https://github.com/leogregianin/siscomex-ncm/actions](https://github.com/leogregianin/siscomex-ncm/workflows/CI/badge.svg?branch=main)

## NCM (Nomenclatura Comum do Mercosul)

`NCM` é a sigla para `Nomenclatura Comum do Mercosul`, toda e qualquer mercadoria que circula no Brasil deve ter este código. A NCM permite a identificação padronizada das mercadorias comercializadas, ou seja todo produto possui uma NCM.

O código deve ser informado no preenchimento da nota fiscal e outros documentos de comércio exterior.

A NCM é adotada por todos os países membros do Mercosul desde janeiro de 1995 e tem como base o método internacional de classificação de mercadoria, chamado como SH (Sistema Harmonizado de Designação e de Codificação de Mercadorias).

O código é usado nas operações de exportação e importação de mercadorias desde 1995, já no mercado interno é obrigatório desde 2013.

## Como funciona?

A Nomenclatura Comum do Mercosul obedece à seguinte estrutura de código: 0000.00.00

Ou seja, é um código de oito dígitos que correspondem ao produto. Cada um dos numerais representa algo diferente, conforme abaixo:

 * Os dois primeiros caracterizam o produto (capítulo);
 * Os dois números seguintes abrangem mais sobre a característica do produto (posição);
 * O quinto e sexto definem a subcategoria do mesmo (ou subposição);
 * O sétimo o classifica (item); e
 * O oitavo se refere ao subitem, que descreve especificamente do que se trata a mercadoria.

Para exemplificar, veja a NCM `4820.20.00`, deve ser entendido da seguinte forma:

 * Capítulo 48: Papel e cartão; obras de pasta de celulose, de papel ou de cartão.

 * Posição 48.20: Livros de registro e de contabilidade, blocos de notas, de encomendas, de recibos, de apontamentos, de papel para cartas, agendas e artigos semelhantes, cadernos, pastas para documentos, classificadores, capas para encadernação (de folhas soltas ou outras), capas de processos e outros artigos escolares, de escritório ou de papelaria, incluindo os formulários em blocos tipo manifold, mesmo com folhas intercaladas de papel-carbono (papel químico), de papel ou cartão; álbuns para amostras ou para coleções e capas para livros, de papel ou cartão.

 * Subposição: Neste exemplo não tem.

 * Item: Neste exemplo não tem.

 * Subitem 4820.20.00 – Cadernos



## Como instalar a biblioteca pelo PyPI?

 * `pip install siscomex-ncm`


## Como instalar a biblioteca pelo código-fonte?

 * Faça fork deste projeto
 * Instale o [poetry](https://python-poetry.org/docs/#installation)
 * Instale as dependências do projeto: `poetry install`


## Como executar os testes?

 * Executar os testes: `make test`


## Como usar essa biblioteca?

### Importar a biblioteca

```python
from ncm.entities import Ncm, NcmList
from ncm.client import FetchNcm
```

### Download do arquivo JSON

```python
fetch_ncm = FetchNcm()
fetch_ncm.download_json()
```


### Gravar do arquivo JSON localmente

```python
fetch_ncm = FetchNcm()
fetch_ncm.download_json()
fetch_ncm.save_json(json_data)
json_data = fetch_ncm.load_json()
```

### Consulta código NCM específico

```python
fetch_ncm = FetchNcm()
obj_dict = fetch_ncm.get_codigo_ncm('01031000')
print(obj_dict.descricao_ncm)  # result: '- Reprodutores de raça pura'
```

### Consulta toda a lista de NCMs

```python
fetch_ncm = FetchNcm()
ncm_list = fetch_ncm.get_all()
print(ncm_list.ncm_list)
```

### Consulta toda a lista de NCMs e retorno somente os códigos com 8 dígitos

```python
fetch_ncm = FetchNcm()
fetch_ncm.only_ncm_8_digits = True
ncm_list = fetch_ncm.get_all()
print(ncm_list.ncm_list)
```

## Licença

  MIT License