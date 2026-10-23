from app.core.database import get_db_connection
from app.models.modelo import ModeloBase

class ModeloRepository:
    @staticmethod
    def crear(data: ModeloBase):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Modelos (nombre, descripcion) VALUES (%s, %s) RETURNING id_modelo;", (data.nombre, data.descripcion))
            id_generado = cursor.fetchone()[0]
            conn.commit()
            return id_generado
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()