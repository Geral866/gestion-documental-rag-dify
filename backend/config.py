import os
from dotenv import load_dotenv

# Carga las variables desde el archivo .env en la raíz
load_dotenv()

# Define las variables explícitamente
DIFY_API_URL = os.getenv("DIFY_API_URL")
DIFY_API_KEY = os.getenv("DIFY_API_KEY")

# Validación rápida (esto ayuda a encontrar el error si faltan valores)
if not DIFY_API_KEY:
    print("ADVERTENCIA: No se encontró DIFY_API_KEY en el archivo .env")
    
    print("CONFIG DIFY_API_URL =", DIFY_API_URL)
print("CONFIG DIFY_API_KEY =", DIFY_API_KEY[:10] + "...")
