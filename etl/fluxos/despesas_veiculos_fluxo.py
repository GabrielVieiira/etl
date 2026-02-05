from prefect import flow, task, get_run_logger
from etl.fontes_dados.despesas_veiculos_api import fetch_despesas_veiculos_data
# from etl.transformacoes.despesa_veiculos import transform_despesa_veiculos
# from etl.loaders.postgres_loader import load_db
# from etl.schemas import DespesaVeiculos

@task(name="📥 Buscar dados despesa_veiculos da API")
def fetch_despesas_veiculo_task() -> list[dict]:
    dados = fetch_despesas_veiculos_data()
    logger = get_run_logger()
    for dado in dados:
        logger.info(dado)
    
    return dados

# @task(name="🧹 Transformar despesa_veiculos com pandas + Pydantic")
# def transform_despesa_veiculo_task(raw: list[dict]) -> list[DespesaVeiculos]:
#     return transform_despesa_veiculos(raw)

# @task(name="📤 Inserir despesa_veiculos no banco de dados")
# def load_despesa_veiculo_task(data: list[despesa_veiculo]):
#     load_db(data,'original.despesa_veiculos')

@flow(name="ETL despesa_veiculos RH (pandas + requests)")
def etl_despesa_veiculos_flow():
    raw_data = fetch_despesas_veiculo_task()
    # clean_data = transform_despesa_veiculo_task(raw_data)
    # load_despesa_veiculo_task(clean_data)

if __name__ == "__main__":
    etl_despesa_veiculos_flow()