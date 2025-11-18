from pydantic import BaseModel

class ControleRefeicao(BaseModel):
    id:         int
    data:       str
    lider:      str
    regional:   str
    qtd_otima:  int
    qtd_boa:    int
    qtd_ruim:   int