# ⚙️ Configuración de Claves API

## Situación Actual

VendingKit está **100% listo**. Todo funciona excepto:
- ❌ La clave API de Anthropic en `.env` no es válida
- ❌ Google Sheets necesita credenciales OAuth (más adelante)

## Solución: Generar Nueva Clave API de Anthropic

### Paso 1: Abre la Consola de Anthropic

Ve a: **https://console.anthropic.com/login**

### Paso 2: Inicia Sesión

- Haz clic en **"Continue with Google"**
- Usa: **josery@gmail.com**
- Autoriza

### Paso 3: Genera Nueva Clave

1. En el panel lateral, ve a **Settings**
2. Luego **API Keys**
3. Haz clic en **+ Create Key**
4. Dale un nombre (ej: "VendingKit Prod")
5. Haz clic en **Create Key**

### Paso 4: Copia la Clave

Deberás ver un modal con tu clave. **Cópiala COMPLETAMENTE** (no la cierres sin copiar).

La clave comienza con: `sk-ant-api...`

### Paso 5: Actualiza el .env

Abre el archivo `.env` en tu editor:

```
/Users/jvasquez/Documents/Proyectos Claude/VendingKit/.env
```

Reemplaza esta línea:

```bash
ANTHROPIC_API_KEY=sk-ant-api03-ppBIesoG5otirmBVuKLeMS5RwDn-yvsDC4VaN4YzrxJDITbj5TNr2Jysheq1I4ToG-PrAmozVE8nis4-YFiXA-_pp0YgAA
```

Con la nueva clave que copiaste:

```bash
ANTHROPIC_API_KEY=sk-ant-api03-[tu-nueva-clave]
```

### Paso 6: Prueba Nuevamente

```bash
cd /Users/jvasquez/Documents/Proyectos\ Claude/VendingKit
python3.11 tests/test_local.py
```

Si todo funciona, deberías ver:
```
🎯 Intención: REPOSICION
📝 Respuesta: Perfecto, registré tu solicitud de reposición...
```

---

## Verificar que la Clave Funciona

Una vez actualizado el `.env`, ejecuta:

```bash
python3.11 << 'EOF'
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv("/Users/jvasquez/Documents/Proyectos Claude/VendingKit/.env")

try:
    client = Anthropic()
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=10,
        messages=[{"role": "user", "content": "Hola"}]
    )
    print("✓ Clave API válida y funcionando")
except Exception as e:
    print(f"✗ Error: {e}")
EOF
```

Si ves `✓ Clave API válida`, ¡listo!

---

## ⚠️ Importante

- **No compartas tu clave API** públicamente
- Si la accidentalmente comparte, regenera inmediatamente en la consola
- Mantenla privada en `.env` (no versiones en Git)

---

## Próximos Pasos

Cuando tengas la clave API funcionando:

1. ✅ Prueba local funciona
2. ⬜ Configura Google Sheets (opcional, pero recomendado)
3. 🚀 Despliega a Railway

---

**¿Necesitas ayuda?** Lee `START_HERE.md`
