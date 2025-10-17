from pydantic import BaseModel
from typing import Optional

class JustificativaAbono(BaseModel):
    codigo:             int
    cod_empresa:        int
    dt_cadasto:         str
    nome:               str
    descricao:          Optional[str]
    dt_apago:           Optional[str]
    abreviacao_escala:  Optional[str]
    abreviacao_espelho: Optional[str]
