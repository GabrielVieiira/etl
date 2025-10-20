import pandas as pd
from typing import Any, List
from etl.schemas import JustificativaAbono

COLUNAS_RELEVANTES = [
    'codigo',
    'cod_empresa',
    'dtcadastro',
    'nome',
    'descricao',
    'dtapago',
    'abreviacao_escala',
    'abreviacao_espelho',
]

def transform_justificativas_abono(raw_data:List[dict[str,Any]]) -> List[JustificativaAbono]:
    df = pd.DataFrame(raw_data)
    df = df[[col for col in COLUNAS_RELEVANTES if col in df.columns]]
    df.fillna(value=pd.NA, inplace=True)
    try:
        justificativas_abono = df.to_dict(orient='records')
        return [JustificativaAbono(**row) for row in justificativas_abono] #type: ignore
    except Exception as e:
        raise ValueError(f'[!] Validação com Pydantic das justificativas de abono falhou: {e}')