from prefect import flow, task
from etl.fontes_dados.ajuste_manual_api import fetch_ajuste_manual_data
from etl.transformacoes.ajuste_manual import transform_ajuste_manual
from etl.loaders.postgres_loader import load_db
from etl.schemas import AjusteManual

@task(name="📥 Buscar dados ajustes manuais da API")
def fetch_ajuste_manual_task() -> list[dict]:
    return fetch_ajuste_manual_data()

@task(name="🧹 Transformar ajustes manuais com pandas + Pydantic")
def transform_ajuste_manual_task(raw: list[dict]) -> list[AjusteManual]:
    return transform_ajuste_manual(raw)

@task(name="📤 Inserir ajustes manuais no banco de dados")
def load_ajuste_manual_task(data: list[AjusteManual]):
    load_db(data,'original.ajustes_manuais')

@flow(name="ETL ajustes manuais RH")
def etl_ajuste_manual_flow():
    raw_data = fetch_ajuste_manual_task()
    clean_data = transform_ajuste_manual_task(raw_data)
    load_ajuste_manual_task(clean_data)

if __name__ == "__main__":
    etl_ajuste_manual_flow()