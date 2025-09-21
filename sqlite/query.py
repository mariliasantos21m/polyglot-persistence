from sqlalchemy import select, insert
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

def create(city: str, state: str, country: str):
    engine = get_sqlite_engine()

    with engine.connect() as conn:
        result_country= conn.execute(
            select(tb_countries.c.id)
            .where(tb_countries.c.name == country)
        ).fetchone()

        if not result_country:
            result_country= conn.execute(insert(tb_countries).values(name=country))
            result_country = result_country.inserted_primary_key
        
        result_state= conn.execute(
            select(tb_states.c.id)
            .where((tb_states.c.name == state) & (tb_states.c.country_id == result_country[0]))
        ).fetchone()

        if not result_state:
            result_state= conn.execute(insert(tb_states).values(name=state, country_id=result_country[0]))
            result_state = result_state.inserted_primary_key

        result_city= conn.execute(
            select(tb_cities.c.id)
            .where(tb_cities.c.name == city and tb_cities.c.state_id == result_state[0])
        ).fetchone()

        if not result_city:
            result_city= conn.execute(insert(tb_cities).values(name=city, state_id=result_state[0]))
