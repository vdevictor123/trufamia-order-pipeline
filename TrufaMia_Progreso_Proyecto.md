# 🍫 TrufaMia — Registro de Progreso del Proyecto

> **Uso:** Recordatorio personal para retomar el proyecto donde lo dejaste.  
> **Última actualización:** Mayo 2025

---

## ¿Qué es este proyecto?

Sistema de automatización contable para **TrufaMia** (tienda artesanal de brigadeiros en España).  
La idea: Ella (tu cuñada) recibe pedidos por email → el sistema los registra automáticamente en Google Sheets.

**Stack usado:**
- Python + gspread (para crear y rellenar el Sheet)
- Google Cloud Service Account (para dar permisos al script)
- Google Apps Script (para la automatización de emails)
- fpdf (para generar el PDF de la guía)

---

## ✅ PASO 1 — Crear el proyecto en Google Cloud

**Qué se hizo:**  
Se creó un proyecto llamado `trufamia-analytics` en Google Cloud Console.  
Esto es necesario para poder usar las APIs de Google (Sheets y Gmail) desde Python.

**Por qué:**  
Google no deja que cualquier script acceda a tus hojas directamente. Necesitas un proyecto cloud que actúe como "puerta de entrada" oficial.

**Resultado:** Proyecto `trufamia-analytics` activo en console.cloud.google.com

---

## ✅ PASO 2 — Crear una Service Account y descargar credenciales

**Qué se hizo:**  
Se creó una cuenta de servicio llamada `trufamia-bot` dentro del proyecto.  
Se descargó el archivo `credentials.json` con las claves privadas del bot.

**Por qué:**  
Una Service Account es como un "usuario robot". El script de Python se identifica como ese robot para poder leer y escribir en Google Sheets sin necesitar que tú inicies sesión cada vez.

**Archivo generado:** `credentials.json.json`  
**Email del bot:** `trufamia-bot@trufamia-analytics.iam.gserviceaccount.com`

> ⚠️ **IMPORTANTE:** Este archivo contiene claves privadas. No lo subas a GitHub nunca. Añádelo al `.gitignore`.

---

## ✅ PASO 3 — Activar las APIs necesarias

**Qué se hizo:**  
Se activaron dos APIs en Google Cloud Console:
- **Google Sheets API** → para que el script pueda leer/escribir en el spreadsheet
- **Google Drive API** → para que el script pueda encontrar y abrir el archivo por ID

**Por qué:**  
Las APIs están desactivadas por defecto. Sin activarlas, el script da error aunque las credenciales sean correctas.

---

## ✅ PASO 4 — Compartir el Spreadsheet con el bot

**Qué se hizo:**  
El Google Sheet fue compartido manualmente con el email del bot (`trufamia-bot@...`) con permisos de **Editor**.

**Por qué:**  
Aunque el bot tenga credenciales, Google Sheets funciona como cualquier documento: si no tienes acceso compartido, no puedes editarlo. El bot necesita estar en la lista de editores.

**Sheet ID:** `1Cx_3_lq3zmh4UzG8sCbT36n_zNGF-V5X_X9Sl8Gwq6k`

---

## ✅ PASO 5 — Script `crear_sheet.py` (configurar el Spreadsheet)

**Qué se hizo:**  
Se escribió y ejecutó el script `crear_sheet.py` que:
1. Se conecta al Sheet con las credenciales del bot
2. Borra el contenido anterior para empezar limpio
3. Crea las 4 pestañas: **PEDIDOS | VENTAS | CLIENTES | STOCK**
4. Añade cabeceras, fórmulas automáticas, desplegables y formatos de color

**Por qué:**  
Hacer esto a mano en Google Sheets llevaría horas y sería difícil de repetir. Con el script, si algo sale mal, lo ejecutas de nuevo y queda perfecto en segundos.

**Pestañas creadas y su función:**

| Pestaña | Qué hace | ¿Se actualiza sola? |
|---------|----------|---------------------|
| PEDIDOS | Registro de cada pedido (fecha, cliente, sabores, precio...) | No — se rellena manualmente |
| VENTAS | Ranking de sabores más vendidos + ingresos estimados | ✅ Sí — usa fórmulas de PEDIDOS |
| CLIENTES | Ficha de cada cliente | No — se actualiza manualmente |
| STOCK | Control de cajas y materiales disponibles | ✅ Parcial — "Vendidas" se calcula sola |

**Fórmulas clave añadidas automáticamente:**
- Columna G (Precio): se calcula según las unidades elegidas en el desplegable
- Columna I (Nuevo/Repetidor): detecta si el cliente ya había pedido antes
- Columna J (Semana): calcula el número de semana del año a partir de la fecha

---

## ✅ PASO 6 — Script `generar_guia.py` (PDF de instrucciones)

**Qué se hizo:**  
Se escribió el script `generar_guia.py` usando la librería `fpdf` para generar un PDF de 9 páginas con instrucciones de uso del Sheet.

**Por qué:**  
Tu cuñada Ella necesita saber cómo rellenar el Sheet correctamente (nombres exactos de sabores, usar los desplegables, etc.). El PDF es su manual de referencia.

**Resultado:** `TrufaMia_Guia_de_uso.pdf` — 9 páginas con portada, índice, instrucciones y referencia rápida.

---

## ✅ PASO 7 — Automatización con Google Apps Script (Gmail → Sheets)

**Qué se hizo:**  
Se creó un script en Google Apps Script (directamente dentro del Google Sheet) que:
1. Lee los emails nuevos de Gmail que Ella envía con el formato de pedido
2. Extrae los datos del email (nombre, teléfono, canal, sabores, etc.)
3. Escribe automáticamente una nueva fila en la pestaña PEDIDOS

**Por qué:**  
Sin esta automatización, alguien tendría que copiar manualmente los datos del email al Sheet. Con el script, Ella envía el email y el pedido aparece solo en el Sheet.

**Componentes del sistema:**
- **Gmail reader:** lee y parsea los emails entrantes
- **Panel visual (sidebar):** checkboxes para seleccionar los 18 sabores (columna H)
- **Menú personalizado:** botón "🍫 TrufaMia → Procesar emails" en el Sheet

**Modo de funcionamiento:** Manual (Victor hace clic cuando quiere procesar los emails)  
**Emails autorizados:** Solo los de la lista `EMAILS_AUTORIZADOS` en el script

**Campos que lee del email:**

| Campo | Obligatorio |
|-------|-------------|
| Nombre | ✅ Sí |
| Telefono | ✅ Sí |
| Canal (WS/IG/En persona) | ✅ Sí |
| Pago (Bizum/Efectivo) | ✅ Sí |
| Caja (4/8/15/16/25/35/100) | ✅ Sí |
| Sabores | ✅ Sí |
| Notas | ❌ Opcional |

> Si el email llega con algún campo mal o incompleto, el script **responde automáticamente** con un email de error indicando qué falta.

---

## 🔜 PRÓXIMOS PASOS (pendiente)

- [ ] Subir el código a GitHub con README
- [ ] Añadir `credentials.json` al `.gitignore`
- [ ] Probar el flujo completo con un email real de Ella
- [ ] Revisar si el PDF necesita actualización con los sabores exactos del catálogo
- [ ] Considerar añadir un trigger automático por tiempo (si el volumen de pedidos aumenta)

---

## 📁 Archivos del proyecto

```
TRUFAMIA/
├── crear_sheet.py          # Crea y configura el Google Sheet completo
├── generar_guia.py         # Genera el PDF de instrucciones para Ella
├── credentials.json.json   # ⚠️ Claves del bot — NO subir a GitHub
└── TrufaMia_Guia_de_uso.pdf  # Manual de uso para Ella
```

---

## 🔗 Links útiles

- **Google Sheet:** https://docs.google.com/spreadsheets/d/1Cx_3_lq3zmh4UzG8sCbT36n_zNGF-V5X_X9Sl8Gwq6k
- **Google Cloud Console:** https://console.cloud.google.com (proyecto: `trufamia-analytics`)
- **Apps Script:** Extensiones → Apps Script (dentro del Sheet)
