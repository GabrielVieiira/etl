import pandas as pd
from typing import Any, List
from etl.schemas import Cargo

COLUNAS_RELEVANTES = [
    'codigo',
    'nome',
    'cod_empresa',
    'qtd'
]

COLUNAS_RENAME = {
    'qtd':'qtd_pessoa',
}

def transform_cargos(raw_data:List[dict[str,Any]]) -> List[Cargo]:
    df = pd.DataFrame(raw_data)
    df = df[[col for col in COLUNAS_RELEVANTES if col in df.columns]]
    df = df.rename(columns=COLUNAS_RENAME)
    df = df.drop_duplicates(subset=['codigo'])
    df.fillna(value=pd.NA, inplace=True)
    try:
        cargos = df.to_dict(orient='records')
        return [Cargo(**row) for row in cargos] #type: ignore
    except Exception as e:
        raise ValueError(f'[!] Validação com Pydantic dos cargos falhou: {e}')