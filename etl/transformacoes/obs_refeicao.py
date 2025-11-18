from typing import Any, List
from etl.schemas import ObsRefeicao
import pandas as pd
import numpy as np

def transform_obs_refeicao(raw_data:List[dict[str,Any]]) -> List[ObsRefeicao]:
    df = pd.DataFrame(raw_data)
    df = df[df['data'] != ''].reset_index(drop=True)
    df = df.map(lambda x: np.nan if isinstance(x, str) and x.strip() == "" else x)
    df['data'] = pd.to_datetime(df['data'], format="%d/%m/%Y", errors="coerce").dt.strftime("%Y-%m-%d")
    df.fillna({'lider':'','regional':'','observacao':'','quantidade':1}, inplace=True)   
    try:
        obs_refeicao = df.to_dict(orient='records')
        return [ObsRefeicao(**row) for row in obs_refeicao] #type: ignore
    except Exception as e:
        raise ValueError(f'[!] Validação com Pydantic das observações de refeição falhou: {e}')