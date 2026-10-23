from fastapi import APIRouter
from app.models.certificado import CertificadoBase
from app.repositories.certificado_repo import CertificadoRepository

router = APIRouter(prefix="/certificados", tags=["Certificados"])

@router.post("/")
def generar_certificado(data: CertificadoBase):
    return {"id_certificado": CertificadoRepository.crear(data)}