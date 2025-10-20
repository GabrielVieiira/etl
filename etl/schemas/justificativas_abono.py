from pydantic import BaseModel
from typing import Optional

class JustificativaAbono(BaseModel):
    codigo:             int
    cod_empresa:        int
    dtcadastro:         str
    nome:               str
    descricao:          Optional[str]
    dtapago:            Optional[str]
    abreviacao_escala:  Optional[str]
    abreviacao_espelho: Optional[str]
