import pandas as pd
from typing import Any, List
from etl.schemas import Regional

COLUNAS_RELEVANTES = [
    'codigo',
    'nome',
    'nro',
    'cod_empresa',
    'qtd_pessoa'
]

def transform_regionais(raw_data:List[dict[str,Any]]) -> List[Regional]:
    df = pd.DataFrame(raw_data)
    df = df[[col for col in COLUNAS_RELEVANTES if col in df.columns]]
    df = df.drop_duplicates(subset=['codigo'])
    df.fillna(value=pd.NA, inplace=True)
    try:
        regionais = df.to_dict(orient='records')
        return [Regional(**row) for row in regionais] #type: ignore
    except Exception as e:
        raise ValueError(f'[!] Validação com Pydantic das regionais falhou: {e}')