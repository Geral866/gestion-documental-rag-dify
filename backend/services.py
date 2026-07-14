import json
import requests

from backend.config import DIFY_API_URL, DIFY_API_KEY


def consultar_dify_stream(pregunta: str):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DIFY_API_KEY}",
    }

    payload = {
        "inputs": {},
        "query": pregunta,
        "response_mode": "streaming",
        "user": "proyecto_delfin_usuario",
    }

    try:
        with requests.post(
            DIFY_API_URL,
            headers=headers,
            json=payload,
            stream=True,
            timeout=(30, 600),
        ) as respuesta:

            print("Status Dify:", respuesta.status_code)

            respuesta.raise_for_status()

            for linea in respuesta.iter_lines(
                decode_unicode=True
            ):
                if not linea:
                    continue

                if not linea.startswith("data:"):
                    continue

                contenido = linea[5:].strip()

                try:
                    data = json.loads(contenido)

                except json.JSONDecodeError:
                    continue

                evento = data.get("event")

                if evento in (
                    "message",
                    "agent_message",
                ):
                    texto = data.get("answer", "")

                    if texto:
                        yield texto

                elif evento == "error":
                    mensaje = data.get(
                        "message",
                        "Error desconocido en Dify."
                    )

                    yield f"\n[ERROR DIFY] {mensaje}"

                elif evento == "message_end":
                    break

    except requests.exceptions.Timeout:
        yield (
            "\nEl modelo local tardó demasiado "
            "en responder."
        )

    except requests.exceptions.RequestException as error:
        print("Error de conexión con Dify:", error)

        yield (
            "\nError al conectar con Dify: "
            f"{str(error)}"
        )