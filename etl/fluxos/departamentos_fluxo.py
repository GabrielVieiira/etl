from prefect import flow, task
from etl.fontes_dados.departamentos_api import fetch_departamentos_data
from etl.transformacoes.departamentos import transform_departamentos
from etl.loaders.postgres_loader import load_db
from etl.schemas import Departamento

@task(name="📥 Buscar dados departamentos da API")
def fetch_departamento_task() -> list[dict]:
    return fetch_departamentos_data()

@task(name="🧹 Transformar departamentos com pandas + Pydantic")
def transform_departamento_task(raw: list[dict]) -> list[Departamento]:
    return transform_departamentos(raw)

@task(name="📤 Inserir departamentos no banco de dados")
def load_departamento_task(data: list[Departamento]):
    load_db(data,'original.departamentos')

@flow(name="ETL departamentos RH (pandas + requests)")
def etl_departamentos_flow():
    raw_data = fetch_departamento_task()
    clean_data = transform_departamento_task(raw_data)
    load_departamento_task(clean_data)

if __name__ == "__main__":
    etl_departamentos_flow()