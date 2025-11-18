from pydantic import BaseModel

class Entregaveis(BaseModel):
    id:                             int
    data:                           str
    lider:                          str
    regional:                       str
    controle_temperatura:           int
    dds:                            int
    campanha:                       int
    controle_satisfacao_qualidade:  int