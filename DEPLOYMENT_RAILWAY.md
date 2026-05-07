# 🚀 VendingKit Railway Deployment Guide

VendingKit está **100% listo** para desplegarse a Railway. Este documento te guía paso a paso.

---

## 📋 Pre-Requisitos

✅ Código: Completo y funcional  
✅ Docker: Dockerfile configurado  
✅ Tests: Pasando localmente  
✅ Variables de entorno: Documentadas en railway.json  

---

## 🌐 Paso 1: Crear Cuenta en Railway

1. Ve a: **https://railway.app**
2. Haz clic en **"Create Account"**
3. Elige autenticación (GitHub recomendado)
4. Autoriza la conexión

---

## 📦 Paso 2: Crear Nuevo Proyecto en Railway

1. En el dashboard, haz clic en **"New Project"**
2. Elige **"Deploy from GitHub"** (o cargar manualmente)
3. Selecciona este repositorio VendingKit
4. Haz clic en **"Create"**

---

## ⚙️ Paso 3: Configurar Variables de Entorno

Railway detectará automáticamente el Dockerfile. Antes de desplegar, agrega las variables de entorno:

En el panel de Railway:
1. Ve a la pestaña **"Variables"** 
2. Agrega CADA una de estas variables con su valor:

```
ANTHROPIC_API_KEY=sk-ant-api03-[tu-clave]
META_ACCESS_TOKEN=[tu-token-meta]
META_PHONE_NUMBER_ID=[tu-numero-id]
META_BUSINESS_ACCOUNT_ID=[tu-business-id]
META_VERIFY_TOKEN=Vending-key-123
GOOGLE_SHEETS_ID=15R_caZHMICAbMHTeqirMHrtaX5BhkH8WdrHGrW3dvUY
GOOGLE_CALENDAR_EMAIL=josery@gmail.com
```

**IMPORTANTE:** Copia los valores EXACTOS de tu archivo `.env` local.

---

## 🔗 Paso 4: Obtener URL de Despliegue

Después de desplegar:
1. Railway asignará automáticamente una URL como: `https://vendingkit-prod-[id].railway.app`
2. Ve a la pestaña **"Deployments"** para verla
3. Copia esta URL (la necesitarás en el Paso 6)

---

## 🌍 Paso 5: Configurar Webhook en Meta

Con la URL de Railway, configura el webhook en Meta Developer Console:

1. Ve a: **https://developers.facebook.com/apps/[tu-app-id]/whatsapp-business/wa-dev-console/**
2. Sección **"Webhooks"**:
   - **Callback URL**: `https://[tu-url-railway]/webhook/whatsapp`
   - **Verify Token**: `Vending-key-123` (debe coincidir con META_VERIFY_TOKEN)
3. Haz clic en **"Verify and Save"**

Railway probará automáticamente la conexión.

---

## ✅ Paso 6: Probar la Conexión

Envía un mensaje de prueba desde WhatsApp a tu número de prueba:

```
"Hola, soy Juan de la empresa Test. La máquina se acabó de bebidas."
```

Deberías recibir una respuesta como:

```
"Hola Juan! Gracias por avisar. Coordino inmediatamente con nuestro equipo de reposición..."
```

---

## 📊 Paso 7: Monitoreo y Logs

En Railway:
1. Ve a **"Logs"** para ver los eventos en tiempo real
2. Ve a **"Database"** si conectaste PostgreSQL para Google Sheets sync
3. Ve a **"Deployments"** para ver el historial de despliegues

---

## 🔄 Paso 8: Actualizaciones Futuras

Para actualizar VendingKit después de cambios:

### Opción A: Git (Recomendado)
```bash
git push origin main
```
Railway redesplegará automáticamente.

### Opción B: Manual
1. Ve a **"Deployments"**
2. Haz clic en **"Deploy"**
3. Selecciona la rama y confir ma

---

## 🆘 Troubleshooting

### "Deployment Failed"
- Revisa los **Logs** en Railway
- Asegúrate de que todas las variables de entorno están configuradas
- Verifica que el Dockerfile es válido: `docker build . -t vendingkit-test`

### "Webhook Error 401"
- META_VERIFY_TOKEN no coincide entre Railway y Meta
- Verifica en Railway que la variable está correcta

### "No hay respuesta"
- Revisa los **Logs** en Railway para errores de API
- Verifica que ANTHROPIC_API_KEY es válida
- Confirma que META_PHONE_NUMBER_ID es correcto

### "Google Sheets no sincroniza"
- Por ahora es OK, sincronización es opcional
- Puedes configurarla más adelante con GOOGLE_APPLICATION_CREDENTIALS

---

## 📞 Configuración de Múltiples Máquinas

Railway soporta múltiples instancias. Para escalar:

1. Ve a **"Settings"** → **"Scaling"**
2. Aumenta "Replicas" a 2-3 (para redundancia)
3. Railway balanceará automáticamente la carga

---

## 🎯 Resumen: Estados del Despliegue

| Estado | Significado | Acción |
|--------|-------------|--------|
| ✅ Running | Sistema en vivo | ¡Funcionando! |
| 🟡 Building | Se está construyendo | Espera 2-3 min |
| ❌ Failed | Error durante build | Revisa los logs |
| ⏸️ Stopped | Despliegue pausado | Haz clic en "Resume" |

---

## 🎉 ¡Listo!

VendingKit está oficialmente en vivo y disponible desde WhatsApp en todo el mundo.

**Próximos Pasos Opcionales:**
- Configurar dominio personalizado
- Conectar Google Sheets completamente
- Configurar alertas de errores
- Monitorear analíticas

---

**Cualquier pregunta o issue durante el despliegue, consulta los logs en Railway.**
