from typing import Optional
from pydantic import BaseModel

class Departamento(BaseModel):
    codigo:         int
    cod_empresa:    int
    nome:           str
    qtd_pessoa:     Optional[int]
        