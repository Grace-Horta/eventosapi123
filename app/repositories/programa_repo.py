from app.core.database import get_db_connection
from app.models.programa import ProgramaBase

class ProgramaRepository:
    @staticmethod
    def crear(data: ProgramaBase):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Programas (nombre, id_facultad) VALUES (%s, %s) RETURNING id_programa;", (data.nombre, data.id_facultad))
            id_generado = cursor.fetchone()[0]
            conn.commit()
            return id_generado
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()