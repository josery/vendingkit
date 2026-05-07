# 📂 VendingKit - Estructura de Proyecto

```
VendingKit/
│
├── 📁 agent/                          # Backend FastAPI
│   ├── main.py                        # Servidor FastAPI + webhook
│   ├── brain.py                       # Motor IA (IntentDetector + ResponseGenerator)
│   ├── memory.py                      # SQLite database + conversation history
│   ├── sheets.py                      # Google Sheets integration
│   ├── memory.py                      # Local incident storage
│   └── providers/
│       └── meta.py                    # Meta WhatsApp Cloud API handler
│
├── 📁 config/                         # Configuración
│   ├── business.yaml                  # Datos del negocio y máquinas
│   └── prompts.yaml                   # Prompts de IA para 9 categorías
│
├── 📁 tests/                          # Testing
│   └── test_local.py                  # Suite de pruebas locales
│
├── 🐳 Docker
│   ├── Dockerfile                     # Imagen Docker para producción
│   └── docker-compose.yml             # Composición para desarrollo
│
├── ⚙️ Configuración
│   ├── .env                           # Variables de entorno (local)
│   ├── .railwayignore                 # Archivos a ignorar en Railway
│   ├── railway.json                   # Configuración Railway
│   └── requirements.txt               # Dependencias Python
│
├── 📖 Documentación
│   ├── README_VENDINGKIT.md           # Guía de usuario principal
│   ├── CLAUDE.md                      # Especificación técnica del sistema
│   ├── SETUP_API_KEY.md               # Configuración de claves API
│   ├── DEPLOYMENT_RAILWAY.md          # Guía detallada de despliegue
│   ├── QUICK_START_PRODUCTION.md      # Inicio rápido (10-15 min)
│   ├── SYSTEM_STATUS.md               # Estado completo del sistema
│   └── PROJECT_STRUCTURE.md           # Este archivo
│
├── 📊 Base de Datos
│   └── vendingkit.db                  # SQLite (creado automáticamente)
│
└── 📝 Archivos Root
    ├── .gitignore                     # Git ignore rules
    └── .env                           # Variables de entorno
```

---

## 📁 Descripción por Carpeta

### `agent/` - Backend Principal
**Propósito**: Lógica de la aplicación
- `main.py` - Servidor FastAPI con endpoint /webhook/whatsapp
- `brain.py` - Orquestador de IA (intención → respuesta)
- `memory.py` - Persistencia de datos en SQLite
- `sheets.py` - Sincronización a Google Sheets
- `providers/meta.py` - Integración Meta WhatsApp

### `config/` - Configuración Estática
**Propósito**: Archivos YAML con configuración
- `business.yaml` - Nombre negocio, máquinas, horarios
- `prompts.yaml` - 9 prompts de IA específicos para vending

### `tests/` - Testing
**Propósito**: Validación del sistema
- `test_local.py` - 5 casos de prueba para desarrollo local

---

## 🔧 Archivos de Configuración

| Archivo | Propósito | Producción |
|---------|-----------|-----------|
| `.env` | Variables locales | No (secreto) |
| `requirements.txt` | Dependencias Python | Sí |
| `Dockerfile` | Imagen Docker | Sí |
| `docker-compose.yml` | Composición local | No |
| `railway.json` | Config Railway | Sí |
| `.railwayignore` | Archivos a ignorar | Sí |

---

## 📚 Documentación

| Documento | Audiencia | Contenido |
|-----------|-----------|----------|
| `README_VENDINGKIT.md` | Usuarios | Cómo usar el sistema |
| `CLAUDE.md` | Desarrolladores | Especificación técnica |
| `SETUP_API_KEY.md` | Configuradores | Generar claves API |
| `DEPLOYMENT_RAILWAY.md` | DevOps | Despliegue detallado |
| `QUICK_START_PRODUCTION.md` | Todos | 6 pasos en 15 min |
| `SYSTEM_STATUS.md` | Técnicos | Estado actual |

---

## 🚀 Flujo de Datos

```
WhatsApp
   ↓
POST /webhook/whatsapp (main.py)
   ↓
Extrae: phone, message
   ↓
brain.py:
   ├─ IntentDetector → Clasifica (9 categorías)
   ├─ ResponseGenerator → Respuesta personalizada
   └─ DataExtractor → Extrae datos (nombre, piso, etc.)
   ↓
memory.py:
   ├─ Guarda en SQLite
   └─ Guarda conversación
   ↓
sheets.py:
   └─ Sincroniza a Google Sheets (opcional)
   ↓
Respuesta → Meta API → WhatsApp
```

---

## 🔑 Variables de Entorno

```yaml
# API de Antropic
ANTHROPIC_API_KEY: sk-ant-api03-...

# Meta WhatsApp Cloud
META_ACCESS_TOKEN: EAA...
META_PHONE_NUMBER_ID: 9052...
META_BUSINESS_ACCOUNT_ID: 2189...
META_VERIFY_TOKEN: Vending-key-123

# Google Sheets
GOOGLE_SHEETS_ID: 15R_...
GOOGLE_CALENDAR_EMAIL: josery@gmail.com

# Servidor
PORT: 8000
HOST: 0.0.0.0
DEBUG: False (producción)
```

---

## 📦 Dependencias Principales

```yaml
# Framework Web
fastapi: 0.104.1
uvicorn: 0.24.0

# IA
anthropic: 0.21.0

# Configuración
python-dotenv: 1.0.0
pyyaml: 6.0.1

# Google
google-auth: 2.25.2
google-api-python-client: 2.107.0
gspread: 5.12.0

# Utilidades
requests: 2.31.0
pytz: 2023.3
```

---

## 🚀 Comandos Útiles

```bash
# Desarrollo Local
python3.11 tests/test_local.py

# Servidor Local
uvicorn agent.main:app --reload --port 8000

# Docker Local
docker-compose up --build

# Docker Production
docker build . -t vendingkit:latest
docker run -p 8000:8000 --env-file .env vendingkit:latest

# Listar Archivos del Proyecto
find . -type f -name "*.py" | head -20
```

---

## 🔄 Ciclo de Despliegue

```
Desarrollo Local
   ↓ (git push)
GitHub
   ↓ (auto-deploy)
Railway
   ↓ (build + run)
VendingKit en Producción 🚀
   ↓
WhatsApp Customers
```

---

## 📊 Tamaños de Archivo

```
agent/main.py:              ~500 líneas
agent/brain.py:             ~280 líneas
agent/memory.py:            ~200 líneas
agent/sheets.py:            ~150 líneas
agent/providers/meta.py:     ~300 líneas

config/business.yaml:       ~30 líneas
config/prompts.yaml:        ~200 líneas

tests/test_local.py:        ~120 líneas

Total Código: ~1,800 líneas
Total Documentación: ~1,500 líneas
```

---

## 🔐 Archivos Secretos

```
.env (NO versionar en Git)
   ├─ ANTHROPIC_API_KEY
   ├─ META_ACCESS_TOKEN
   └─ META_BUSINESS_ACCOUNT_ID

En Railway:
   └─ Todas las variables (seguras)
```

---

## 🎯 Flujo de Configuración

```
1. Crear .env con credenciales
   ↓
2. Instalar dependencias (pip install -r requirements.txt)
   ↓
3. Probar localmente (python tests/test_local.py)
   ↓
4. Subir a GitHub
   ↓
5. Conectar Railway
   ↓
6. Configurar variables en Railway
   ↓
7. Obtener URL pública
   ↓
8. Actualizar webhook en Meta
   ↓
9. ¡En vivo! 🚀
```

---

## 📈 Escalabilidad

```
Actual (1 instancia):     500-1000 msg/día
Con 2 replicas:           2000+ msg/día
Con 3 replicas + caché:   5000+ msg/día
```

---

## 🔧 Mantenimiento

```
Diario:
  - Revisar logs de errores
  - Verificar disponibilidad

Semanal:
  - Backup de SQLite
  - Análisis de incidentes

Mensual:
  - Actualizar dependencias
  - Revisión de performance
```

---

## 📞 Soporte

Para preguntas sobre:
- **Arquitectura**: Ver `CLAUDE.md`
- **Despliegue**: Ver `DEPLOYMENT_RAILWAY.md`
- **Errores**: Ver logs en Railway
- **Inicio rápido**: Ver `QUICK_START_PRODUCTION.md`

---

**VendingKit v1.0** - Sistema completo listo para producción
