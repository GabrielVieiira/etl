import requests
from typing import List, Dict
from etl.utils.token import get_ifractal_token
from etl.utils.config import IFRACTAL_API_URL, IFRACTAL_API_USER

HEADER = {
    'Content-Type': 'application/json',
    'User': IFRACTAL_API_USER,
    'Token': get_ifractal_token(),
}

BODY = {
    'pag': 'ponto_justificativa',
    'cmd': 'get',
}

def fetch_justificativas_abono_data() -> List[Dict[str,str]]:
    try:
        response_justificativas_abono = requests.post(IFRACTAL_API_URL, json=BODY, headers=HEADER)
        data_justificativas_abono = response_justificativas_abono.json().get('itens',[])
        return data_justificativas_abono
    except requests.RequestException as e:
        print(f'[!] Erro ao fazer requisição à API de justificativas de abono: {e}')
        return []