# Componente Langflow: NocoDB - Crear Registro

Componente custom de Langflow que crea un registro en una tabla de NocoDB
enviando los campos **Nombre** y **Apellido**. Está preparado para usarse
como **herramienta (Tool)** de un Agente: el agente completa `Nombre` y
`Apellido` y el componente hace el `POST` a la API v2 de NocoDB.

## Instalación

1. En Langflow, arrastrá un **Custom Component** al canvas (o usá el menú
   `+` → *New Custom Component*).
2. Pegá el contenido de [`nocodb_create_record.py`](./nocodb_create_record.py).
3. Guardá. Aparecerá el componente **NocoDB - Crear Registro**.

## Configuración

| Campo       | Descripción                                              | Default                    |
|-------------|----------------------------------------------------------|----------------------------|
| Base URL    | URL de la instancia de NocoDB (avanzado)                 | `https://app.nocodb.com`   |
| Table ID    | ID de la tabla destino                                   | `mftyeo3ltghe9el`          |
| xc-token    | API token de NocoDB (header `xc-token`) — **requerido**  | —                          |
| Nombre      | Valor del campo `Nombre` (tool mode)                     | —                          |
| Apellido    | Valor del campo `Apellido` (tool mode)                   | —                          |

> **Seguridad:** el token NO está hardcodeado en el componente. Cargalo en el
> campo `xc-token` (tipo secreto). Si el token del ejemplo de Postman fue
> compartido públicamente, conviene **rotarlo** en NocoDB.

## Uso con un Agente

1. Conectá el componente al **Agent** usando la salida como *Tool* (activá
   `Tool Mode` en el componente).
2. El agente decidirá cuándo llamarlo y pasará `Nombre` y `Apellido` según la
   conversación.

## Equivalente al request de Postman

```
POST https://app.nocodb.com/api/v2/tables/mftyeo3ltghe9el/records
Headers:
  xc-token: <TU_TOKEN>
  Content-Type: application/json
Body:
  { "Nombre": "...", "Apellido": "..." }
```

## Salida

Devuelve un objeto `Data` con la respuesta JSON de NocoDB (incluye el `Id` del
registro creado). Ante error HTTP o de conexión, devuelve un `Data` con la
clave `error` y el `status_code`, y muestra el detalle en el estado del
componente.
