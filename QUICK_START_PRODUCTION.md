# 🚀 VendingKit - Guía Rápida Despliegue a Producción

**Estado Actual**: ✅ Sistema 100% funcional  
**Tiempo hasta Producción**: 10-15 minutos  

---

## 📋 Checklist Previo

- [x] Código desarrollado ✅
- [x] Tests pasados (65 incidentes) ✅
- [x] Docker configurado ✅
- [x] Variables de entorno configuradas ✅
- [x] Meta WhatsApp tokens válidos ✅
- [x] Google Sheets configurado ✅
- [x] API Key Anthropic activa ✅

**RESULTADO**: Listo para desplegarse

---

## 🌐 Paso 1: Railway (2 minutos)

```bash
1. Ve a: https://railway.app
2. Crea cuenta con GitHub
3. Nuevo proyecto → Deploy from GitHub
4. Selecciona: VendingKit
5. Clic: Create
```

---

## ⚙️ Paso 2: Configurar Variables (3 minutos)

En Railway Dashboard → Variables:

```
ANTHROPIC_API_KEY=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

META_ACCESS_TOKEN=EAAMEgKMKMlABRRgirCcuisIqB8RufTtUx1OpM8KpLvsvxEbJ5ZCi4AwIDpFEaXAZBi6ZBF5oo1DBsdrH3X3jAZBbLxIJZANtgTie0stwpYwMmQxNxOjRYgh3wAY2oto3WCsuM4ZBXjlyeFKdfwGGzppzDZCeTKdS26Uqe3VZBJ4lOZBAXiFZAkOY9ZA4Y1NBNuLDvBNZBkZAh4TppnvFVDZC6XLwKyxtF9sXQrWnH70rAJWNXSVfgtv9m4s3jUYP4DQUgIvtSP3LjrzxsnepkSFBSMXMp7

META_PHONE_NUMBER_ID=905292252675991

META_BUSINESS_ACCOUNT_ID=2189685348208011

META_VERIFY_TOKEN=Vending-key-123

GOOGLE_SHEETS_ID=15R_caZHMICAbMHTeqirMHrtaX5BhkH8WdrHGrW3dvUY

GOOGLE_CALENDAR_EMAIL=josery@gmail.com
```

---

## 🚀 Paso 3: Deploy (Automático)

Railway comenzará automáticamente:
- Build del Docker ⏳ (2-3 min)
- Start del servidor 🚀 (30 seg)
- Asignación de URL 🌐 (automático)

**Estado**: Ve a "Deployments" para seguir

---

## 🔗 Paso 4: Obtener URL Pública

En Railway → Deployments:
```
URL asignada: https://vendingkit-[random].railway.app
```

Cópiala (la usarás en el paso siguiente).

---

## 🌍 Paso 5: Meta Webhook (2 minutos)

Ve a: https://developers.facebook.com/apps/849375467811408/whatsapp-business/wa-dev-console/

**Webhooks** sección:
```
Callback URL: https://[tu-url-railway]/webhook/whatsapp
Verify Token: Vending-key-123
```

Clic: "Verify and Save"

---

## ✅ Paso 6: Test (30 segundos)

Envía WhatsApp:
```
"Hola, la máquina se acabó de bebidas"
```

**Respuesta esperada:**
```
"Hola! Registré tu solicitud de reposición..."
```

---

## 🎉 ¡LISTO!

**VendingKit está EN VIVO** 🚀

---

## 📊 Monitoreo

- **Logs**: Railway → Logs (ver mensajes en tiempo real)
- **Errores**: Railway → Alerts (notificaciones)
- **BD**: SQLite en Railway (persiste automáticamente)

---

## 🆘 Si algo falla

### Error: "Webhook failed verification"
- Verifica META_VERIFY_TOKEN es exactamente: `Vending-key-123`

### Error: "No reply from Claude"
- Verifica ANTHROPIC_API_KEY es válido
- Ve a Railway → Logs para más detalles

### Error: "Webhook timeout"
- Railway puede tardar primeros 30s
- Intenta enviar otro mensaje

---

## 🎯 Siguientes Mejoras (Opcional)

- [ ] Google Sheets sync completo (add auth)
- [ ] Dominio personalizado
- [ ] Alertas de errores por email
- [ ] Dashboard de analytics
- [ ] Multi-idioma

---

## 📞 Más Información

Documentación completa en:
- `DEPLOYMENT_RAILWAY.md` - Guía detallada
- `SYSTEM_STATUS.md` - Estado del sistema
- `CLAUDE.md` - Especificación técnica

---

**¡Enhorabuena! 🎊 Tu agente WhatsApp está en producción.**
