from app.core.database import get_db_connection
from app.models.modelo_x_rol import ModeloXRolBase

class ModeloXRolRepository:
    @staticmethod
    def crear(data: ModeloXRolBase):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO Modelos_Por_Rol (id_rol, id_modelo, puede_crear, puede_leer, puede_actualizar, puede_eliminar)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_modelo_por_rol;
            """
            cursor.execute(query, (data.id_rol, data.id_modelo, data.puede_crear, data.puede_leer, data.puede_actualizar, data.puede_eliminar))
            id_generado = cursor.fetchone()[0]
            conn.commit()
            return id_generado
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()