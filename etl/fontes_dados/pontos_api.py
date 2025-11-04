import requests
from datetime import datetime, timedelta
from typing import List, Dict
from etl.utils.token import get_ifractal_token
from etl.utils.config import API_URL, API_USER

headers = {
    'Content-Type': 'application/json',
    'User': API_USER,
    'Token': get_ifractal_token(),
}

body = {
    'pag': 'ponto_dia',
    'cmd': 'get',
    'data':'21/09/2025',
}

def fetch_pontos_data() -> List[Dict[str, str]]:
    dados = []
    data_do_loop = datetime.strptime(body['data'], "%d/%m/%Y")
    today = datetime.today()

    while data_do_loop <= today:
        body['data'] = data_do_loop.strftime("%d/%m/%Y")
        print("Buscando:", body['data'])

        resp = requests.post(API_URL, json=body, headers=headers,timeout=(15, 300))
        itens = resp.json().get('itens', [])
        if not itens:
            data_do_loop += timedelta(days=1)
            continue
        dados.extend(itens)
        data_do_loop += timedelta(days=1)
    return dados