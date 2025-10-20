from prefect import flow, task
from etl.fontes_dados.cargos_api import fetch_cargos_data
from etl.transformacoes.cargos import transform_cargos
from etl.loaders.postgres_loader import load_db
from etl.schemas import Cargo

@task(name="📥 Buscar dados cagos da API")
def fetch_cargo_task() -> list[dict]:
    return fetch_cargos_data()

@task(name="🧹 Transformar cargos com pandas + Pydantic")
def transform_cargo_task(raw: list[dict]) -> list[Cargo]:
    return transform_cargos(raw)

@task(name="📤 Inserir cargos no banco de dados")
def load_cargo_task(data: list[Cargo]):
    load_db(data,'original.cargos')

@flow(name="ETL Cargos RH (pandas + requests)")
def etl_cargos_flow():
    raw_data = fetch_cargo_task()
    clean_data = transform_cargo_task(raw_data)
    load_cargo_task(clean_data)

if __name__ == "__main__":
    etl_cargos_flow()