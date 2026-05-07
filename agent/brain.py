"""
VendingKit Brain Module
Contiene los dos agentes de IA:
1. Intent Detector - Clasifica el tipo de solicitud
2. Response Generator - Genera respuesta personalizada
"""

import os
import re
import yaml
from typing import Tuple, Dict, Any, List
from dotenv import load_dotenv
from anthropic import Anthropic

# Carga variables de entorno desde .env
# Busca en múltiples ubicaciones
env_files = [
    ".env",
    os.path.join(os.path.dirname(__file__), "..", ".env"),
    os.path.expanduser("~/.vendingkit/.env"),
]

for env_file in env_files:
    if os.path.exists(env_file):
        try:
            load_dotenv(env_file, override=True)
        except:
            pass
        break

# Inicializa cliente de Anthropic
# Obtiene API key de variable de entorno (que debe estar cargada antes)
api_key = os.getenv("ANTHROPIC_API_KEY")
if api_key:
    client = Anthropic(api_key=api_key)
else:
    # Si no hay API key, crea cliente que fallará con mensaje claro
    try:
        client = Anthropic()  # Intenta usar ANTHROPIC_API_KEY del entorno
    except:
        client = None


class IntentDetector:
    """Detecta la intención del cliente (clasificación)"""

    def __init__(self, prompts_config: Dict[str, Any]):
        self.prompt_template = prompts_config.get("prompts", {}).get("intent_detection", "")
        self.categories = prompts_config.get("prompts", {}).get("intent_categories", [])

    def detect(self, message: str) -> str:
        """Detecta la intención del mensaje"""
        try:
            prompt = self.prompt_template.format(message=message)

            response = client.messages.create(
                model="claude-opus-4-1-20250805",
                max_tokens=50,
                messages=[{"role": "user", "content": prompt}],
            )

            # Extrae la respuesta y limpia
            intent = response.content[0].text.strip().upper()

            # Valida que sea una categoría válida
            if intent in self.categories:
                return intent
            else:
                # Si no es válida, retorna la más cercana o CONSULTA
                return "CONSULTA"

        except Exception as e:
            print(f"Error en detección de intención: {e}")
            return "CONSULTA"


class ResponseGenerator:
    """Genera respuestas personalizadas basadas en la intención"""

    def __init__(self, prompts_config: Dict[str, Any], business_config: Dict[str, Any]):
        self.prompt_template = prompts_config.get("prompts", {}).get("response_generation", "")
        self.agent_name = business_config.get("agent", {}).get("name", "VendingKit Agent")
        self.business_name = business_config.get("business", {}).get("name", "VendingKit")

    def generate(
        self,
        message: str,
        intention: str,
        location: str = "No especificada",
        history: List[Dict[str, str]] = None,
    ) -> str:
        """Genera una respuesta personalizada"""
        try:
            prompt = self.prompt_template.format(
                agent_name=self.agent_name,
                business_name=self.business_name,
                intention=intention,
                message=message,
                location=location,
            )

            # Construye historial para contexto
            messages = []
            if history:
                messages.extend(history)

            messages.append({"role": "user", "content": prompt})

            response = client.messages.create(
                model="claude-opus-4-1-20250805",
                max_tokens=300,
                messages=messages,
            )

            return response.content[0].text.strip()

        except Exception as e:
            print(f"Error en generación de respuesta: {e}")
            return "Disculpa, estoy procesando tu solicitud. Por favor intenta de nuevo."


class VendingKitBrain:
    """Brain central que coordina ambos agentes"""

    def __init__(self, prompts_config_path: str = "config/prompts.yaml", business_config_path: str = "config/business.yaml"):
        # Carga configuraciones
        self.prompts_config = self._load_yaml(prompts_config_path)
        self.business_config = self._load_yaml(business_config_path)

        # Inicializa agentes
        self.intent_detector = IntentDetector(self.prompts_config)
        self.response_generator = ResponseGenerator(self.prompts_config, self.business_config)

    def _load_yaml(self, path: str) -> Dict[str, Any]:
        """Carga archivo YAML"""
        try:
            # Intenta ruta relativa al directorio actual
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f)

            # Intenta ruta absoluta
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                with open(abs_path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f)

            # Si no encuentra, retorna diccionario vacío
            print(f"⚠️  No se encontró {path}")
            return {}
        except Exception as e:
            print(f"Error cargando {path}: {e}")
            return {}

    def process_message(
        self, message: str, phone_number: str = "", location: str = "", history: List[Dict[str, str]] = None
    ) -> Tuple[str, str, Dict[str, Any]]:
        """
        Procesa un mensaje y retorna:
        1. Intención detectada
        2. Respuesta generada
        3. Datos extraídos
        """

        # Paso 1: Detecta intención
        intention = self.intent_detector.detect(message)

        # Paso 2: Genera respuesta
        response = self.response_generator.generate(message, intention, location, history)

        # Paso 3: Extrae datos del mensaje y respuesta
        extracted_data = self._extract_data(message, response, intention, phone_number)

        return intention, response, extracted_data

    def _extract_data(self, message: str, response: str, intention: str, phone_number: str) -> Dict[str, Any]:
        """Extrae datos relevantes del mensaje"""

        data = {
            "phone_number": phone_number,
            "category": intention,
            "description": message,
            "response": response,
            "name": self._extract_name(message, response),
            "location": self._extract_location(message, response),
            "company": self._extract_company(message, response),
            "floor": self._extract_floor(message, response),
            "extension": self._extract_extension(message, response),
            "celular": self._extract_celular(message, response),
            "monto": self._extract_monto(message, response),
        }

        return data

    def _extract_name(self, message: str, response: str) -> str:
        """Intenta extraer el nombre del cliente"""
        # Busca patrones como "Mi nombre es", "Soy", etc.
        patterns = [
            r"(?:mi\s+nombre\s+es|soy|llamo)\s+([A-Za-záéíóúñ\s]+)",
            r"(?:name\s+is|I'm)\s+([A-Za-z\s]+)",
        ]

        combined = message.lower() + " " + response.lower()

        for pattern in patterns:
            match = re.search(pattern, combined, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return ""

    def _extract_location(self, message: str, response: str) -> str:
        """Intenta extraer la ubicación"""
        patterns = [r"(?:ubicación|location|dirección|address)[:\s]+([^,\n]+)"]
        combined = message.lower() + " " + response.lower()

        for pattern in patterns:
            match = re.search(pattern, combined, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return ""

    def _extract_company(self, message: str, response: str) -> str:
        """Intenta extraer la empresa"""
        patterns = [r"(?:empresa|company|negocio)[:\s]+([^,\n]+)"]
        combined = message.lower() + " " + response.lower()

        for pattern in patterns:
            match = re.search(pattern, combined, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return ""

    def _extract_floor(self, message: str, response: str) -> str:
        """Intenta extraer el piso"""
        patterns = [r"(?:piso|floor|nivel)[:\s]*(\d+)"]
        combined = message.lower() + " " + response.lower()

        for pattern in patterns:
            match = re.search(pattern, combined, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return ""

    def _extract_extension(self, message: str, response: str) -> str:
        """Intenta extraer la extensión"""
        patterns = [r"(?:extensión|extension|ext)[:\s]*(\d+)"]
        combined = message.lower() + " " + response.lower()

        for pattern in patterns:
            match = re.search(pattern, combined, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return ""

    def _extract_celular(self, message: str, response: str) -> str:
        """Intenta extraer el celular"""
        patterns = [r"(?:celular|mobile|teléfono)[:\s]*(\d{7,})"]
        combined = message.lower() + " " + response.lower()

        for pattern in patterns:
            match = re.search(pattern, combined, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return ""

    def _extract_monto(self, message: str, response: str) -> str:
        """Intenta extraer el monto"""
        patterns = [r"\$\s*(\d+(?:\.\d{2})?)", r"(?:monto|amount)[:\s]*\$*(\d+(?:\.\d{2})?)"]
        combined = message.lower() + " " + response.lower()

        for pattern in patterns:
            match = re.search(pattern, combined, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return ""
