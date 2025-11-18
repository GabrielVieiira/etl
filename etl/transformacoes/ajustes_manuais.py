from typing import Any, List
from etl.schemas import AjusteManual
import pandas as pd

COLUNAS_DATA = [
    'data_recebimento',
    'data_evento'
]

def transform_ajustes_manuais(raw_data:List[dict[str,Any]]) -> List[AjusteManual]:
    df = pd.DataFrame(raw_data)
    for col in COLUNAS_DATA:
        df[col] = pd.to_datetime(df[col], format="%d/%m/%Y", errors="coerce").dt.strftime("%Y-%m-%d")
    try:
        ajustes_manuais = df.to_dict(orient='records')
        return [AjusteManual(**row) for row in ajustes_manuais] #type: ignore
    except Exception as e:
        raise ValueError(f'[!] Validação com Pydantic dos ajustes manuais falhou: {e}')