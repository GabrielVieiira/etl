from pydantic import BaseModel
from typing import Optional

class Funcionario(BaseModel):
    codigo:             int
    matricula:          Optional[str]
    nome:               str
    cpf:                Optional[str]
    cod_cargo:          Optional[int]
    cod_departamento:   Optional[int]
    cod_tipo:           Optional[str]
    cod_regional:       Optional[int]
    regional_nro:       Optional[int]
    dtadmissao:         Optional[str]
    dtdemissao:         Optional[str]
    dtnascimento:       Optional[str]
    idade:              Optional[int]
    tempo_casa:         Optional[int]
    cod_empresa:        Optional[int]
    salario:            Optional[float]