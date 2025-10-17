import requests
from typing import List, Dict
from etl.utils.token import get_ifractal_token
from etl.utils.config import API_URL, API_USER

HEADER = {
    'Content-Type': 'application/json',
    'User': API_USER,
    'Token': get_ifractal_token(),
}

BODY = {
    'pag': 'configuracao_depto',
    'cmd': 'get',
}

def fetch_departamentos_data()->List[Dict[str,str]]:
    try:
        response_departamentos = requests.post(API_URL, json=BODY, headers=HEADER)
        data_departamentos = response_departamentos.json()
        return data_departamentos
    except requests.RequestException as e:
        print(f'[!] Erro ao fazer requisição à API de departamentos: {e}')
        return []