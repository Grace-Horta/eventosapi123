from app.core.database import get_db_connection
from app.models.certificado import CertificadoBase

class CertificadoRepository:
    @staticmethod
    def crear(data: CertificadoBase):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Certificados (codigo_validacion, id_asistencia) VALUES (%s, %s) RETURNING id_certificado;", (data.codigo_validacion, data.id_asistencia))
            id_generado = cursor.fetchone()[0]
            conn.commit()
            return id_generado
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()