from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from backend.services import consultar_dify_stream


router = APIRouter()


class Consulta(BaseModel):
    pregunta: str


@router.post("/chat")
async def chat(consulta: Consulta):

    return StreamingResponse(
        consultar_dify_stream(
            consulta.pregunta
        ),
        media_type="text/plain; charset=utf-8",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )