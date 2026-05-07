# VendingKit — Guía de Inicio Rápido

## ✅ Credenciales Configuradas

Tu VendingKit ya tiene todas las credenciales necesarias. Verifica el archivo `.env`:

```
✓ ANTHROPIC_API_KEY
✓ META_ACCESS_TOKEN
✓ META_PHONE_NUMBER_ID: 905292252675991
✓ META_VERIFY_TOKEN: Vending-key-123
✓ GOOGLE_SHEETS_ID: 15R_caZHMICAbMHTeqirMHrtaX5BhkH8WdrHGrW3dvUY
✓ GOOGLE_CALENDAR_EMAIL: josery@gmail.com
```

---

## 🚀 Opción 1: Ejecución Local (Recomendado para Desarrollo)

### Paso 1: Instalar dependencias

```bash
cd /Users/jvasquez/Documents/Proyectos\ Claude/VendingKit
pip install -r requirements.txt
```

### Paso 2: Prueba local del agente

```bash
python tests/test_local.py
```

Esto ejecutará una suite de pruebas con diferentes tipos de mensajes y mostrará:
- Intención detectada
- Respuesta generada
- Datos extraídos
- Sincronización con Google Sheets

### Paso 3: Iniciar servidor FastAPI

```bash
python -m uvicorn agent.main:app --reload --port 8000
```

El servidor estará disponible en: `http://localhost:8000`

**Endpoints disponibles:**
- `GET /health` — Verifica el estado del servidor
- `GET /webhook` — Verificación de webhook (usado por Meta)
- `POST /webhook` — Recibe mensajes de WhatsApp
- `GET /config/status` — Estado de configuración
- `GET /incidents` — Lista incidentes guardados
- `POST /sync/sheets` — Sincroniza con Google Sheets

---

## 🐳 Opción 2: Ejecución con Docker (Recomendado para Producción)

### Paso 1: Construir imagen

```bash
docker build -t vendingkit:latest .
```

### Paso 2: Ejecutar contenedor

```bash
docker run -p 8000:8000 \
  --env-file .env \
  vendingkit:latest
```

O con Docker Compose (más fácil):

```bash
docker-compose up -d
```

---

## 🔗 Configurar Webhook en Meta

### Paso 1: Abre Facebook Developer Console

Ve a: https://developers.facebook.com/apps/849375467811408/whatsapp-business/wa-dev-console/

### Paso 2: Configurar Webhook

En **Configuration** → **Webhook**:

- **Callback URL:** `https://tu-dominio.com/webhook`
- **Verify Token:** `Vending-key-123` (del .env)
- **Subscribe fields:** `messages`

### Paso 3: Prueba

Meta enviará un GET para verificar. Tu servidor debe responder con el challenge.

---

## 💬 Cómo Funciona

### 1️⃣ Cliente envía mensaje por WhatsApp

```
Juan: "La máquina se acabó de bebidas, piso 3"
```

### 2️⃣ Meta webhook envía mensaje a tu servidor

```
POST /webhook
{
  "object": "whatsapp_business_account",
  "entry": [...]
}
```

### 3️⃣ VendingKit procesa

- **Brain 1 (Intent Detector):** Clasifica → `REPOSICION`
- **Brain 2 (Response Generator):** Genera respuesta → "Entendido, confirma ubicación exacta..."
- **Data Extraction:** Extrae nombre, piso, ubicación, etc.
- **Memory:** Guarda en SQLite
- **Sheets Sync:** Envía automáticamente a Google Sheets

### 4️⃣ Respuesta enviada

```
VendingKit: "Perfecto Juan, registré tu reposición para el piso 3..."
```

### 5️⃣ Incidente en Google Sheets

Se agrega automáticamente una fila con:
| Fecha | Teléfono | Nombre | Ubicación | Empresa | Piso | Extensión | Celular | Categoría | Descripción | Respuesta | Monto |
|-------|----------|--------|-----------|---------|------|-----------|---------|-----------|-------------|----------|-------|

---

## 🧪 Pruebas Incluidas

El archivo `tests/test_local.py` incluye casos de prueba para:

- ✅ REPOSICION
- ✅ RECLAMACION (con dinero perdido)
- ✅ RUTAS_ENTREGAS
- ✅ MANTENIMIENTO
- ✅ CONSULTA simple

Ejecuta:
```bash
python tests/test_local.py
```

---

## 📊 Monitorear Incidentes

### Ver incidentes guardados

```bash
curl http://localhost:8000/incidents
```

### Ver estado de configuración

```bash
curl http://localhost:8000/config/status
```

### Sincronizar manualmente con Sheets

```bash
curl -X POST http://localhost:8000/sync/sheets
```

---

## 🔧 Estructura del Proyecto

```
VendingKit/
├── agent/
│   ├── main.py           ← FastAPI app + webhook
│   ├── brain.py          ← Intent detector + response generator
│   ├── memory.py         ← SQLite conversation history
│   ├── sheets.py         ← Google Sheets integration
│   └── providers/
│       └── meta.py       ← Meta WhatsApp API
├── config/
│   ├── business.yaml     ← Config del negocio
│   └── prompts.yaml      ← Prompts de IA
├── tests/
│   └── test_local.py     ← Suite de pruebas
├── .env                  ← Credenciales (no versionar)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── vendingkit.db         ← BD SQLite (generada)
```

---

## 🚨 Troubleshooting

### "Módulo no encontrado"
```bash
pip install -r requirements.txt
```

### "Error de credenciales Meta"
Verifica que `META_ACCESS_TOKEN` sea válido y no haya expirado.

### "Google Sheets no funciona"
Asegúrate que la hoja es accesible públicamente o configurar OAuth.

### "Puerto 8000 ya en uso"
```bash
lsof -i :8000
kill -9 <PID>
```

---

## 📞 Soporte

Para problemas, revisa:
1. Logs: `python tests/test_local.py`
2. Estado: `curl http://localhost:8000/config/status`
3. Incidentes: `curl http://localhost:8000/incidents`

---

**VendingKit está listo. ¡Comienza a procesar mensajes! 🎉**
