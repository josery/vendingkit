# 🎉 VendingKit — Bienvenida

Felicidades. Tu **VendingKit** está completamente configurado y listo para usar.

---

## ✅ Estado Actual

### Credenciales Configuradas (6/6)
- ✅ **ANTHROPIC_API_KEY** — Claude API
- ✅ **META_ACCESS_TOKEN** — WhatsApp Cloud API
- ✅ **META_PHONE_NUMBER_ID** — 905292252675991
- ✅ **META_VERIFY_TOKEN** — Vending-key-123
- ✅ **GOOGLE_SHEETS_ID** — 15R_caZHMICAbMHTeqirMHrtaX5BhkH8WdrHGrW3dvUY
- ✅ **GOOGLE_CALENDAR_EMAIL** — josery@gmail.com

### Componentes Generados
- ✅ **Backend FastAPI** — Servidor HTTP con webhook
- ✅ **AI Brain** — Dos agentes Claude especializados
- ✅ **Memory System** — Base de datos SQLite
- ✅ **Google Sheets Integration** — Sincronización automática
- ✅ **Meta WhatsApp Provider** — Conexión directa a WhatsApp
- ✅ **Docker Setup** — Listo para desplegar

---

## 🚀 Próximos Pasos

Elige tu camino según tu situación:

### 📍 Opción A: Quiero Probar Localmente (Desarrollo)

**Tiempo:** 5 minutos  
**Complejidad:** Baja

```bash
# 1. Abre Terminal
# 2. Ve al directorio
cd /Users/jvasquez/Documents/Proyectos\ Claude/VendingKit

# 3. Instala dependencias
pip install -r requirements.txt

# 4. Prueba el agente localmente
python tests/test_local.py

# 5. Observa:
#    - Intenciones detectadas (REPOSICION, RECLAMACION, etc.)
#    - Respuestas generadas por Claude
#    - Datos extraídos del mensaje
#    - Sincronización con Google Sheets
```

📖 **Guía completa:** [QUICKSTART.md](./QUICKSTART.md)

---

### 🌐 Opción B: Quiero Desplegar a Producción (Railway)

**Tiempo:** 15 minutos  
**Complejidad:** Media

```bash
# 1. Crea cuenta en railway.app
# 2. Conecta tu repo de GitHub
# 3. Configura variables de entorno en Railway
# 4. Railway desplega automáticamente
# 5. Configura webhook en Meta
```

📖 **Guía completa:** [DEPLOY.md](./DEPLOY.md)

---

### 🐳 Opción C: Quiero Usar Docker Local

**Tiempo:** 10 minutos  
**Complejidad:** Media-Baja

```bash
# Con Docker Compose (recomendado)
docker-compose up

# O construye manualmente
docker build -t vendingkit .
docker run -p 8000:8000 --env-file .env vendingkit
```

El servidor estará en: `http://localhost:8000`

---

## 📋 Archivo por Archivo

### 🧠 Sistema de IA

| Archivo | Propósito |
|---------|-----------|
| `agent/brain.py` | 2 agentes Claude: detección de intención + generación de respuesta |
| `agent/main.py` | Servidor FastAPI con webhook |
| `agent/memory.py` | Almacenamiento local en SQLite |
| `agent/sheets.py` | Sincronización con Google Sheets |
| `agent/providers/meta.py` | Integración con Meta WhatsApp Cloud API |

### ⚙️ Configuración

| Archivo | Propósito |
|---------|-----------|
| `config/business.yaml` | Info del negocio (nombre, máquinas, horarios) |
| `config/prompts.yaml` | Prompts especializados para vending |
| `.env` | Credenciales (NO versionar) |

### 📦 Despliegue

| Archivo | Propósito |
|---------|-----------|
| `requirements.txt` | Dependencias Python |
| `Dockerfile` | Imagen Docker |
| `docker-compose.yml` | Orquestación local |
| `railway.json` | Config para Railway |
| `.gitignore` | Archivos a ignorar en Git |

### 📚 Documentación

| Archivo | Propósito |
|---------|-----------|
| `QUICKSTART.md` | Guía de inicio rápido |
| `DEPLOY.md` | Despliegue a Railway |
| `START_HERE.md` | Este archivo |
| `CLAUDE.md` | Especificación técnica |

### 🧪 Testing

| Archivo | Propósito |
|---------|-----------|
| `tests/test_local.py` | Suite de pruebas interactivas |

---

## 💬 Cómo Funciona

### 1. Cliente envía mensaje por WhatsApp

```
Cliente: "La máquina de piso 3 se quedó sin bebidas"
```

### 2. Meta webhook notifica a tu servidor

Tu servidor recibe el mensaje en `POST /webhook`

### 3. VendingKit procesa

1. **Intent Detector** → Clasifica como `REPOSICION`
2. **Response Generator** → Genera respuesta natural
3. **Data Extractor** → Extrae: nombre, piso, ubicación, etc.
4. **Memory** → Guarda en SQLite
5. **Google Sheets** → Sincroniza automáticamente

### 4. Respuesta enviada

```
VendingKit: "Recibido. Registré reposición para piso 3.
¿Cuál es la ubicación exacta de la máquina?"
```

### 5. Incidente aparece en Google Sheets

Automáticamente se agrega una fila con todos los datos extraídos.

---

## 🎯 Categorías que Reconoce

VendingKit detecta automáticamente:

| Categoría | Ejemplos |
|-----------|----------|
| **REPOSICION** | "Se acabó", "llenar", "refill", "sin producto" |
| **MANTENIMIENTO** | "No funciona", "dañado", "roto", "error" |
| **FALLO_DISPENSACION** | "Atrapado", "no sale", "trancado" |
| **RECLAMACION** | "Perdí dinero", "cobró dos veces" |
| **RUTAS_ENTREGAS** | "¿Cuándo llegan?", "próxima reposición" |
| **FINANCIAMIENTO** | "¿Cuánto cuesta?", "quiero poner una" |
| **CONSULTA_VENTAS** | "Qué vende más", "estadísticas" |
| **CONSULTA** | "Precios", "ubicación", "horario" |
| **CONVERSACION** | Saludos simples, charla casual |

---

## 🛠️ Comandos Útiles

### Desarrollo
```bash
# Prueba local completa
python tests/test_local.py

# Inicia servidor
python -m uvicorn agent.main:app --reload --port 8000

# Ver incidentes
curl http://localhost:8000/incidents

# Ver configuración
curl http://localhost:8000/config/status
```

### Docker
```bash
# Local con compose
docker-compose up

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

### Git
```bash
# Si planeas versionarlo
git init
git add .
git commit -m "Initial VendingKit setup"
git remote add origin https://github.com/tuusuario/vendingkit
git push -u origin main
```

---

## 📞 Problemas Comunes

### "ModuleNotFoundError: No module named 'anthropic'"
```bash
pip install -r requirements.txt
```

### "Error de credenciales Meta"
Verifica en `.env` que el token no esté expirado.

### "Google Sheets no sincroniza"
- Verifica que el SHEETS_ID sea correcto
- Comprueba que la hoja sea pública o accesible

### "Puerto 8000 ya en uso"
```bash
lsof -i :8000  # Ver qué está usando el puerto
kill -9 <PID>  # Liberar puerto
```

---

## 🎓 Aprendiendo

Para entender mejor VendingKit:

1. **Lee CLAUDE.md** — Especificación técnica completa
2. **Ejecuta test_local.py** — Ve el agente en acción
3. **Abre agent/brain.py** — Entiende cómo funciona la IA
4. **Modifica config/prompts.yaml** — Personaliza respuestas

---

## 🎉 ¡Empieza!

### Para desarrollo rápido:
```bash
python tests/test_local.py
```

### Para producción:
```bash
# Ve a railway.app y sigue DEPLOY.md
```

### Para desarrollo local:
```bash
python -m uvicorn agent.main:app --reload
```

---

## 📚 Próxima Lectura

Basado en tu siguiente acción:

- **Quiero probar ahora** → [QUICKSTART.md](./QUICKSTART.md)
- **Quiero desplegar** → [DEPLOY.md](./DEPLOY.md)
- **Quiero entender todo** → [CLAUDE.md](./CLAUDE.md)

---

**Felicitaciones por tener VendingKit listo. 🚀**

¿Preguntas? Revisa los archivos de documentación o ejecuta `python tests/test_local.py` para ver todo en acción.
