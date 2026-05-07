"""
VendingKit Main FastAPI Application
Servidor principal con webhook para Meta WhatsApp Cloud API
"""

import os
import sys
import logging
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Carga variables de entorno
load_dotenv()

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importa módulos de VendingKit
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.brain import VendingKitBrain
from agent.memory import Memory
from agent.sheets import init_sheets_manager
from agent.providers.meta import MetaProvider

# Inicializa componentes
app = FastAPI(title="VendingKit", version="1.0.0")
brain = VendingKitBrain()
memory = Memory()
meta = MetaProvider()
sheets_manager = init_sheets_manager()

# Variables globales
WEBHOOK_VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN", "Vending-key-123")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "app": "VendingKit"}


@app.get("/webhook")
async def verify_webhook(request: Request):
    """Webhook verification endpoint para Meta"""
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    logger.info(f"Webhook verification request: mode={mode}, token={token[:10]}...")

    if mode == "subscribe" and meta.verify_webhook(token):
        logger.info("✓ Webhook verified successfully")
        return Response(content=challenge, media_type="text/plain")
    else:
        logger.warning("✗ Webhook verification failed")
        return JSONResponse({"error": "Invalid verification"}, status_code=403)


@app.post("/webhook")
async def handle_webhook(request: Request):
    """Procesa mensajes entrantes de WhatsApp"""
    try:
        payload = await request.json()
        logger.info(f"Webhook payload recibido: {payload}")

        # Valida que sea de WhatsApp
        if payload.get("object") != "whatsapp_business_account":
            return JSONResponse({"status": "ok"})

        # Parsea el mensaje
        message_data = meta.parse_webhook_payload(payload)
        if not message_data:
            return JSONResponse({"status": "ok"})

        sender = message_data["sender"]
        message_text = message_data["message"]
        message_id = message_data["message_id"]

        logger.info(f"Mensaje de {sender}: {message_text}")

        # Guarda en memoria
        memory.save_conversation(sender, message_text, "user")

        # Obtiene historial de conversación
        history = memory.get_conversation_history(sender)

        # Procesa con el brain
        intention, response, extracted_data = brain.process_message(
            message_text, phone_number=sender, history=history
        )

        logger.info(f"Intención detectada: {intention}")
        logger.info(f"Respuesta generada: {response}")

        # Guarda la respuesta en memoria
        memory.save_conversation(sender, response, "assistant")

        # Guarda el incidente en BD local
        if intention != "CONVERSACION":
            extracted_data["phone_number"] = sender
            incident_id = memory.save_incident(extracted_data)
            logger.info(f"Incidente guardado (ID: {incident_id})")

            # Intenta sincronizar con Google Sheets
            if sheets_manager:
                if sheets_manager.append_incident(extracted_data):
                    memory.mark_incident_synced(incident_id)
                    logger.info(f"Incidente sincronizado con Sheets")

        # Marca mensaje como leído
        meta.mark_message_read(message_id)

        # Envía respuesta
        result = meta.send_message(sender, response)

        if result["success"]:
            logger.info(f"Respuesta enviada a {sender}")
            return JSONResponse({"status": "ok", "message_id": result.get("message_id")})
        else:
            logger.error(f"Error enviando respuesta: {result.get('error')}")
            return JSONResponse({"status": "error", "error": result.get("error")}, status_code=500)

    except Exception as e:
        logger.error(f"Error en handler del webhook: {e}", exc_info=True)
        return JSONResponse({"status": "error", "error": str(e)}, status_code=500)


@app.post("/test/message")
async def test_send_message(phone_number: str, message: str):
    """Endpoint de prueba para enviar mensajes"""
    result = meta.send_message(phone_number, message)
    return result


@app.get("/incidents")
async def get_incidents():
    """Obtiene todos los incidentes no sincronizados"""
    incidents = memory.get_unsync_incidents()
    return {"count": len(incidents), "incidents": incidents}


@app.post("/sync/sheets")
async def sync_to_sheets():
    """Sincroniza incidentes pendientes con Google Sheets"""
    if not sheets_manager:
        return {"error": "Google Sheets no configurado"}

    incidents = memory.get_unsync_incidents()
    synced = sheets_manager.append_multiple_incidents(incidents)

    for incident in incidents:
        memory.mark_incident_synced(incident["id"])

    return {"synced": synced, "total": len(incidents)}


@app.get("/config/status")
async def config_status():
    """Retorna el estado de configuración"""
    return {
        "meta": {
            "configured": bool(os.getenv("META_ACCESS_TOKEN")),
            "phone_number_id": os.getenv("META_PHONE_NUMBER_ID", "N/A"),
        },
        "anthropic": {
            "configured": bool(os.getenv("ANTHROPIC_API_KEY")),
        },
        "google_sheets": {
            "configured": bool(sheets_manager),
            "sheets_id": os.getenv("GOOGLE_SHEETS_ID", "N/A"),
        },
        "database": {
            "path": "vendingkit.db",
        },
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    logger.info(f"🚀 VendingKit iniciando en {host}:{port}")
    uvicorn.run(app, host=host, port=port)
