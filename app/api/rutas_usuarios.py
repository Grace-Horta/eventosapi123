from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    crear_token, get_usuario_actual, hash_password, requiere_roles, verificar_password,
)
from app.models.usuario import Usuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

Rol = Literal["Administrador", "Docente", "Estudiante"]


class LoginSchema(BaseModel):
    email: str
    password: str


class UsuarioSchema(BaseModel):
    nombre: str = Field(min_length=1)
    email: str = Field(min_length=3)
    rol: Rol
    password: Optional[str] = None  # obligatoria al crear; opcional al editar
    activo: bool = True


def _out(u: Usuario) -> dict:
    # Nunca se devuelve el hash de la contraseña
    return {"id": u.id, "nombre": u.nombre, "email": u.email, "rol": u.rol, "activo": u.activo}


def _guardar(db: Session):
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Ya existe un usuario con ese correo.")


@router.post("/login")
def login(datos: LoginSchema, db: Session = Depends(get_db)):
    email = datos.email.strip().lower()
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario or not usuario.activo or not verificar_password(datos.password, usuario.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Correo o contraseña incorrectos")
    return {"token": crear_token(usuario), "usuario": _out(usuario)}


@router.get("/me")
def me(usuario: Usuario = Depends(get_usuario_actual)):
    return _out(usuario)


_admin = Depends(requiere_roles("Administrador"))


@router.get("/")
def listar(db: Session = Depends(get_db), _a=_admin):
    return [_out(u) for u in db.query(Usuario).order_by(Usuario.id).all()]


@router.post("/", status_code=status.HTTP_201_CREATED)
def crear(datos: UsuarioSchema, db: Session = Depends(get_db), _a=_admin):
    if not datos.password or len(datos.password) < 8:
        raise HTTPException(status_code=422, detail="La contraseña debe tener al menos 8 caracteres.")
    nuevo = Usuario(
        nombre=datos.nombre.strip(),
        email=datos.email.strip().lower(),
        password_hash=hash_password(datos.password),
        rol=datos.rol,
        activo=datos.activo,
    )
    db.add(nuevo)
    _guardar(db)
    db.refresh(nuevo)
    return _out(nuevo)


@router.put("/{usuario_id}")
def actualizar(usuario_id: int, datos: UsuarioSchema, db: Session = Depends(get_db),
               actual: Usuario = _admin):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if usuario.id == actual.id and (datos.rol != "Administrador" or not datos.activo):
        raise HTTPException(status_code=400, detail="No puedes quitarte tu propio rol de administrador ni desactivarte.")
    usuario.nombre = datos.nombre.strip()
    usuario.email = datos.email.strip().lower()
    usuario.rol = datos.rol
    usuario.activo = datos.activo
    if datos.password:
        if len(datos.password) < 8:
            raise HTTPException(status_code=422, detail="La contraseña debe tener al menos 8 caracteres.")
        usuario.password_hash = hash_password(datos.password)
    _guardar(db)
    db.refresh(usuario)
    return _out(usuario)


@router.delete("/{usuario_id}")
def eliminar(usuario_id: int, db: Session = Depends(get_db), actual: Usuario = _admin):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if usuario.id == actual.id:
        raise HTTPException(status_code=400, detail="No puedes eliminar tu propio usuario.")
    db.delete(usuario)
    _guardar(db)
    return {"mensaje": "Usuario eliminado"}
