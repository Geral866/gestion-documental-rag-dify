import requests
from backend.config import DIFY_API_URL, DIFY_API_KEY # Asegúrate de que DIFY_API_KEY también se importa

def consultar_dify(pregunta: str):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DIFY_API_KEY}" # Usa la DIFY_API_KEY importada
    }

    payload = {
        "inputs": {},
        "query": pregunta,
        "response_mode": "blocking", # Puedes cambiar a "streaming" si lo necesitas
        "user": "unique_user_id" # Asegúrate de que este ID de usuario sea único por sesión o usuario
    }

    print("URL usada para la conexión con Dify:", DIFY_API_URL)
    print("API KEY usada para la conexión con Dify (primeros 10 caracteres):", DIFY_API_KEY[:10] + "...")
    

    try:
        respuesta = requests.post(
            DIFY_API_URL, # <<<<<<<<<<<<<<<<<<<< CORREGIDO: Ahora usa la variable DIFY_API_URL
            headers=headers,
            json=payload
        )

        print("Status de la respuesta de Dify:", respuesta.status_code)
        print("Cuerpo de la respuesta de Dify:")
        print(respuesta.text)

        respuesta.raise_for_status() # Esto lanzará una excepción para códigos de estado de error (4xx o 5xx)

        return {
            "status": respuesta.status_code,
            "body": respuesta.text
        }

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con Dify: {e}")
        return {
            "status": 500,
            "body": f"Error al conectar con Dify: {e}"
        }