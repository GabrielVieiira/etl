from prefect import flow, task
from etl.fontes_dados.controle_refeicoes_api import fetch_controle_refeicoes_data
from etl.transformacoes.controle_refeicoes import transform_controle_refeicoes
from etl.loaders.postgres_loader import load_db
from etl.schemas import ControleRefeicao

@task(name="📥 Buscar dados controle de refeições da API")
def fetch_controle_refeicoes_task() -> list[dict]:
    return fetch_controle_refeicoes_data()

@task(name="🧹 Transformar controle de refeições com pandas + Pydantic")
def transform_controle_refeicoes_task(raw: list[dict]) -> list[ControleRefeicao]:
    return transform_controle_refeicoes(raw)

@task(name="📤 Inserir controle de refeições no banco de dados")
def load_controle_refeicoes_task(data: list[ControleRefeicao]) -> None:
    load_db(data,'original.controle_refeicoes')

@flow(name="ETL controle de refeições RH")
def etl_controle_refeicoes_flow():
    raw_data = fetch_controle_refeicoes_task()
    clean_data = transform_controle_refeicoes_task(raw_data)
    load_controle_refeicoes_task(clean_data)

if __name__ == "__main__":
    etl_controle_refeicoes_flow()