from prefect import flow, task
from etl.fontes_dados.entregaveis_api import fetch_entregaveis
from etl.transformacoes.entregaveis import transform_entregaveis
from etl.loaders.postgres_loader import load_db
from etl.schemas import Entregaveis

@task(name="📥 Buscar dados de entregaveis da API")
def fetch_entregaveis_task() -> list[dict]:
    return fetch_entregaveis()

@task(name="🧹 Transformar entregaveis com pandas + Pydantic")
def transform_entregaveis_task(raw: list[dict]) -> list[Entregaveis]:
    return transform_entregaveis(raw)

@task(name="📤 Inserir entregaveis no banco de dados")
def load_entregaveis_task(data: list[Entregaveis]) -> None:
    load_db(data,'original.entregaveis')

@flow(name="ETL entregaveis RH")
def etl_entregaveis_flow():
    raw_data = fetch_entregaveis_task()
    clean_data = transform_entregaveis_task(raw_data)
    load_entregaveis_task(clean_data)

if __name__ == "__main__":
    etl_entregaveis_flow()