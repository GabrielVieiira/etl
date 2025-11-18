import pandas as pd
from typing import Any, List
from etl.schemas import Funcionario

COLUNAS_RELEVANTES = [
    'codigo',
    'matricula',
    'nome',
    'cpf',
    'cod_cargo',
    'cod_unidade',
    'cod_tipo',
    'cod_centro_custo',
    'centro_custo_nro',
    'dtadmissao',
    'dtdemissao',
    'dtnascimento',
    'idade',
    'tempo_casa',
    'cod_empresa',
    'salario',
]

COLUNAS_RENAME = {

    'cod_unidade':'cod_departamento',
    'cod_centro_custo':'cod_regional',
    'centro_custo_nro':'regional_nro',
}

def transform_funcionarios(raw_data: List[dict[str,Any]]) -> List[Funcionario]:
    df = pd.DataFrame(raw_data)
    df = df[[col for col in COLUNAS_RELEVANTES if col in df.columns]]
    df = df.rename(columns=COLUNAS_RENAME)
    df = df.drop_duplicates(subset=['codigo'])
    df.fillna(value=pd.NA, inplace=True)
    try:
        funcionarios = df.to_dict(orient='records')
        return [Funcionario(**row) for row in funcionarios] #type: ignore
    except Exception as e:
        raise ValueError(f'[!] Validação com Pydantic dos funcionarios falhou: {e}')