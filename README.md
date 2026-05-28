# 🍫 TrufaMia — Automated Order Management System

> **EN** | A data pipeline built to automate order management for a family-owned artisan food business, eliminating manual data entry and enabling real-time business insights.

> **ES** | Pipeline de datos construido para automatizar la gestión de pedidos de un negocio familiar artesanal, eliminando la entrada manual de datos y habilitando métricas de negocio en tiempo real.

---

![Google Sheets](https://img.shields.io/badge/Google%20Sheets-34A853?style=flat&logo=google-sheets&logoColor=white)
![Google Apps Script](https://img.shields.io/badge/Apps%20Script-4285F4?style=flat&logo=google&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Gmail API](https://img.shields.io/badge/Gmail%20API-EA4335?style=flat&logo=gmail&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## Table of Contents / Índice

- [The Problem](#the-problem--el-problema)
- [The Solution](#the-solution--la-solución)
- [Architecture](#architecture--arquitectura)
- [Tech Stack](#tech-stack)
- [Features](#features--funcionalidades)
- [Data Model](#data-model)
- [Roadmap](#roadmap)
- [Project Structure](#project-structure)
- [Setup](#setup--instalación)
- [Key Learnings](#key-learnings)

---

## The Problem / El Problema

**EN** — A small artisan food business run by a single person managing everything alone: production, sales, delivery, accounting, and customer relations. Orders arrived informally through social media and messaging apps, recorded manually (or not at all), making it impossible to track:

- Which products sell most
- Revenue per week/month
- Customer purchase history
- Stock levels

**ES** — Un pequeño negocio artesanal gestionado por una sola persona que lleva todo: producción, ventas, entregas, contabilidad y atención al cliente. Los pedidos llegaban de forma informal por redes sociales y mensajería, registrándose manualmente (o sin registrarse), lo que hacía imposible saber:

- Qué productos se venden más
- Ingresos por semana/mes
- Historial de compras de clientes
- Niveles de stock

---

## The Solution / La Solución

**EN** — A fully automated data pipeline that:
1. Receives structured order emails from authorised senders
2. Parses and validates all fields automatically
3. Writes structured rows to Google Sheets
4. Updates sales analytics, customer records and stock in real time
5. Sends automatic error feedback if the email format is wrong

**ES** — Un pipeline de datos completamente automatizado que:
1. Recibe emails de pedido con formato estructurado de remitentes autorizados
2. Parsea y valida todos los campos automáticamente
3. Escribe filas estructuradas en Google Sheets
4. Actualiza analíticas de ventas, registros de clientes y stock en tiempo real
5. Envía feedback de error automático si el formato del email es incorrecto

---

## Architecture / Arquitectura

```
Order received (WhatsApp / Instagram / In person)
                      ↓
          Staff sends structured email
          to business Gmail account
                      ↓
           ┌─────────────────────┐
           │    Gmail Inbox      │
           │  Subject: PEDIDO    │
           │  [BUSINESS_KEYWORD] │
           └──────────┬──────────┘
                      ↓
           ┌─────────────────────┐
           │    Apps Script      │  ← Triggered manually from Sheet menu
           │   (JavaScript)      │
           │                     │
           │  1. Auth check      │  ← Only authorised senders processed
           │  2. Parse fields    │  ← Name, Phone, Channel, Payment...
           │  3. Extract items   │  ← "Product:quantity" format
           │  4. Validate sum    │  ← Quantities must equal box size
           │  5. Generate ID     │  ← Auto-incremented order ID
           └──────────┬──────────┘
                      ↓
    ┌─────────────────────────────────────┐
    │           Google Sheets             │
    │                                     │
    │  PEDIDOS   → One row per order      │
    │  VENTAS    → Product analytics      │
    │  CLIENTES  → Customer records       │
    │  STOCK     → Inventory tracking     │
    └─────────────────────────────────────┘
```

---

## Tech Stack

| Technology | Role | Why chosen |
|---|---|---|
| **Google Apps Script** (JS) | Core automation engine | Native Google ecosystem, no external services |
| **Gmail API** | Email ingestion | Direct integration via Apps Script |
| **Google Sheets** | Data storage & analytics | Accessible to non-technical users, free |
| **Python + fpdf** | PDF documentation | Automated end-user guide generation |
| **Python + gspread** | Initial sheet setup | Programmatic structure, dropdowns, formulas |
| **Google Drive API** | Spreadsheet access | Via service account credentials |

---

## Features / Funcionalidades

### Email → Sheet Pipeline
- Parses structured emails automatically
- Validates all mandatory fields (Name, Phone, Channel, Payment, Box size, Products)
- Normalises input variations: `WS` / `wpp` / `WHATSAPP` → `WhatsApp`
- Validates that product quantities sum to the correct box size
- Generates unique auto-incremented order IDs
- Sends automatic error reply with corrected template if format is wrong
- Marks processed emails with a Gmail label to avoid double-processing

### Sales Analytics (VENTAS sheet)
- Units sold per product + number of orders per product
- Boxes sold per size + total revenue per box type
- Auto-updates on every processing run

### Customer Management (CLIENTES sheet)
- Auto-creates new customer records from incoming orders
- Auto-updates: total orders, last order date, main channel, total spent
- Preserves manually-entered fields (customer type: individual/wholesale)
- Identifies customers by phone number as primary key

### Stock Tracking (STOCK sheet)
- Tracks box inventory by size
- Tracks packaging materials
- Auto-calculates units sold and remaining stock
- Conditional formatting: red alert when stock ≤ 5 units

### Visual Product Selector
- Sidebar panel inside Google Sheets for manual order entry
- Numeric input per product with real-time running total
- Validates sum against box size before writing to cell

---

## Data Model

### PEDIDOS (Orders)

| Column | Field | Type | Source |
|---|---|---|---|
| A | ID Pedido | String `Pyyyy-NNN` | Auto-generated |
| B | Fecha pedido | Date | Email or today |
| C | Fecha entrega | Date | Email (optional) |
| D | Nombre cliente | String | Email |
| E | Telefono | String | Email |
| F | Canal | Enum | Email (normalised) |
| G | Metodo de pago | Enum | Email (normalised) |
| H | Unidades caja | Integer | Email |
| I | Precio EUR | Integer | Auto (price lookup) |
| J | Sabores | String | Email (`"ProductA:10, ProductB:5"`) |
| K | Nuevo o repetidor | Enum | Formula (COUNTIF) |
| L | Semana | Integer | Formula (WEEKNUM) |
| M | Notas | String | Email (optional) |

### CLIENTES (Customers)

| Column | Field | Source |
|---|---|---|
| A | Nombre | Auto (latest from PEDIDOS) |
| B | Telefono | Auto — **primary key** |
| C | Total pedidos | Auto-calculated |
| D | Ultimo pedido | Auto-calculated |
| E | Canal | Auto (most frequent) |
| F | Tipo | **Manual** (Particular / Mayorista) |
| G | Total gastado EUR | Auto-calculated |

---

## Roadmap

### Completed
- [x] Google Sheet structure with 4 tabs (PEDIDOS, VENTAS, CLIENTES, STOCK)
- [x] Dropdown validation for Channel, Payment, Box size
- [x] Auto-formulas: price lookup, new/returning customer, week number
- [x] Gmail → Sheets pipeline via Apps Script
- [x] Email field validation with automatic error reply
- [x] Input normalisation (multiple variants → canonical values)
- [x] Product quantities format in email (`Product: quantity`)
- [x] Quantity sum validation against box size
- [x] Auto-incremented order ID generation
- [x] Sales analytics: units per product + revenue per box type
- [x] Customer records auto-update on order processing
- [x] Visual product selector sidebar with quantity inputs
- [x] Optional delivery date field
- [x] PDF end-user guide (Python/fpdf)
- [x] Manual processing mode (menu-driven, no background triggers)

### In Progress
- [ ] WhatsApp integration (evaluating options)
- [ ] Email template refinement based on real usage feedback

### Planned
- [ ] Weekly revenue summary email report
- [ ] Low stock automatic alert
- [ ] Customer ID linked to orders (full relational model)
- [ ] Dashboard tab with charts (revenue trend, top products)
- [ ] SQL/database migration for larger data volumes
- [ ] Power BI / Looker Studio connection

---

## Project Structure

```
TrufaMia-Data-Pipeline/
│
├── README.md
│
├── scripts/
│   ├── TrufaMia_AppsScript_v6.js   # Main automation — Gmail → Sheets
│   ├── crear_sheet.py               # Sheet structure setup via gspread
│   └── generar_guia.py              # PDF user guide generator
│
├── docs/
│   ├── Guia_Instalacion.md          # Step-by-step installation guide
│   ├── Plantilla_Email.txt          # Order email template
│   └── Guia_de_uso.pdf              # End-user PDF guide
│
└── assets/
    └── screenshots/                 # Sheet, VENTAS, CLIENTES screenshots
```

---

## Setup / Instalación

> ⚠️ **Important / Importante:** This project handles real business data.
> All credentials, IDs and email addresses have been removed from this repo.
> You must configure your own values before use.

### Prerequisites
- Google Account with Gmail and Google Sheets
- Google Cloud project with Sheets + Drive APIs enabled (for Python scripts)
- Apps Script access in Google Sheets (Extensions → Apps Script)

### 1. Configure the spreadsheet (Python)

```bash
pip install gspread google-auth fpdf2

# Add your Google Service Account credentials as credentials.json
# NEVER commit this file — it's in .gitignore

python scripts/crear_sheet.py
```

### 2. Configure the Apps Script

Open `scripts/TrufaMia_AppsScript_v6.js` and update the CONFIG block:

```javascript
const CONFIG = {
  ASUNTO_EMAIL: "PEDIDO TRUFAMIA",        // Subject line to watch for

  EMAILS_AUTORIZADOS: [
    "your-email@gmail.com",               // ← replace with your email
    "collaborator-email@gmail.com"        // ← replace with collaborator email
  ],

  SPREADSHEET_ID: "YOUR_SPREADSHEET_ID", // ← from your Google Sheet URL
  // ...
};
```

### 3. Install in Google Sheets

1. Open your Google Sheet
2. Extensions → Apps Script
3. Delete default code, paste the configured script
4. Save (Ctrl+S), name the project
5. Run `onOpen` once to grant permissions
6. Reload the Sheet — **🍫 TrufaMia** menu should appear

### 4. Test with a sample order

Send an email to your Gmail with:

```
Subject: PEDIDO TRUFAMIA

Fecha de pedido: 17/05/2026
Fecha de entrega: 21/05/2026
Nombre: Test cliente
Telefono: 600000000
Canal: WhatsApp
Pago: Bizum
Caja: 25

Sabores:
Coco: 5
Chocolate con leche: 5
Chocolate blanco: 5
Chocolate 50%: 
Maracuya: 
Limon: 
Churros: 
Ferrero Rocher: 5
Oreo: 5
Leche nido con Nutella: 
Sorpresa de uva: 
Queso Mahon con dulce de guayaba: 
Chocolate belga: 
Prestigio: 
Casadinho: 
Fresa: 
Pistacho: 
Caramelo salado: 

Notas: Sin frutos secos

Notas: Test
```

Then in the Sheet: **🍫 TrufaMia → 📬 Procesar emails de pedidos**

### .gitignore (critical)

```
credentials.json
credentials_json.json
*.json
.env
```

---

## Key Learnings

**EN**
- Designed a real-world ETL pipeline using only Google's free ecosystem
- Applied data normalisation to handle human input variations at ingestion time
- Built a relational data model (Orders ↔ Customers ↔ Sales) from scratch
- Used AI-assisted development to accelerate the build while learning JavaScript
- Validated that data quality at the source is the foundation of any reliable analytics system

**ES**
- Diseñé un pipeline ETL real usando únicamente el ecosistema gratuito de Google
- Apliqué normalización de datos para gestionar variaciones de input humano en la ingesta
- Construí un modelo de datos relacional (Pedidos ↔ Clientes ↔ Ventas) desde cero
- Usé desarrollo asistido por IA para acelerar la construcción mientras aprendía JavaScript
- Validé que la calidad del dato en el origen es la base de cualquier sistema de analítica fiable

---

## About / Sobre el proyecto

**EN** — Built to help a family member who recently started a small business and was managing everything manually. The goal: reduce administrative friction so they can focus on what they do best.

Also a practical learning project in JavaScript, API integration, and data pipeline design — complementing a background in data analytics.

**ES** — Construido para ayudar a un familiar que acaba de empezar un pequeño negocio y lo gestionaba todo manualmente. El objetivo: reducir la fricción administrativa para que pueda centrarse en lo que mejor sabe hacer.

También un proyecto de aprendizaje práctico en JavaScript, integración de APIs y diseño de pipelines de datos — complementando un perfil de analista de datos.

---

*Built with ❤️ and 🍫*