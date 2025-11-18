from pydantic import BaseModel

class ObsRefeicao(BaseModel):
    id:         int
    data:       str
    lider:      str
    regional:   str
    observacao: str
    quantidade: int