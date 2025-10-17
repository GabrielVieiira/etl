from typing import Optional
from pydantic import BaseModel

class Cargo(BaseModel):
    codigo:     int
    nome:       str
    cod_epresa: int
    qtd_pessoa: Optional[int]