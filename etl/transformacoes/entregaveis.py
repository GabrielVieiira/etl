from typing import Any, List
from etl.schemas import Entregaveis
import pandas as pd
import numpy as np

def transform_entregaveis(raw_data:List[dict[str,Any]]) -> List[Entregaveis]:
    df = pd.DataFrame(raw_data)
    df = df[df['data'] != ''].reset_index(drop=True)
    df = df.map(lambda x: np.nan if isinstance(x, str) and x.strip() == "" else x)
    df['data'] = pd.to_datetime(df['data'], format="%d/%m/%Y", errors="coerce").dt.strftime("%Y-%m-%d")
    df.fillna(value=0, inplace=True)
    try:
        entregaveis = df.to_dict(orient='records')
        return [Entregaveis(**row) for row in entregaveis] #type: ignore
    except Exception as e:
        raise ValueError(f'[!] Validação com Pydantic de entregaveis falhou: {e}')