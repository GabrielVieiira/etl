import pandas as pd
from typing import Any, List
from etl.schemas import Empresa

COLUNAS_RELEVANTES = [
    'codigo',
    'nome',
    'qtd_pessoa'
]

def transform_empresas(raw_data:List[dict[str,Any]]) -> List[Empresa]:
    df = pd.DataFrame(raw_data)
    df = df[[col for col in COLUNAS_RELEVANTES if col in df.columns]]
    df = df.drop_duplicates(subset=['codigo'])
    df.fillna(value=pd.NA, inplace=True)
    try:
        empresas = df.to_dict(orient='records')
        return [Empresa(**row) for row in empresas] #type: ignore
    except Exception as e:
        raise ValueError(f'[!] Validação com Pydantic das empresas falhou: {e}')