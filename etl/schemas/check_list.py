from pydantic import BaseModel
from typing import Optional

class CheckList(BaseModel):
    id:                 int
    data:               str
    patrimonio:         str
    km_ou_horimetro:    Optional[float]
    motorista:          str
    checklist_ok:       str
    tipo_patrimonio:    str
    regional:           str