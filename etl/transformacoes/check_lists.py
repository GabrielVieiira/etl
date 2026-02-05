from typing import Any, List
from etl.schemas import CheckList
import pandas as pd
import numpy as np

from etl.transformacoes.cargos import COLUNAS_RENAME

COLUNAS_RELEVANTES = [
    'id',
    'Data',
    'Patrimonio',
    'km ou horimetro',
    'Motorista',
    'Checklist ok?',
    'Tipo Patrimonio',
    'Regional',
]

COLUNAS_RENAME = {
    'Data':'data',
    'Patrimonio':'patrimonio',
    'km ou horimetro':'km_ou_horimetro',
    'Motorista':'motorista',
    'Checklist ok?':'checklist_ok',
    'Tipo Patrimonio':'tipo_patrimonio',
    'Regional':'regional',
}

def transform_check_lists(raw_data:List[dict[str,Any]]) -> List[CheckList]:
    df = pd.DataFrame(raw_data)
    df = df[[col for col in COLUNAS_RELEVANTES if col in df.columns]]
    df = df.rename(columns=COLUNAS_RENAME)
    df = df[df['motorista'] != ''].reset_index(drop=True)
    df['data'] = pd.to_datetime(df['data'], format="%d/%m/%Y", errors="coerce").dt.strftime("%Y-%m-%d")
    df['km_ou_horimetro'] = (
        df['km_ou_horimetro']
            .astype(str)
            .str.strip()
            .replace('', np.nan)
            .str.replace(',', '.', regex=False)
            .astype(float)
    )
    try:
        check_lists = df.to_dict(orient='records')
        return [CheckList(**row) for row in check_lists] #type: ignore
    except Exception as e:
        raise ValueError(f'[!] Validação com Pydantic dos check lists falhou: {e}')