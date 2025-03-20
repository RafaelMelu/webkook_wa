
# WhatsApp Webhook FastAPI

Este proyecto implementa un servidor utilizando **FastAPI** para manejar webhooks de WhatsApp a través de la **WhatsApp Cloud API**. El servidor recibe mensajes entrantes, responde con un mensaje de eco y marca los mensajes como leídos.

## Funcionalidades

- **Recepción de mensajes**: El servidor recibe mensajes de texto desde WhatsApp.
- **Respuesta de eco**: Responde automáticamente con el mismo texto recibido.
- **Marcado como leído**: Los mensajes recibidos son marcados como leídos a través de la API de WhatsApp.

## Requisitos

- Python 3.7 o superior.
- Bibliotecas necesarias:
  - `fastapi`
  - `requests`
  - `uvicorn`
  - `python-dotenv`

## Instalación

### 1. Clona este repositorio

```bash
git clone https://github.com/tu-usuario/whatsapp-webhook.git
cd whatsapp-webhook
```

### 2. Crea un entorno virtual (opcional, pero recomendado)

```bash
python -m venv venv
source venv/bin/activate  # En Windows usa: venv\Scripts\activate
```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configura las variables de entorno

Crea un archivo `.env` en la raíz del proyecto y agrega las siguientes variables:

```env
WEBHOOK_VERIFY_TOKEN=tu_token_de_verificación
GRAPH_API_TOKEN=tu_token_de_api_de_facebook
PORT=8000  # (opcional, usa el puerto que prefieras)
```

- **WEBHOOK_VERIFY_TOKEN**: Token utilizado para verificar la suscripción del webhook con WhatsApp.
- **GRAPH_API_TOKEN**: Token de acceso a la API de Facebook para interactuar con WhatsApp.
- **PORT**: Puerto en el que el servidor escuchará (opcional, por defecto usa el puerto 8000).

### 5. Ejecuta el servidor

```bash
uvicorn main:app --reload
```

El servidor estará disponible en `http://localhost:8000`.

## Endpoints

### 1. **POST /webhook**

Este endpoint maneja los mensajes entrantes desde WhatsApp.

- **Entrada**: Un objeto JSON enviado por WhatsApp.
- **Salida**: Un JSON con el estado de la recepción.

Ejemplo de respuesta:

```json
{
  "status": "received"
}
```

### 2. **GET /webhook**

Este endpoint se utiliza para verificar el webhook con WhatsApp.

- **Parámetros**:
  - `hub_mode`: El modo de suscripción de WhatsApp (debe ser `subscribe`).
  - `hub_verify_token`: El token de verificación proporcionado en el archivo `.env`.
  - `hub_challenge`: El desafío proporcionado por WhatsApp para verificar el webhook.

Ejemplo de respuesta:

```json
{
  "status": "Verification successful"
}
```

### 3. **GET /**

Endpoint básico para comprobar si el servidor está corriendo.

Ejemplo de respuesta:

```json
{
  "message": "WebHook Running"
}
```

## Despliegue

### 1. Desplegar en Vercel

Para desplegar en Vercel, sigue los siguientes pasos:

1. Crea un archivo `vercel.json` en la raíz del proyecto:

    ```json
    {
      "version": 2,
      "builds": [
        {
          "src": "main.py",
          "use": "@vercel/python"
        }
      ]
    }
    ```

2. Conecta tu repositorio en [Vercel](https://vercel.com) y despliega tu aplicación.

## Contribución

Si deseas contribuir, por favor haz un **fork** de este repositorio y envía un **pull request** con tus cambios.

## Licencia

Este proyecto está bajo la licencia MIT. Para más detalles, consulta el archivo [LICENSE](LICENSE).

