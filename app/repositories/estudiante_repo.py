from app.core.database import get_db_connection
from app.models.estudiante import EstudianteBase

class EstudianteRepository:
    @staticmethod
    def crear(data: EstudianteBase):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Estudiantes (codigo, id_usuario) VALUES (%s, %s) RETURNING id_estudiante;", (data.codigo, data.id_usuario))
            id_generado = cursor.fetchone()[0]
            conn.commit()
            return id_generado
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()