"""Fábrica de rutas CRUD (GET lista, GET uno, POST, PUT, DELETE) con control de roles."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import requiere_roles


def _guardar(db: Session):
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un registro con esos datos o está relacionado con otros registros.",
        )


def crear_crud(prefix, tag, Modelo, Schema,
               roles_ver=(), roles_crear=("Administrador",), roles_editar=("Administrador",)):
    """
    roles_ver=()   -> cualquier usuario con sesión iniciada puede consultar.
    roles_crear    -> quién puede hacer POST.
    roles_editar   -> quién puede hacer PUT y DELETE.
    """
    router = APIRouter(prefix=prefix, tags=[tag])
    dep_ver = Depends(requiere_roles(*roles_ver))
    dep_crear = Depends(requiere_roles(*roles_crear))
    dep_editar = Depends(requiere_roles(*roles_editar))

    def _obtener(db: Session, item_id: int):
        item = db.query(Modelo).filter(Modelo.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        return item

    @router.get("/")
    def listar(db: Session = Depends(get_db), _u=dep_ver):
        return db.query(Modelo).order_by(Modelo.id).all()

    @router.get("/{item_id}")
    def obtener(item_id: int, db: Session = Depends(get_db), _u=dep_ver):
        return _obtener(db, item_id)

    @router.post("/", status_code=status.HTTP_201_CREATED)
    def crear(datos: Schema, db: Session = Depends(get_db), _u=dep_crear):
        nuevo = Modelo(**datos.model_dump())
        db.add(nuevo)
        _guardar(db)
        db.refresh(nuevo)
        return nuevo

    @router.put("/{item_id}")
    def actualizar(item_id: int, datos: Schema, db: Session = Depends(get_db), _u=dep_editar):
        item = _obtener(db, item_id)
        for clave, valor in datos.model_dump().items():
            setattr(item, clave, valor)
        _guardar(db)
        db.refresh(item)
        return item

    @router.delete("/{item_id}")
    def eliminar(item_id: int, db: Session = Depends(get_db), _u=dep_editar):
        item = _obtener(db, item_id)
        db.delete(item)
        _guardar(db)
        return {"mensaje": "Registro eliminado"}

    return router
