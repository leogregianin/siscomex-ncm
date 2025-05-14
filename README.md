# Siscomex-NCM

[![PyPI](https://img.shields.io/pypi/v/siscomex-ncm)](https://pypi.org/project/siscomex-ncm/) 
![pyversions](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue) 
![CI](https://github.com/leogregianin/siscomex-ncm/workflows/CI/badge.svg?branch=main)

Uma biblioteca Python para acessar e consultar dados da Nomenclatura Comum do Mercosul (NCM) a partir da API do Siscomex.

## Sobre a NCM

A **Nomenclatura Comum do Mercosul (NCM)** é o sistema padronizado de códigos utilizado para classificar mercadorias e produtos em operações comerciais no Mercosul. Toda mercadoria que circula no Brasil deve ter um código NCM associado, que deve ser informado nas notas fiscais e documentos de comércio exterior.

O sistema foi adotado pelos países do Mercosul desde janeiro de 1995 e baseia-se no Sistema Harmonizado de Designação e de Codificação de Mercadorias (SH). No mercado interno brasileiro, seu uso é obrigatório desde 2013.

### Estrutura do código NCM

O código NCM segue a estrutura `0000.00.00`, um código de oito dígitos em que:

| Posição | Componente | Descrição |
|---------|------------|-----------|
| 1º e 2º | Capítulo | Caracterização básica do produto |
| 3º e 4º | Posição | Características gerais do produto |
| 5º e 6º | Subposição | Subcategoria do produto |
| 7º | Item | Classificação específica |
| 8º | Subitem | Descrição detalhada da mercadoria |

**Exemplo:**  
Código NCM: `4820.20.00` - Cadernos

* **Capítulo 48**: Papel e cartão; obras de pasta de celulose, de papel ou de cartão.
* **Posição 48.20**: Livros de registro, blocos de notas, cadernos, etc.
* **Subposição 4820.20**: Cadernos

## Instalação

### Via PyPI (recomendado)

```bash
pip install siscomex-ncm
```

### A partir do código-fonte

```bash
# 1. Clone o repositório
git clone https://github.com/leogregianin/siscomex-ncm.git
cd siscomex-ncm

# 2. Instale o poetry (se ainda não estiver instalado)
# https://python-poetry.org/docs/#installation

# 3. Instale as dependências
poetry install
```

## Uso Básico

### Importar a biblioteca

```python
from ncm.client import FetchNcm
from ncm.entities import Ncm, NcmList
```

### Consultar código NCM específico

```python
# Inicializa o cliente (carrega automaticamente os dados do cache ou da API)
fetch_ncm = FetchNcm()

# Consulta um código NCM específico
ncm = fetch_ncm.get_codigo_ncm('01031000')
print(ncm.codigo_ncm)      # '01031000'
print(ncm.descricao_ncm)   # '- Reprodutores de raça pura'
print(ncm.data_inicio)     # datetime object
print(ncm.tipo_ato)        # Tipo do ato normativo
```

### Consultar lista de NCMs

```python
# Obter todos os códigos NCM
ncm_list = fetch_ncm.get_all()
print(len(ncm_list.ncm_list))  # Quantidade de códigos

# Obter apenas códigos NCM com 8 dígitos
ncm_list_8_digits = fetch_ncm.get_all(only_ncm_8_digits=True)

# Iterar sobre os resultados
for ncm in ncm_list_8_digits.ncm_list:
    print(f"{ncm.codigo_ncm}: {ncm.descricao_ncm}")
```

### Gerenciar o cache de dados

```python
# Atualizar os dados forçadamente (ignorando o cache)
fetch_ncm = FetchNcm()
fetch_ncm.refresh_data()

# A classe FetchNcm gerencia automaticamente o cache:
# - Armazena os dados em um arquivo local (ncm.json)
# - Valida a data do cache (expira após 7 dias)
# - Verifica a integridade do arquivo
```

## Funcionalidades Avançadas

### Tratamento de erros

```python
from ncm.exceptions import NcmDownloadException

try:
    fetch_ncm = FetchNcm()
    ncm = fetch_ncm.get_codigo_ncm('01031000')
except NcmDownloadException as e:
    print(f"Erro ao baixar dados da API: {e}")
```

### Performance otimizada

A biblioteca implementa diversas otimizações:
- Índice interno para busca rápida por código NCM
- Cache de consultas com `lru_cache` para operações repetidas
- Expiração automática do cache (7 dias por padrão)
- Tratamento de conexão com timeout e retentativas

## Desenvolvimento

### Executar os testes

```bash
make test
```

### Contribuir

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Implemente suas mudanças e adicione testes
4. Commite suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
5. Envie para o GitHub (`git push origin feature/nova-funcionalidade`)
6. Abra um Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.