import requests
from typing import List, Dict

from etl.utils.token import get_ifractal_token
from etl.utils.config import IFRACTAL_API_URL, IFRACTAL_API_USER

colunas_que_me_interessam_cargos = [
    'codigo',
    'nome',
    'cod_empresa',
    'qtd'
]

HEADER = {
    'Content-Type': 'application/json',
    'User': IFRACTAL_API_USER,
    'Token': get_ifractal_token(),
}

BODY = {
    'pag': 'configuracao_cargo',
    'cmd': 'get',
}

def fetch_cargos_data()-> List[Dict[str,str]]:
    try:
        response_cargos_e_funcoes = requests.post(IFRACTAL_API_URL, json=BODY, headers=HEADER)
        response_cargos_e_funcoes.raise_for_status()

        data_cargos_e_funcoes = response_cargos_e_funcoes.json().get('itens',[])
        return data_cargos_e_funcoes
    
    except requests.RequestException as e:
        print(f'[!] Erro ao fazer requisição à API de cargos: {e}')
        return []