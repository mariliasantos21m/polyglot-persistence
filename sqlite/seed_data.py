from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, insert
from db_sqlite import get_sqlite_engine;

engine = get_sqlite_engine()

metadata = MetaData()
metadata.drop_all(engine)
tb_countries = Table(
    'countries', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String, nullable=False, unique=True)
)


tb_states = Table(
    'states', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String, nullable=False),
    Column('country_id', Integer, ForeignKey('countries.id'), nullable=False)
)


tb_cities =Table(
    'cities', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String, nullable=False),
    Column('state_id', Integer, ForeignKey('states.id'), nullable=False)
)

metadata.create_all(engine)
with engine.connect() as conn:
    transaction = conn.begin()
    try:
        result_brasil= conn.execute(insert(tb_countries).values(name="Brasil"))
        brasil_id = result_brasil.inserted_primary_key[0]

        result_sp = conn.execute(insert(tb_states).values(name="São Paulo", country_id=brasil_id))
        sp_id = result_sp.inserted_primary_key[0]

        result_pb = conn.execute(insert(tb_states).values(name="Paraíba", country_id=brasil_id))
        pb_id = result_pb.inserted_primary_key[0]

        cidades_data = [
            {"name": "São Paulo", "state_id": sp_id},
            {"name": "Campinas", "state_id": sp_id},
            {"name": "Santos", "state_id": sp_id},
            {"name": "Sorocaba", "state_id": sp_id},
            {"name": "Ribeirão Preto", "state_id": sp_id},
            {"name": "João Pessoa", "state_id": pb_id},
            {"name": "Campina Grande", "state_id": pb_id},
            {"name": "Bayeux", "state_id": pb_id},
            {"name": "Santa Rita", "state_id": pb_id},
            {"name": "Patos", "state_id": pb_id},
        ]
        conn.execute(insert(tb_cities), cidades_data)
        
        transaction.commit()
    except:
        transaction.rollback()
        # lança a exceção capturada e tratada(ainda que pacialmente) no except
        raise