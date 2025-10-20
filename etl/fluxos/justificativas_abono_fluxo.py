from prefect import flow, task
from etl.fontes_dados.justificativas_abono_api import fetch_justificativas_abono_data
from etl.transformacoes.justificativas_abono import transform_justificativas_abono
from etl.loaders.postgres_loader import load_db
from etl.schemas import JustificativaAbono

@task(name="📥 Buscar dados justificatias abono da API")
def fetch_justificativas_abono_task() -> list[dict]:
    return fetch_justificativas_abono_data()

@task(name="🧹 Transformar justificativas abono com pandas + Pydantic")
def transform_justificativas_abono_task(raw: list[dict]) -> list[JustificativaAbono]:
    return transform_justificativas_abono(raw)

@task(name="📤 Inserir justificativas abono no banco de dados")
def load_justificativas_abono_task(data: list[JustificativaAbono]):
    load_db(data,'original.justificativas')

@flow(name="ETL justificativas abono RH (pandas + requests)")
def etl_justificativas_abono_flow():
    raw_data = fetch_justificativas_abono_task()
    clean_data = transform_justificativas_abono_task(raw_data)
    load_justificativas_abono_task(clean_data)

if __name__ == "__main__":
    etl_justificativas_abono_flow()