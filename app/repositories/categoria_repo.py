from app.core.database import get_db_connection
from app.models.categoria import CategoriaBase

class CategoriaRepository:
    @staticmethod
    def crear(data: CategoriaBase):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Categorias (nombre) VALUES (%s) RETURNING id_categoria;", (data.nombre,))
            id_generado = cursor.fetchone()[0]
            conn.commit()
            return id_generado
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()