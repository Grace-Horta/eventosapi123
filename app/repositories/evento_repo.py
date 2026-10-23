from app.core.database import get_db_connection
from app.models.evento import EventoBase

class EventoRepository:
    @staticmethod
    def crear(data: EventoBase):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO Eventos (titulo, descripcion, fecha, id_categoria, id_ubicacion, id_organizador)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_evento;
            """
            cursor.execute(query, (data.titulo, data.descripcion, data.fecha, data.id_categoria, data.id_ubicacion, data.id_organizador))
            id_generado = cursor.fetchone()[0]
            conn.commit()
            return id_generado
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()