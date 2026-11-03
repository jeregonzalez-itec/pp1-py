===== ENCONTRAME API — Comandos de desarrollo =====

--- ENTORNO VIRTUAL ---
Activar (Windows PowerShell):
    .\.venv\Scripts\activate

Desactivar:
    deactivate

--- SERVIDOR ---
Levantar en modo desarrollo (hot-reload):
    fastapi dev src/main.py

La API queda disponible en:
    http://127.0.0.1:8000
    http://127.0.0.1:8000/docs  (Swagger UI interactivo)

--- BASE DE DATOS (Alembic) ---
Generar nueva migración (tras cambiar modelos):
    alembic revision --autogenerate -m "descripcion_del_cambio"

Aplicar migraciones pendientes:
    alembic upgrade head

Verificar que el schema está sincronizado (sin drift):
    alembic check

Ver historial de migraciones:
    alembic history --verbose

--- DEPENDENCIAS ---
Instalar desde requirements.txt:
    pip install -r requirements.txt

Actualizar requirements.txt con las versiones instaladas:
    pip freeze > requirements.txt

--- NOTA (solo la primera vez en Windows) ---
Si PowerShell bloquea la ejecucion de scripts:
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

