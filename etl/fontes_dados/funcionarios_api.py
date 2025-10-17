import requests
from typing import List, Dict
from etl.utils.token import get_ifractal_token
from etl.utils.config import API_URL, API_USER

HEADER = {
    'Content-Type': 'application/json',
    'User': API_USER,
    'Token': get_ifractal_token()
}

BODY_ATIVOS = {
    'pag': 'funcionario_cadastrar',
    'cmd': 'get'
}

BODY_INATIVOS = {
    'pag': 'funcionario_cadastrar',
    'cmd': 'get',
    'demitido': 'True'
}

def fetch_funcionarios_data() -> List[Dict[str,str]]:
    try:
        response_ativos = requests.post(API_URL, json=BODY_ATIVOS, headers=HEADER, timeout=30)
        response_ativos.raise_for_status()

        response_inativos = requests.post(API_URL, json=BODY_INATIVOS, headers=HEADER, timeout=30)
        response_inativos.raise_for_status()

        data_ativos = response_ativos.json().get('itens', [])
        data_inativos = response_inativos.json().get('itens', [])

        return data_ativos + data_inativos

    except requests.RequestException as e:
        print(f'[!] Erro ao fazer requisição à API de funcionarios: {e}')
        return []