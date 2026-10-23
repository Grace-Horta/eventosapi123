from app.core.database import get_db_connection
from app.models.rol import RolBase

class RolRepository:
    @staticmethod
    def crear(data: RolBase):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Roles (nombre) VALUES (%s) RETURNING id_rol;", (data.nombre,))
            id_generado = cursor.fetchone()[0]
            conn.commit()
            return id_generado
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()