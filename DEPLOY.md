# VendingKit — Despliegue a Railway

Railway es la opción más fácil para desplegar VendingKit sin configuraciones complicadas.

---

## 🚀 Despliegue Rápido a Railway

### Paso 1: Crea una cuenta en Railway

1. Ve a https://railway.app
2. Regístrate con GitHub (recomendado) o email
3. Crea un nuevo proyecto

### Paso 2: Conecta tu repositorio

1. En Railway, haz clic en **"New Project"**
2. Selecciona **"GitHub Repo"**
3. Conecta tu repositorio de VendingKit
4. Autoriza Railway a acceder a GitHub

### Paso 3: Configura las variables de entorno

En Railway, ve a **Settings** → **Environment**

Agrega estas variables (copia del `.env`):

```
ANTHROPIC_API_KEY=sk-ant-api03-[tu-clave]

META_ACCESS_TOKEN=EAAMEgKMKMlABRRgirCcuisIqB8RufTtUx1OpM8KpLvsvxEbJ5ZCi4AwIDpFEaXAZBi6ZBF5oo1DBsdrH3X3jAZBbLxIJZANtgTie0stwpYwMmQxNxOjRYgh3wAY2oto3WCsuM4ZBXjlyeFKdfwGGzppzDZCeTKdS26Uqe3VZBJ4lOZBAXiFZAkOY9ZA4Y1NBNuLDvBNZBkZAh4TppnvFVDZC6XLwKyxtF9sXQrWnH70rAJWNXSVfgtv9m4s3jUYP4DQUgIvtSP3LjrzxsnepkSFBSMXMp7

META_PHONE_NUMBER_ID=905292252675991

META_VERIFY_TOKEN=Vending-key-123

GOOGLE_SHEETS_ID=15R_caZHMICAbMHTeqirMHrtaX5BhkH8WdrHGrW3dvUY

GOOGLE_CALENDAR_EMAIL=josery@gmail.com

PORT=8000

DEBUG=False
```

### Paso 4: Railway detecta automáticamente

Railway detectará:
- `Dockerfile` → Construirá la imagen
- `requirements.txt` → Instalará dependencias
- `railway.json` (si existe) → Configuración personalizada

### Paso 5: Despliega

1. Haz un `git push` a tu rama principal
2. Railway detectará cambios automáticamente
3. Iniciará el build y despliegue
4. Tu app estará live en ~3-5 minutos

---

## 🔗 Configura el Webhook en Meta

Una vez desplegado en Railway:

### 1. Obtén la URL pública

En Railway:
- Ve a tu proyecto
- Busca la sección **Deployments**
- Copia la URL (algo como `https://vendingkit-prod.railway.app`)

### 2. Configura en Meta Developer Console

1. Ve a https://developers.facebook.com/apps/849375467811408/whatsapp-business/wa-dev-console/
2. En **Configuration** → **Webhook**:
   - **Callback URL:** `https://vendingkit-prod.railway.app/webhook`
   - **Verify Token:** `Vending-key-123`
   - **Subscribe to:** `messages`

3. Haz clic en **Verify and Save**

Meta enviará un GET para verificar tu servidor. Si todo está bien:
```
✓ Webhook successfully verified
```

---

## 📊 Monitorear en Railway

### Logs en tiempo real
```bash
railway logs -f
```

### Ver estado del app
```bash
railway status
```

### Variables de entorno actualizadas
```bash
railway env list
```

---

## 🔄 Updates y Redeployes

Cada vez que hagas `git push`:
1. Railway detecta cambios
2. Reinicia el build automáticamente
3. El app se actualiza sin downtime

Para forzar un redeploy sin cambios:
```bash
railway redeploy
```

---

## 🛑 Troubleshooting en Railway

### App no inicia
Revisa logs:
```bash
railway logs -f
```

Busca errores como:
- Módulos faltantes → Actualiza `requirements.txt`
- Credenciales inválidas → Verifica `.env`
- Puerto incorrecto → Railway asigna puerto automáticamente

### Webhook no recibe mensajes
1. Verifica que la URL sea correcta
2. Prueba con `curl`:
```bash
curl https://tu-app.railway.app/health
```

3. Si falla, revisa logs de Railway

### BD SQLite se pierde entre redeployes

Railway usa un sistema de archivos efímero. Para persistencia:

**Opción A: Usa PostgreSQL**
1. En Railway, agrega servicio PostgreSQL
2. Actualiza `memory.py` para usar `psycopg2`

**Opción B: Sincroniza con Google Sheets**
- Todos los incidentes se guardan automáticamente en Sheets
- SQLite es solo cache local

Recomendamos **Opción B** para VendingKit.

---

## 💰 Costos

Railway ofrece:
- **Gratis:** Primeros $5 USD/mes
- **Pago:** $0.10 por CPU-hour, $0.05 por GB-hour

Para VendingKit (bajo uso):
- ~$0.50-2 USD/mes

---

## 🔐 Seguridad

### DO:
✅ Usa variables de entorno para credenciales
✅ Mantén `.env` fuera de Git (añade a `.gitignore`)
✅ Usa HTTPS (Railway lo hace automáticamente)
✅ Limpia logs regularmente

### DON'T:
❌ Hardcodea credenciales en código
❌ Hagas commit del `.env`
❌ Compartas tokens públicamente
❌ Ejecutes comandos SQL sin validar

---

## 📋 Checklist de Despliegue

- [ ] Cuenta en Railway creada
- [ ] Repositorio conectado a Railway
- [ ] Variables de entorno configuradas
- [ ] Build completado exitosamente
- [ ] App está en status "Running"
- [ ] URL pública obtenida
- [ ] Webhook configurado en Meta
- [ ] Webhook verificado en Meta ✓
- [ ] Prueba manual de mensaje enviado
- [ ] Incidente aparece en Google Sheets

---

## 🎉 ¡Listo!

Tu VendingKit está ahora en producción. Los clientes pueden enviar mensajes por WhatsApp y el agente responderá automáticamente.

**Próximos pasos:**
1. Invita operadores a usar el bot
2. Monitorea incidentes en Google Sheets
3. Ajusta prompts si es necesario
4. Escala según demanda

---

**¿Preguntas?** Revisa los logs de Railway o contacta soporte.
