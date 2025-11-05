from pydantic import BaseModel
from typing import Optional

class AjusteManual(BaseModel):
    id:                 int  
    data_recebimento:   str
    data_evento:        str
    colaborador:        str
    responsavel:        str
    regional:           str
    tipo:               str
    justificativa:      Optional[str]