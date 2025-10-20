from prefect import flow, task
from etl.fontes_dados.funcionarios_api import fetch_funcionarios_data
from etl.transformacoes.funcionarios import transform_funcionarios
from etl.loaders.postgres_loader import load_db
from etl.schemas.funcionarios import Funcionario

@task(name="📥 Buscar dados da API")
def fetch_task() -> list[dict]:
    return fetch_funcionarios_data()

@task(name="🧹 Transformar com pandas + Pydantic")
def transform_task(raw: list[dict]) -> list[Funcionario]:
    return transform_funcionarios(raw)

@task(name="📤 Inserir no banco de dados")
def load_task(data: list[Funcionario]):
    load_db(data,'original.funcionarios')

@flow(name="ETL Funcionários RH (pandas + requests)")
def etl_funcionarios_flow():
    raw_data = fetch_task()
    clean_data = transform_task(raw_data)
    load_task(clean_data)

if __name__ == "__main__":
    etl_funcionarios_flow()