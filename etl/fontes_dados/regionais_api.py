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
    'pag': 'configuracao_centro_custo',
    'cmd': 'get',
}

def fetch_centro_custo_data()->List[Dict[str,str]]:
    try:
        response_centros_de_custo = requests.post(API_URL, json=BODY, headers=HEADER)
        data_centros_de_custo = response_centros_de_custo.json().get('itens',[])
        return data_centros_de_custo
    except requests.RequestException as e:
        print(f'[!] Erro ao fazer requisição à API de centro de custo: {e}')
        return []
