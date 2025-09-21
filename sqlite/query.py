from sqlalchemy import select
from sqlite.db_sqlite import get_sqlite_engine, metadata
from sqlite.tables import tb_countries, tb_states, tb_cities

def get_countries():
    engine = get_sqlite_engine()
    if engine is None: return []

    with engine.connect() as conn:
        result= conn.execute(select(tb_countries))
        return result.fetchall()
    
def get_states(country:list[int]):
    engine = get_sqlite_engine()
    if engine is None: return []

    with engine.connect() as conn:
        if(len(country) > 0):
            result= conn.execute(
                select(tb_states)
                .where(tb_states.columns.country_id.in_(country))
            )
            return result.fetchall()
        
        result= conn.execute(select(tb_states))
        return result.fetchall()
    
def get_cities(state:list[int]):
    engine = get_sqlite_engine()
    if engine is None: return []
    
    with engine.connect() as conn:
        if(len(state) > 0):
            result= conn.execute(
                select(tb_cities)
                .where(tb_cities.columns.state_id.in_(state))
            )
            return result.fetchall()
        
        result= conn.execute(select(tb_cities))
        return result.fetchall()