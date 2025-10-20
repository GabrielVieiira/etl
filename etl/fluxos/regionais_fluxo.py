from prefect import flow, task
from etl.fontes_dados.regionais_api import fetch_centro_custo_data
from etl.transformacoes.regionais import transform_regionais
from etl.loaders.postgres_loader import load_db
from etl.schemas import Regional

@task(name="📥 Buscar dados regionais da API")
def fetch_regionais_task() -> list[dict]:
    return fetch_centro_custo_data()

@task(name="🧹 Transformar regionais com pandas + Pydantic")
def transform_regionais_task(raw: list[dict]) -> list[Regional]:
    return transform_regionais(raw)

@task(name="📤 Inserir regionais no banco de dados")
def load_regionais_task(data: list[Regional]):
    load_db(data,'original.regionais')

@flow(name="ETL regionais RH (pandas + requests)")
def etl_regionais_flow():
    raw_data = fetch_regionais_task()
    clean_data = transform_regionais_task(raw_data)
    load_regionais_task(clean_data)

if __name__ == "__main__":
    etl_regionais_flow()