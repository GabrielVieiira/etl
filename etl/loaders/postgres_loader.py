from typing import Any
from etl.utils.config import DATABASE_URL
from sqlalchemy import create_engine, MetaData, Table, insert
from sqlalchemy.dialects.postgresql import insert as pg_insert

def load_db(data: list[Any], table_name: str) -> None:
    engine = create_engine(DATABASE_URL)
    metadata = MetaData()
    metadata.reflect(bind=engine, schema='original')
    table: Table = metadata.tables[table_name]
    dialect = engine.dialect.name

    registros = [obj.dict() for obj in data]

    with engine.begin() as connection:
        colunas = table.columns.keys()
        tem_codigo = "codigo" in colunas
        tem_id = "id" in colunas

        if not registros:
            return

        if dialect == "postgresql":
            stmt = pg_insert(table).values(registros)

            if tem_codigo or tem_id:
                chave = "codigo" if tem_codigo else "id"
                stmt = stmt.on_conflict_do_update(
                    index_elements=[chave],
                    set_={k: stmt.excluded[k] for k in registros[0] if k != chave}
                )
            connection.execute(stmt)
        else:
            stmt = insert(table)
            connection.execute(stmt, registros)