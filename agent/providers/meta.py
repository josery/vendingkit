"""
VendingKit Meta WhatsApp Provider
Gestiona la integración con Meta WhatsApp Cloud API
"""

import os
import json
from typing import Dict, Any, Optional
import requests
from datetime import datetime

# Credenciales de Meta
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
META_PHONE_NUMBER_ID = os.getenv("META_PHONE_NUMBER_ID")
META_VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN")
META_BUSINESS_ACCOUNT_ID = os.getenv("META_BUSINESS_ACCOUNT_ID")

# Endpoints de Meta
META_API_URL = "https://graph.instagram.com/v19.0"
WHATSAPP_URL = f"{META_API_URL}/{META_PHONE_NUMBER_ID}/messages"


class MetaProvider:
    """Proveedor de Meta para WhatsApp"""

    def __init__(self):
        self.access_token = META_ACCESS_TOKEN
        self.phone_number_id = META_PHONE_NUMBER_ID
        self.verify_token = META_VERIFY_TOKEN
        self.api_url = WHATSAPP_URL

    def verify_webhook(self, token: str) -> bool:
        """Verifica que el token de webhook sea válido"""
        return token == self.verify_token

    def send_message(self, phone_number: str, message: str) -> Dict[str, Any]:
        """Envía un mensaje de texto a WhatsApp"""
        try:
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": phone_number,
                "type": "text",
                "text": {"preview_url": False, "body": message},
            }

            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }

            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=10,
            )

            if response.status_code == 200:
                print(f"✓ Mensaje enviado a {phone_number}")
                return {"success": True, "message_id": response.json().get("messages")[0].get("id")}
            else:
                print(f"✗ Error enviando mensaje: {response.text}")
                return {"success": False, "error": response.text}

        except Exception as e:
            print(f"✗ Excepción al enviar mensaje: {e}")
            return {"success": False, "error": str(e)}

    def send_template_message(self, phone_number: str, template_name: str, params: list = None) -> Dict[str, Any]:
        """Envía un mensaje de template"""
        try:
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": phone_number,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {"code": "es"},
                },
            }

            if params:
                payload["template"]["parameters"] = {"body": {"parameters": params}}

            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }

            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=10,
            )

            if response.status_code == 200:
                print(f"✓ Template enviado a {phone_number}")
                return {"success": True, "message_id": response.json().get("messages")[0].get("id")}
            else:
                print(f"✗ Error enviando template: {response.text}")
                return {"success": False, "error": response.text}

        except Exception as e:
            print(f"✗ Excepción al enviar template: {e}")
            return {"success": False, "error": str(e)}

    def parse_webhook_payload(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parsea el payload del webhook de Meta"""
        try:
            # Meta envía los mensajes en entry[0].changes[0].value.messages
            if "entry" not in payload:
                return None

            entry = payload["entry"][0]
            if "changes" not in entry:
                return None

            changes = entry["changes"][0]
            value = changes.get("value", {})

            # Verifica que haya mensajes
            if "messages" not in value:
                return None

            message = value["messages"][0]
            sender = message.get("from")
            message_id = message.get("id")
            timestamp = message.get("timestamp")

            # Extrae el contenido del mensaje
            if message.get("type") == "text":
                text = message["text"]["body"]
            elif message.get("type") == "button":
                text = message["button"]["text"]
            else:
                return None

            return {
                "sender": sender,
                "message": text,
                "message_id": message_id,
                "timestamp": timestamp,
                "type": message.get("type"),
                "raw_payload": value,
            }

        except Exception as e:
            print(f"Error parseando webhook: {e}")
            return None

    def mark_message_read(self, message_id: str) -> bool:
        """Marca un mensaje como leído"""
        try:
            payload = {
                "messaging_product": "whatsapp",
                "status": "read",
                "message_id": message_id,
            }

            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }

            # Usa el endpoint de messages con el message_id
            url = f"{META_API_URL}/{message_id}"

            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=10,
            )

            return response.status_code == 200

        except Exception as e:
            print(f"Error marcando mensaje como leído: {e}")
            return False

    def get_message_media(self, media_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene información de un media"""
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
            }

            url = f"{META_API_URL}/{media_id}"

            response = requests.get(
                url,
                headers=headers,
                timeout=10,
            )

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error obteniendo media: {response.text}")
                return None

        except Exception as e:
            print(f"Error en get_message_media: {e}")
            return None
