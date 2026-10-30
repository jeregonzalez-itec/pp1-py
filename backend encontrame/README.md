# 🐾 API Veterinaria NFC

**EFI – Práctica Profesionalizante I: Python (ITEC Río Cuarto, 2026)**
Docente: Facundo Esteban Lemo · Carrera: Desarrollo de Software

API REST hecha con **FastAPI + SQLModel + Alembic** para gestionar veterinarias, tags NFC/QR, mascotas y sus dueños. Cada mascota se identifica con un tag NFC emitido por una veterinaria.

## 👥 Integrantes

- Nombre Apellido
- Nombre Apellido
- Nombre Apellido
- Nombre Apellido

## 🧱 Modelo de datos

```
Veterinaria 1 ──< TagNFC 1 ── 1 Mascota >── 1 Usuario (dueño)
```

| Tabla | Relaciones (FK) |
|---|---|
| `veterinaria` | – |
| `tagnfc` | `veterinaria_id → veterinaria.id` |
| `mascota` | `tag_id → tagnfc.id` (único), `usuario_id → usuario.id` |
| `usuario` | – |

Cada archivo de `models/` tiene sus clases `Base`, la principal (`table=True`) y `Public`. Los schemas `Nested` (con relaciones anidadas) están en `models/anidados.py`.

## 📁 Estructura

```
.
├── alembic/                # Entorno de migraciones
│   ├── env.py
│   └── versions/           # Migraciones registradas
├── alembic.ini
├── requirements.txt
├── README.md
└── src/
    ├── main.py             # App FastAPI, CORS, routers, paginación
    ├── database.py         # Engine SQLite + get_db
    ├── core/               # auth (bcrypt + JWT), dependencies, utils
    ├── models/             # SQLModel: Base / table / Public / Nested
    └── routers/            # CRUD por modelo + auth
```

## ⚙️ Instalación

```bash
# Con uv (recomendado)
uv venv
.venv\Scripts\activate                   # Windows
uv pip install -r requirements.txt

# O con venv clásico
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## 🗄️ Base de datos (migraciones)

Ejecutar siempre desde la raíz del proyecto:

```bash
alembic upgrade head                                # crea las tablas
alembic revision --autogenerate -m "descripcion"    # nueva migración tras cambiar un modelo
```

## ▶️ Ejecutar

```bash
fastapi dev src/main.py
```

- Swagger: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc

Variable opcional: `SECRET_KEY` (clave para firmar los JWT).

## 🔌 Endpoints

| Recurso | Prefijo | Operaciones |
|---|---|---|
| Veterinarias | `/veterinarias` | GET (paginado) · GET `/{id}` · POST · PUT `/{id}` · DELETE `/{id}` |
| Tags NFC | `/tags` | ídem |
| Mascotas | `/mascotas` | ídem |
| Usuarios | `/usuarios` | ídem |
| Auth | `/auth` | POST `/register` · POST `/login` · GET `/me` (JWT) |

- Los listados son paginados: `?page=1&size=50`.
- `DELETE` acepta `?logico=true` para baja lógica.
- Los endpoints por id devuelven **404** (documentado en `/docs`); los duplicados devuelven **409**.

## 🌿 Flujo de Git (GitFlow)

`main` (producción) ← `develop` ← `feature/*`. Cada integrante trabaja en `feature/nombre-de-la-tarea`, abre un Pull Request a `develop` y al cerrar la entrega se mergea `develop` a `main`.
