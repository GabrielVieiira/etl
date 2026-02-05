from typing import Any, List
from etl.schemas import ControleRefeicao
import pandas as pd
import numpy as np

def transform_controle_refeicoes(raw_data:List[dict[str,Any]]) -> List[ControleRefeicao]:
    df = pd.DataFrame(raw_data)
    df = df[df['data'] != ''].reset_index(drop=True)
    df['id'] = df['id'].astype(int)
    df = df.map(lambda x: np.nan if isinstance(x, str) and x.strip() == "" else x)
    df['data'] = pd.to_datetime(df['data'], format="%d/%m/%Y", errors="coerce").dt.strftime("%Y-%m-%d")
    df.fillna(value=0, inplace=True)
    try:
        controle_refeicoes = df.to_dict(orient='records')
        return [ControleRefeicao(**row) for row in controle_refeicoes] #type: ignore
    except Exception as e:
        raise ValueError(f'[!] Validação com Pydantic do controle de refeição falhou: {e}')