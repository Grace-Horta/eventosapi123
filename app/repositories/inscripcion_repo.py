from app.core.database import get_db_connection
from app.models.inscripcion import InscripcionBase

class InscripcionRepository:
    @staticmethod
    def crear(data: InscripcionBase):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Inscripciones (id_estudiante, id_evento) VALUES (%s, %s) RETURNING id_inscripcion;", (data.id_estudiante, data.id_evento))
            id_generado = cursor.fetchone()[0]
            conn.commit()
            return id_generado
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()