# VendingKit — WhatsApp AI Agent para Máquinas de Vending

Un framework inteligente para construir agentes de WhatsApp especializados en máquinas de vending, con IA y tracking automático — **sin programar**.

## ¿Qué es VendingKit?

✅ Detecta automáticamente: reposición, mantenimiento, reclamaciones
✅ Responde inteligentemente según el tipo de incidente
✅ Registra TODO en Google Sheets (automático)
✅ Agenda visitas en Google Calendar
✅ Captura: nombre, ubicación, empresa, piso, extensión, celular, monto

## Categorías de Incidentes

```
REPOSICION             → "Se acabó", "llenar", "refill"
MANTENIMIENTO          → "No funciona", "dañado"
FALLO_DISPENSACION     → "Atrapado", "no sale"
RECLAMACION            → "Perdí dinero", "quiero devolución"
RUTAS_ENTREGAS         → "¿Cuándo llegan?"
FINANCIAMIENTO         → "¿Cuánto cuesta?"
CONSULTA_VENTAS        → "¿Qué vende más?"
CONSULTA               → "Precios", "reunión"
CONVERSACION           → Saludos, charla
```

## Campos en Google Sheets (AUTOMÁTICO)

Fecha/Hora | Teléfono | Nombre | Ubicación | Empresa | Piso | Extensión | Celular | Categoría | Descripción | Respuesta | Monto

## Stack

Python 3.11 + FastAPI + Claude API + SQLite + Google Sheets + Meta/Twilio + Docker + Railway

## Inicio Rápido

```bash
# 1. Clona o descarga
git clone https://github.com/tu-usuario/vendingkit.git
cd vendingkit

# 2. Lee la guía completa
cat CLAUDE.md

# 3. Instala y empieza
python3 start.sh
```

## Estructura

```
vendingkit/
├── CLAUDE.md           ← Guía completa (LEE PRIMERO)
├── agent/              ← FastAPI + IA + Sheets
├── config/             ← business.yaml + prompts.yaml
├── tests/              ← test_local.py (sin WhatsApp)
└── requirements.txt    ← Dependencias
```

## Comandos

```bash
python tests/test_local.py    # Test sin WhatsApp
uvicorn agent.main:app --reload  # Arrancar servidor
docker compose up --build     # Docker
```

## ¿Necesitas Ayuda?

Lee **CLAUDE.md** — contiene todo lo que necesitas saber.

---

**VendingKit está listo. ¡Empecemos!** 🚀
