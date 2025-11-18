from prefect import flow, task
from etl.fontes_dados.obs_refeicoes_api import fetch_obs_refeicao_data
from etl.transformacoes.obs_refeicao import transform_obs_refeicao
from etl.loaders.postgres_loader import load_db
from etl.schemas import ObsRefeicao

@task(name="📥 Buscar dados de observações de refeição da API")
def fetch_obs_refeicao_task() -> list[dict]:
    return fetch_obs_refeicao_data()

@task(name="🧹 Transformar observações de refeição com pandas + Pydantic")
def transform_obs_refeicao_task(raw: list[dict]) -> list[ObsRefeicao]:
    return transform_obs_refeicao(raw)

@task(name="📤 Inserir observações de refeição no banco de dados")
def load_obs_refeicao_task(data: list[ObsRefeicao]) -> None:
    load_db(data,'original.obs_refeicao')

@flow(name="ETL observações de refeição RH", log_prints=True)
def etl_obs_refeicao_flow():
    raw_data = fetch_obs_refeicao_task()
    clean_data = transform_obs_refeicao_task(raw_data)
    load_obs_refeicao_task(clean_data)

if __name__ == "__main__":
    etl_obs_refeicao_flow()