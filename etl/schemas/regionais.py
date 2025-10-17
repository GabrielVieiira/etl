from pydantic import BaseModel
from typing import Optional

class Regional(BaseModel):
    codigo:         int
    nome:           str
    nro:            int
    cod_empresa:    int
    qtd_pessoa:     Optional[int]