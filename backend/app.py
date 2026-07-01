from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import router

app = FastAPI(title="Backend RAG - Proyecto Delfín")

# Configurar CORS para permitir que tu frontend (HTML/JS) se conecte
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas
app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Backend RAG funcionando correctamente"}

