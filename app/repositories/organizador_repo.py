from app.core.database import get_db_connection
from app.models.organizador import OrganizadorBase

class OrganizadorRepository:
    @staticmethod
    def crear(data: OrganizadorBase):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Organizadores (id_usuario) VALUES (%s) RETURNING id_organizador;", (data.id_usuario,))
            id_generado = cursor.fetchone()[0]
            conn.commit()
            return id_generado
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()