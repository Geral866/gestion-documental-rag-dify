from fastapi import APIRouter
from pydantic import BaseModel
from backend.services import consultar_dify

router = APIRouter()

class Consulta(BaseModel):
    pregunta: str

@router.post("/chat")
async def chat(consulta: Consulta):
    return consultar_dify(consulta.pregunta)