from prefect import flow, task
from etl.fontes_dados.check_lists_api import fetch_check_lists_data
from etl.transformacoes.check_lists import transform_check_lists
from etl.loaders.postgres_loader import load_db
from etl.schemas import CheckList

@task(name="📥 Buscar dados check lists da API")
def fetch_check_lists_task() -> list[dict]:
    return fetch_check_lists_data()

@task(name="🧹 Transformar check lists com pandas + Pydantic")
def transform_check_lists_task(raw: list[dict]) -> list[CheckList]:
    return transform_check_lists(raw)

@task(name="📤 Inserir check lists no banco de dados")
def load_check_lists_task(data: list[CheckList]) -> None:
    load_db(data,'original.checklists')

@flow(name="ETL check lists RH")
def etl_check_lists_flow():
    raw_data = fetch_check_lists_task()
    clean_data = transform_check_lists_task(raw_data)
    load_check_lists_task(clean_data)

if __name__ == "__main__":
    etl_check_lists_flow()