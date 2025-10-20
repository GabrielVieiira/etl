from prefect import flow, task
from etl.fontes_dados.empresas_api import fetch_empresas_data
from etl.transformacoes.empresas import transform_empresas
from etl.loaders.postgres_loader import load_db
from etl.schemas import Empresa

@task(name="📥 Buscar dados empresas da API")
def fetch_empresas_task() -> list[dict]:
    return fetch_empresas_data()

@task(name="🧹 Transformar empresas com pandas + Pydantic")
def transform_empresas_task(raw: list[dict]) -> list[Empresa]:
    return transform_empresas(raw)

@task(name="📤 Inserir empresas no banco de dados")
def load_empresas_task(data: list[Empresa]):
    load_db(data,'original.empresas')

@flow(name="ETL empresas RH (pandas + requests)")
def etl_empresas_flow():
    raw_data = fetch_empresas_task()
    clean_data = transform_empresas_task(raw_data)
    load_empresas_task(clean_data)

if __name__ == "__main__":
    etl_empresas_flow()