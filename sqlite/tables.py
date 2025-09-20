from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlite.db_sqlite import metadata;

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