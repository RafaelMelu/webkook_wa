import os
import requests
from fastapi import FastAPI, Query, Request
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

WEBHOOK_VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN")
GRAPH_API_TOKEN = os.getenv("GRAPH_API_TOKEN")
PORT = int(os.getenv("PORT", 8000))

app = FastAPI()

@app.post("/webhook")
async def webhook(req: Request):
    """Maneja mensajes entrantes de WhatsApp."""
    data = await req.json()
    print("📩 Incoming POST request to /webhook")
    print("🔹 Received Data:", data)

    message = data.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {}).get("messages", [{}])[0]

    if message and message.get("type") == "text":
        phone_number_id = data["entry"][0]["changes"][0]["value"]["metadata"]["phone_number_id"]
        sender = message["from"]
        text_body = message["text"]["body"]
        message_id = message["id"]

        print(f"✅ Message received from {sender}: {text_body}")

        # Responder con un mensaje de eco
        send_whatsapp_message(phone_number_id, sender, f"Echo: {text_body}", message_id)

        # Marcar el mensaje como leído
        mark_message_as_read(phone_number_id, message_id)

        print(f"📤 Sent echo message to {sender}")

    return {"status": "received"}

@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: int = Query(None, alias="hub.challenge")
):
    """Verifica el webhook de WhatsApp."""
    print("📩 Incoming GET request to /webhook")
    print(f"🔹 hub.mode: {hub_mode}, hub.verify_token: {hub_verify_token}, hub.challenge: {hub_challenge}")

    if hub_mode == "subscribe" and hub_verify_token == WEBHOOK_VERIFY_TOKEN:
        print("✅ Webhook verified successfully!")
        return int(hub_challenge)  # Aseguramos que se devuelve como número

    print("❌ Webhook verification failed")
    return {"error": "Verification failed"}, 403

@app.get("/")
async def home():
    print("📩 Incoming GET request to /")
    return {"message": "WeebHook Running"}

def send_whatsapp_message(phone_number_id, to, text, message_id):
    """Envía un mensaje de texto a través de WhatsApp Cloud API."""
    url = f"https://graph.facebook.com/v22.0/639991559190781/messages"
    print("PRUEBA URL", url)
    print("PRUEBA TOKEN", GRAPH_API_TOKEN)
    headers = {"Authorization": f"Bearer {GRAPH_API_TOKEN}"}
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    print(f"📤 Sending message to {to}: {text}")
    response = requests.post(url, headers=headers, json=payload)
    print(f"🔹 Response: {response.status_code}, {response.text}")

def mark_message_as_read(phone_number_id, message_id):
    """Marca un mensaje como leído."""
    url = f"https://graph.facebook.com/v22.0/639991559190781/messages"
    headers = {"Authorization": f"Bearer {GRAPH_API_TOKEN}"}
    payload = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id,
    }
    print(f"📌 Marking message {message_id} as read")
    response = requests.post(url, headers=headers, json=payload)
    print(f"🔹 Response: {response.status_code}, {response.text}")

if __name__ == "__main__":
    import uvicorn
    print(f"🚀 Starting server on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
