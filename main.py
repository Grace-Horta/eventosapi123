from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base

# 1. IMPORTAR TODOS LOS MODELOS PARA QUE SQLAlchemy LOS RECONOZCA
from app.models.usuario import Usuario
from app.models.facultad import Facultad
from app.models.evento import Evento
from app.models.asistencia import Asistencia
# (Si tienes más modelos definidos en tu carpeta app/models/, impórtalos aquí también)

# 2. IMPORTAR LAS RUTAS (APIS)
from app.api.rutas_usuarios import router as usuarios_router
from app.api.rutas_facultades import router as facultades_router
from app.api.rutas_eventos import router as eventos_router
from app.api.rutas_asistencias import router as asistencias_router
from app.api.rutas_ubicaciones import router as ubicaciones_router
from app.api.rutas_categorias import router as categorias_router
from app.api.rutas_organizadores import router as organizadores_router
from app.api.rutas_programas import router as programas_router
from app.api.rutas_inscripciones import router as inscripciones_router

# 3. IMPORTAR EL SEED (Opcional si deseas sembrar datos al iniciar)
from app.core.seed import sembrar_usuarios

app = FastAPI(
    title="Sistema de Gestión de Eventos Académicos",
    version="1.0.0",
    description="API modular desarrollada con FastAPI y PostgreSQL (Neon) para evaluación académica."
)

# Configuración de CORS para permitir la comunicación con el frontend en Svelte
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. CREAR AUTOMÁTICAMENTE LAS TABLAS EN NEON AL ARRANCAR
Base.metadata.create_all(bind=engine)

# 5. REGISTRAR TODOS LOS ROUTERS
app.include_router(usuarios_router)
app.include_router(facultades_router)
app.include_router(eventos_router)
app.include_router(asistencias_router)
app.include_router(ubicaciones_router)
app.include_router(categorias_router)
app.include_router(organizadores_router)
app.include_router(programas_router)
app.include_router(inscripciones_router)

@app.on_event("startup")
def startup_event():
    # Ejecutar siembra de datos iniciales si corresponde
    try:
        sembrar_usuarios()
    except Exception as e:
        print(f"Aviso en seed: {e}")

@app.get("/", tags=["Root"])
def read_root():
    return {"mensaje": "¡Bienvenido a la API de Gestión de Eventos Académicos!", "docs": "/docs"}