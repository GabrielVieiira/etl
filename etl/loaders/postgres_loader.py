from typing import Any
from sqlalchemy import create_engine, MetaData, Table, text, insert
from etl.utils.config import DATABASE_URL
from etl.schemas.funcionarios import Funcionario

def load_db(data: list[Any], table_name: str) -> None:
    """
    Insere ou atualiza dados na tabela 'funcionarios', adaptando-se automaticamente
    ao banco de dados (PostgreSQL ou SQLite).

    Parâmetros:
    - funcionarios: Lista de objetos validados com Pydantic
    - table_name: Nome da tabela de destino (padrão: 'funcionarios')
    """

    engine = create_engine(DATABASE_URL)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table: Table = metadata.tables[table_name]
    dialect = engine.dialect.name
    with engine.begin() as connection:
        for funcionario in data:
            dados = funcionario.dict()
            if dialect == "postgresql":
                statement = insert(table).values(**dados)
                statement = statement.on_conflict_do_update(
                    index_elements=["codigo"],
                    set_={k: statement.excluded[k] for k in dados if k != "codigo"}
                )
                connection.execute(statement)

            elif dialect == "sqlite":
                colunas = ", ".join(dados.keys())
                valores = ", ".join([f":{chave}" for chave in dados])
                query = f"INSERT OR REPLACE INTO {table_name} ({colunas}) VALUES ({valores})"
                connection.execute(text(query), dados)
            else:
                raise NotImplementedError(f"Banco '{dialect}' ainda não é suportado.")