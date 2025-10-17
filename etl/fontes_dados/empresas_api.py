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
    'pag': 'configuracao_empresa',
    'cmd': 'get',
}

def fetch_empresas_data()->List[Dict[str,str]]:
    try:
        response_empresas = requests.post(API_URL, json=BODY, headers=HEADER)
        data_empresas = response_empresas.json().get('itens',[])
        return data_empresas
    except requests.RequestException as e:
        print(f'[!] Erro ao fazer requisição à API de empresas: {e}')
        return []