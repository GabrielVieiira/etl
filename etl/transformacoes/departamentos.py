import pandas as pd
from typing import Any, List
from etl.schemas import Departamento

COLUNAS_RELEVANTES = [
    'codigo',
    'nome',
    'nro',
    'cod_empresa',
    'qtd_pessoa'
]

def transform_departamentos(raw_data:List[dict[str,Any]]) -> List[Departamento]:
    df = pd.DataFrame(raw_data)
    df = df[[col for col in COLUNAS_RELEVANTES if col in df.columns]]
    df.fillna(value=pd.NA, inplace=True)
    try:
        departamentos = df.to_dict(orient='records')
        return [Departamento(**row) for row in departamentos] #type: ignore
    except Exception as e:
        raise ValueError(f'[!] Validação com Pydantic dos departamentos falhou: {e}')