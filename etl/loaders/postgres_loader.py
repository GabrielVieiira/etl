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

    # Converte lista de modelos Pydantic em lista de dicts
    registros = [obj.dict() for obj in data]

    with engine.begin() as connection:
        if not registros:
            return

        if dialect == "postgresql":
            # Inserção com upsert (INSERT ... ON CONFLICT DO UPDATE)
            stmt = pg_insert(table).values(registros)
            stmt = stmt.on_conflict_do_update(
                index_elements=["codigo"],
                set_={k: stmt.excluded[k] for k in registros[0] if k != "codigo"}
            )
            connection.execute(stmt)
        else:
            # Inserção simples em lote para SQLite ou outros
            stmt = insert(table)
            connection.execute(stmt, registros)