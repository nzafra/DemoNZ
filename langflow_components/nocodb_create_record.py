import requests

from langflow.custom import Component
from langflow.io import MessageTextInput, Output, SecretStrInput, StrInput
from langflow.schema import Data


class NocoDBCreateRecordComponent(Component):
    """Crea un registro en una tabla de NocoDB.

    Pensado para ser usado como herramienta (Tool) por un Agente de Langflow:
    el agente provee `Nombre` y `Apellido` y el componente hace el POST a la
    API de NocoDB (v2) para crear el registro.
    """

    display_name = "NocoDB - Crear Registro"
    description = "Crea un registro en una tabla de NocoDB enviando Nombre y Apellido."
    documentation = "https://docs.nocodb.com/developer-resources/rest-APIs/overview"
    icon = "database"
    name = "NocoDBCreateRecord"

    inputs = [
        StrInput(
            name="base_url",
            display_name="Base URL",
            info="URL base de la instancia de NocoDB.",
            value="https://app.nocodb.com",
            advanced=True,
        ),
        StrInput(
            name="table_id",
            display_name="Table ID",
            info="ID de la tabla de NocoDB donde se crea el registro.",
            value="mftyeo3ltghe9el",
        ),
        SecretStrInput(
            name="xc_token",
            display_name="xc-token",
            info="API token de NocoDB (header xc-token).",
            required=True,
        ),
        MessageTextInput(
            name="nombre",
            display_name="Nombre",
            info="Valor para el campo 'Nombre' del registro.",
            tool_mode=True,
            required=True,
        ),
        MessageTextInput(
            name="apellido",
            display_name="Apellido",
            info="Valor para el campo 'Apellido' del registro.",
            tool_mode=True,
            required=True,
        ),
    ]

    outputs = [
        Output(display_name="Resultado", name="record", method="create_record"),
    ]

    def create_record(self) -> Data:
        url = f"{self.base_url.rstrip('/')}/api/v2/tables/{self.table_id}/records"

        headers = {
            "xc-token": self.xc_token,
            "Content-Type": "application/json",
        }

        payload = {
            "Nombre": self.nombre,
            "Apellido": self.apellido,
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
        except requests.exceptions.HTTPError as exc:
            error_body = exc.response.text if exc.response is not None else str(exc)
            status = exc.response.status_code if exc.response is not None else "N/A"
            self.status = f"Error {status} al crear el registro: {error_body}"
            return Data(data={"error": error_body, "status_code": status})
        except requests.exceptions.RequestException as exc:
            self.status = f"Error de conexión con NocoDB: {exc}"
            return Data(data={"error": str(exc)})

        data = Data(data=result)
        self.status = data
        return data
