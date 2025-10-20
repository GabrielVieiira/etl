from prefect import flow, task
from etl.fontes_dados.pontos_api import fetch_pontos_data
from etl.transformacoes.pontos import transform_pontos
from etl.loaders.postgres_loader import load_db
from etl.schemas import Regional

@task(name="📥 Buscar dados pontos da API")
def fetch_pontos_task() -> list[dict]:
    return fetch_pontos_data()

@task(name="🧹 Transformar pontos com pandas + Pydantic")
def transform_pontos_task(raw: list[dict]) -> list[Regional]:
    return transform_pontos(raw)

@task(name="📤 Inserir pontos no banco de dados")
def load_pontos_task(data: list[Regional]):
    load_db(data,'original.pontos')

@flow(name="ETL pontos RH (pandas + requests)")
def etl_pontos_flow():
    raw_data = fetch_pontos_task()
    clean_data = transform_pontos_task(raw_data)
    load_pontos_task(clean_data)

if __name__ == "__main__":
    etl_pontos_flow()