from sqlalchemy import select
from sqlite.db_sqlite import get_sqlite_engine, metadata
from sqlite.tables import tb_countries, tb_states, tb_cities

def get_countries():
    engine = get_sqlite_engine()
    if engine is None: return []

    with engine.connect() as conn:
        result= conn.execute(select(tb_countries))
        return result.fetchall()
    
def get_states():
    engine = get_sqlite_engine()
    if engine is None: return []

    with engine.connect() as conn:
        result= conn.execute(select(tb_states))
        return result.fetchall()
    
def get_cities():
    engine = get_sqlite_engine()
    if engine is None: return []
    
    with engine.connect() as conn:
        result= conn.execute(select(tb_cities))
        return result.fetchall()