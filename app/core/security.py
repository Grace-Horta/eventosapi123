import os
import hashlib
import hmac
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from sqlalchemy.orm import Session

from app.core.database import get_db  # importar database primero carga el .env
from app.models.usuario import Usuario

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("Falta SECRET_KEY en el archivo .env")

TOKEN_HORAS = 8
_serializer = URLSafeTimedSerializer(SECRET_KEY, salt="eventos-auth")
_bearer = HTTPBearer(auto_error=False)


# ---------- Contraseñas (PBKDF2 con sal, solo librería estándar) ----------
def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    h = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return f"{salt.hex()}${h.hex()}"


def verificar_password(password: str, almacenado: str) -> bool:
    try:
        salt_hex, hash_hex = almacenado.split("$")
        salt = bytes.fromhex(salt_hex)
    except ValueError:
        return False
    h = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return hmac.compare_digest(h.hex(), hash_hex)


# ---------- Tokens ----------
def crear_token(usuario: Usuario) -> str:
    return _serializer.dumps({"id": usuario.id})


def get_usuario_actual(
    cred: HTTPAuthorizationCredentials = Depends(_bearer),
    db: Session = Depends(get_db),
) -> Usuario:
    no_autorizado = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Sesión no válida o expirada. Inicia sesión de nuevo.",
    )
    if cred is None:
        raise no_autorizado
    try:
        datos = _serializer.loads(cred.credentials, max_age=TOKEN_HORAS * 3600)
    except (BadSignature, SignatureExpired):
        raise no_autorizado

    usuario = db.query(Usuario).filter(Usuario.id == datos.get("id")).first()
    if not usuario or not usuario.activo:
        raise no_autorizado
    return usuario


def requiere_roles(*roles: str):
    """Sin roles = cualquier usuario autenticado. Con roles = solo esos roles."""
    def dependencia(usuario: Usuario = Depends(get_usuario_actual)) -> Usuario:
        if roles and usuario.rol not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para realizar esta acción.",
            )
        return usuario
    return dependencia
