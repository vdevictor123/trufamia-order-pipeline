# Guía de Instalación — TrufaMia Data Pipeline

## Requisitos previos

- Cuenta de Google con Gmail y Google Sheets activos
- Python 3.8 o superior instalado
- Proyecto en Google Cloud con las APIs **Google Sheets** y **Google Drive** habilitadas
- Cuenta de servicio (Service Account) con archivo `credentials.json` descargado

---

## 1. Instalar dependencias Python

```bash
pip install gspread google-auth fpdf2
```

---

## 2. Configurar credenciales

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un proyecto (o usa uno existente)
3. Activa las APIs: **Google Sheets API** y **Google Drive API**
4. Crea una **Service Account** → descarga la clave como `credentials.json`
5. Coloca `credentials.json` en la raíz del proyecto (**nunca lo subas a GitHub — está en `.gitignore`**)
6. Comparte tu Google Sheet con el email de la Service Account (con permisos de editor)

---

## 3. Crear la estructura del spreadsheet

Edita `scripts/crear_sheet.py` y actualiza las variables al inicio del archivo:

```python
CREDS_FILE     = "credentials.json"
SPREADSHEET_ID = "YOUR_SPREADSHEET_ID_HERE"
```

El `SPREADSHEET_ID` está en la URL de tu hoja:  
`https://docs.google.com/spreadsheets/d/`**`TU_ID_AQUI`**`/edit`

Luego ejecuta:

```bash
python scripts/crear_sheet.py
```

Esto crea las 4 hojas (PEDIDOS, VENTAS, CLIENTES, STOCK) con sus cabeceras, formatos, desplegables y fórmulas.

---

## 4. Instalar el Apps Script en Google Sheets

1. Abre tu Google Sheet
2. Ve a **Extensiones → Apps Script**
3. Borra el código por defecto
4. Pega el contenido de `scripts/TrufaMia_AppsScript_v6.js`
5. Edita el bloque `CONFIG` al principio del script:

```javascript
const CONFIG = {
  EMAILS_AUTORIZADOS: [
    "your-email@gmail.com",           // ← tu email
    "collaborator-email@gmail.com"    // ← email del colaborador (si aplica)
  ],
  SPREADSHEET_ID: "YOUR_SPREADSHEET_ID_HERE",  // ← ID de tu hoja
  // resto sin cambios
};
```

6. Guarda el script (Ctrl+S), ponle un nombre al proyecto
7. Ejecuta `onOpen` una vez para conceder permisos
8. Recarga la hoja — aparecerá el menú **🍫 TrufaMia**

---

## 5. Generar la guía PDF (opcional)

Edita `scripts/generar_guia.py` y actualiza:

```python
URL    = "https://docs.google.com/spreadsheets/d/YOUR_SPREADSHEET_ID_HERE"
OUTPUT = "docs/Guia_de_uso.pdf"
```

Luego ejecuta:

```bash
python scripts/generar_guia.py
```

---

## 6. Probar el pipeline

Envía un email a tu cuenta de Gmail con:

```
Asunto: PEDIDO TRUFAMIA

Fecha de pedido: DD/MM/AAAA
Nombre: Test Cliente
Telefono: 600000000
Canal: WhatsApp
Pago: Bizum
Caja: 8

Sabores:
Coco: 4
Oreo: 4

Notas: Pedido de prueba
```

Después, en la hoja: **🍫 TrufaMia → 📬 Procesar emails de pedidos**

---

## Archivos sensibles — NUNCA subir a GitHub

| Archivo | Motivo |
|---|---|
| `credentials.json` | Clave privada de la Service Account de Google |
| `*.json` | Cualquier otro archivo JSON puede contener tokens |
| `.env` | Variables de entorno con datos sensibles |

Estos patrones ya están incluidos en `.gitignore`.
