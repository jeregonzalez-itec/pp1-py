LEVANTO ENTORNO VIRTUAL DE FASTAPI EN WINDOWS CON:
    - .\venv\Scripts\activate 


LEVANTO EL SERVIDOR CON :
    - fastapi dev src/main.py

PREPARO CON UN COMMIT LA MIGRACION DE LA DB CON ALEMBIC MEDIANTE ESTE COMANDO:
    - alembic revision --autogenerate -m "Primera migracion"

'PUSHEO' LA MIGRACION CON :
    - alembic upgrade head 