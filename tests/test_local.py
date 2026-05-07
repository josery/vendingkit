#!/usr/bin/env python3
"""
VendingKit Local Testing
Permite probar el agente de forma local sin necesidad de WhatsApp
"""

import sys
import os
from dotenv import load_dotenv

# Agrega la ruta del proyecto
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# IMPORTANTE: Carga .env ANTES de importar agent modules
env_path = os.path.join(project_root, ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)
    print(f"✓ .env cargado desde: {env_path}")
else:
    print(f"⚠️  .env no encontrado en: {env_path}")

from agent.brain import VendingKitBrain
from agent.memory import Memory
from agent.sheets import init_sheets_manager

# Carga variables de entorno
load_dotenv()

# Inicializa componentes
brain = VendingKitBrain()
memory = Memory()
sheets_manager = init_sheets_manager()


def print_section(title: str):
    """Imprime un título de sección"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_message(phone: str, message: str):
    """Prueba procesar un mensaje"""
    print(f"\n📱 Teléfono: {phone}")
    print(f"💬 Mensaje: {message}")

    # Procesa el mensaje
    intention, response, data = brain.process_message(message, phone_number=phone)

    print(f"🎯 Intención: {intention}")
    print(f"📝 Respuesta: {response}")
    print(f"📊 Datos extraídos:")
    for key, value in data.items():
        if value:
            print(f"   - {key}: {value}")

    # Guarda en memoria si no es conversación
    if intention != "CONVERSACION":
        incident_id = memory.save_incident(data)
        print(f"💾 Incidente guardado (ID: {incident_id})")

        # Intenta sincronizar con Sheets
        if sheets_manager and intention != "CONVERSACION":
            if sheets_manager.append_incident(data):
                print(f"☁️  Sincronizado con Google Sheets")


def test_suite():
    """Ejecuta una suite de pruebas"""

    print_section("🚀 VendingKit Local Testing Suite")

    # Pruebas
    test_cases = [
        (
            "34612345678",
            "Hola, soy Juan García de la empresa Tech Solutions, piso 3, extensión 305. La máquina del pasillo se acabó de bebidas.",
        ),
        (
            "34687654321",
            "Urgente: Se perdió dinero en la máquina de la zona común. Me cobraron dos veces. Celular: 34687654322",
        ),
        (
            "34612111111",
            "¿Cuándo es la próxima reposición? Ubicación: Av Principal 45, Madrid",
        ),
        (
            "34645555555",
            "La máquina no funciona, la pantalla está apagada y no dispensa productos",
        ),
        (
            "34623333333",
            "Hola, ¿cuál es el precio de las bebidas?",
        ),
    ]

    for i, (phone, message) in enumerate(test_cases, 1):
        print_section(f"Prueba {i}/{len(test_cases)}")
        test_message(phone, message)

    # Resumen
    print_section("📊 Resumen")

    incidents = memory.get_unsync_incidents()
    print(f"Total de incidentes: {len(incidents)}")
    print(f"Google Sheets: {'Conectado' if sheets_manager else 'No configurado'}")

    if incidents:
        print("\nÚltimos incidentes:")
        for inc in incidents[-3:]:
            print(f"  - {inc['category']}: {inc['name']} ({inc['phone_number']})")

    print_section("✅ Testing completado")


if __name__ == "__main__":
    try:
        test_suite()
    except KeyboardInterrupt:
        print("\n\n⚠️  Testing interrumpido por usuario")
    except Exception as e:
        print(f"\n❌ Error durante testing: {e}")
        import traceback

        traceback.print_exc()
