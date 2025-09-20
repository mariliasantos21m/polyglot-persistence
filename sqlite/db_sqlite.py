from sqlalchemy import create_engine

def get_sqlite_engine():
    """
    Cria e retorna uma engine de conexão com o banco de dados SQLite.
    """
    try:
        engine = create_engine("sqlite:///locations.db")
        return engine
    except Exception as e:
        print(f"Erro ao conectar com o SQLite: {e}")
        return None