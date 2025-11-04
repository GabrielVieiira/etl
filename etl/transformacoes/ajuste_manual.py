from typing import Any, List
from etl.schemas import AjusteManual

def transform_ajuste_manual(raw_data:List[dict[str,Any]]) -> List[AjusteManual]:
    try:
        return [AjusteManual(**row) for row in raw_data] #type: ignore
    except Exception as e:
        raise ValueError(f'[!] Validação com Pydantic dos ajustes manuais falhou: {e}')