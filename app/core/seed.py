from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.usuario import Usuario

# ⚠️ EDITA ESTOS CORREOS Y CONTRASEÑAS ANTES DE LA PRIMERA EJECUCIÓN.
# Solo estos correos podrán entrar al sistema (más los que el administrador cree en /usuarios).
# Se insertan únicamente si la tabla "usuarios" está vacía.
USUARIOS_INICIALES = [
    ("Administrador", "gracehorta@email.com", "pass123", "Administrador"),
    ("Docente Demo", "kilian@email.com", "pass123*", "Docente"),
    ("Estudiante Demo", "lucilili@email.com", "pass123*", "Estudiante"),
]


def sembrar_usuarios():
    db = SessionLocal()
    try:
        if db.query(Usuario).count() == 0:
            for nombre, email, password, rol in USUARIOS_INICIALES:
                db.add(Usuario(
                    nombre=nombre,
                    email=email.strip().lower(),
                    password_hash=hash_password(password),
                    rol=rol,
                    activo=True,
                ))
            db.commit()
    finally:
        db.close()
