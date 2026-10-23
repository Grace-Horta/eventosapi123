from app.core.database import get_db_connection
from app.models.usuario import UsuarioBase

class UsuarioRepository:
    @staticmethod
    def crear(data: UsuarioBase):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO Usuarios (nombre, apellido, documento_identidad, telefono, email, password, semestre, id_rol, id_programa)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_usuario;
            """
            cursor.execute(query, (
                data.nombre, data.apellido, data.documento_identidad,
                data.telefono, data.email, data.password,
                data.semestre, data.id_rol, data.id_programa
            ))
            id_generado = cursor.fetchone()[0]
            conn.commit()
            return id_generado
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()