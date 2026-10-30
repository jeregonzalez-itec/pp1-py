from sqlmodel import Session, create_engine

# SQLite: base de datos local (un archivo en la raíz del proyecto)
URL = "sqlite:///./veterinaria.db"

# check_same_thread=False: FastAPI atiende los requests en distintos hilos
engine = create_engine(URL, connect_args={"check_same_thread": False})


def get_db():
    """Dependencia que se inyecta en los Path Operations (una sesión por request)."""
    with Session(engine) as session:
        yield session
