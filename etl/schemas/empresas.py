from pydantic import BaseModel
from typing import Optional

class Empresa(BaseModel):
    codigo:         int
    nome:           str
    qtd_pessoas:    Optional[int]