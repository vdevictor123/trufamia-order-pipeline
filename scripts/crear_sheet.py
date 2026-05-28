#!/usr/bin/env python3
"""Rellena el Google Spreadsheet TrufaMia - Contabilidad 2025"""

import gspread
from google.oauth2.service_account import Credentials

CREDS_FILE     = "credentials.json"
SPREADSHEET_ID = "YOUR_SPREADSHEET_ID_HERE"

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]


def rgb(r, g, b):
    return {"red": r / 255.0, "green": g / 255.0, "blue": b / 255.0}


PINK   = rgb(255, 182, 193)
GREEN  = rgb(144, 238, 144)
BLUE   = rgb(173, 216, 230)
YELLOW = rgb(255, 255, 153)
RED    = rgb(255, 80,  80)


def header_req(sheet_id, num_cols, bg, row=0):
    return {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": row, "endRowIndex": row + 1,
                "startColumnIndex": 0, "endColumnIndex": num_cols
            },
            "cell": {"userEnteredFormat": {
                "backgroundColor": bg,
                "textFormat": {"bold": True, "fontSize": 10},
                "horizontalAlignment": "CENTER",
                "verticalAlignment": "MIDDLE",
                "wrapStrategy": "WRAP"
            }},
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)"
        }
    }


def freeze_req(sheet_id):
    return {
        "updateSheetProperties": {
            "properties": {
                "sheetId": sheet_id,
                "gridProperties": {"frozenRowCount": 1}
            },
            "fields": "gridProperties.frozenRowCount"
        }
    }


def dropdown_req(sheet_id, start_row, end_row, col, values):
    return {
        "setDataValidation": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row, "endRowIndex": end_row,
                "startColumnIndex": col, "endColumnIndex": col + 1
            },
            "rule": {
                "condition": {
                    "type": "ONE_OF_LIST",
                    "values": [{"userEnteredValue": str(v)} for v in values]
                },
                "showCustomUi": True,
                "strict": True
            }
        }
    }


def cond_red_req(sheet_id, start_row, end_row, col, idx=0):
    return {
        "addConditionalFormatRule": {
            "rule": {
                "ranges": [{
                    "sheetId": sheet_id,
                    "startRowIndex": start_row, "endRowIndex": end_row,
                    "startColumnIndex": col, "endColumnIndex": col + 1
                }],
                "booleanRule": {
                    "condition": {
                        "type": "NUMBER_LESS_THAN_EQ",
                        "values": [{"userEnteredValue": "5"}]
                    },
                    "format": {"backgroundColor": RED}
                }
            },
            "index": idx
        }
    }


def col_w(sheet_id, col, px):
    return {
        "updateDimensionProperties": {
            "range": {
                "sheetId": sheet_id, "dimension": "COLUMNS",
                "startIndex": col, "endIndex": col + 1
            },
            "properties": {"pixelSize": px},
            "fields": "pixelSize"
        }
    }


def row_h(sheet_id, start, end, px):
    return {
        "updateDimensionProperties": {
            "range": {
                "sheetId": sheet_id, "dimension": "ROWS",
                "startIndex": start, "endIndex": end
            },
            "properties": {"pixelSize": px},
            "fields": "pixelSize"
        }
    }


def note_req(sheet_id, row, col, text):
    return {
        "updateCells": {
            "rows": [{"values": [{"note": text}]}],
            "fields": "note",
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": row, "endRowIndex": row + 1,
                "startColumnIndex": col, "endColumnIndex": col + 1
            }
        }
    }


def upd(ws, values, range_name, **kwargs):
    """Wrapper para gspread 6.x: values primero, range segundo."""
    return ws.update(values, range_name, **kwargs)


# ──────────────────────────────────────────────────────────────
print("Conectando a Google Sheets...")
creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
gc = gspread.authorize(creds)

print("Abriendo spreadsheet...")
ss = gc.open_by_key(SPREADSHEET_ID)
print(f"  Conectado: {ss.title}")

# Locale y zona horaria
ss.batch_update({"requests": [{
    "updateSpreadsheetProperties": {
        "properties": {"locale": "en_US", "timeZone": "Europe/Madrid"},
        "fields": "locale,timeZone"
    }
}]})

# Limpiar: borrar todas las hojas excepto la primera y dejar solo una en blanco
all_sheets = ss.worksheets()
first_id = all_sheets[0].id

# Borrar hojas extra de ejecuciones anteriores
delete_reqs = [
    {"deleteSheet": {"sheetId": ws.id}}
    for ws in all_sheets[1:]
]
if delete_reqs:
    ss.batch_update({"requests": delete_reqs})

# Renombrar la primera hoja a PEDIDOS y limpiar su contenido
ss.batch_update({"requests": [{"updateSheetProperties": {
    "properties": {"sheetId": first_id, "title": "PEDIDOS"},
    "fields": "title"
}}]})

# Recargar ws1 con el título actualizado
ws1 = ss.get_worksheet_by_id(first_id)
ws1.clear()

# Añadir las demás hojas
ws2 = ss.add_worksheet('VENTAS',   rows=100,  cols=5)
ws3 = ss.add_worksheet('CLIENTES', rows=500,  cols=10)
ws4 = ss.add_worksheet('STOCK',    rows=30,   cols=8)
id1, id2, id3, id4 = ws1.id, ws2.id, ws3.id, ws4.id


# ══════════════════════════════════════════════════════════════
# HOJA 1 — PEDIDOS
# ══════════════════════════════════════════════════════════════
print("Configurando PEDIDOS...")

upd(ws1, [[
    "Fecha", "Nombre cliente", "Telefono", "Canal", "Metodo de pago",
    "Unidades caja", "Precio EUR", "Sabores", "Nuevo o repetidor", "Semana", "Notas"
]], 'A1:K1')

upd(ws1, [
    [f'=IF(F{r}="","",IF(F{r}=4,6,IF(F{r}=8,11,IF(F{r}=15,20,IF(F{r}=16,21,IF(F{r}=25,32,IF(F{r}=35,45,IF(F{r}=100,120,""))))))))'
     ] for r in range(2, 202)
], 'G2:G201', value_input_option='USER_ENTERED')

upd(ws1, [
    [f'=IF(B{r}="","",IF(COUNTIF($B$2:B{r},B{r})>1,"Repetidor","Nuevo"))']
    for r in range(2, 202)
], 'I2:I201', value_input_option='USER_ENTERED')

upd(ws1, [
    [f'=IF(A{r}="","",WEEKNUM(A{r},2))'] for r in range(2, 202)
], 'J2:J201', value_input_option='USER_ENTERED')

ss.batch_update({"requests": [
    header_req(id1, 11, PINK),
    freeze_req(id1),
    dropdown_req(id1, 1, 201, 3, ["WhatsApp", "Instagram", "En persona"]),
    dropdown_req(id1, 1, 201, 4, ["Bizum", "Efectivo"]),
    dropdown_req(id1, 1, 201, 5, [4, 8, 15, 16, 25, 35, 100]),
    col_w(id1, 0, 100), col_w(id1, 1, 160), col_w(id1, 2, 110),
    col_w(id1, 3, 110), col_w(id1, 4, 130), col_w(id1, 5, 110),
    col_w(id1, 6, 85),  col_w(id1, 7, 220), col_w(id1, 8, 150),
    col_w(id1, 9, 75),  col_w(id1, 10, 220),
    row_h(id1, 0, 1, 40),
]})


# ══════════════════════════════════════════════════════════════
# HOJA 2 — VENTAS
# ══════════════════════════════════════════════════════════════
print("Configurando VENTAS...")

SABORES = [
    "Coco", "Chocolate con leche", "Chocolate blanco", "Chocolate 50%",
    "Maracuya", "Limon", "Churros", "Ferrero Rocher", "Oreo",
    "Leche nido con Nutella", "Sorpresa de uva",
    "Queso Mahon con dulce de guayaba", "Chocolate belga",
    "Prestigio", "Casadinho", "Fresa", "Pistacho", "Caramelo salado"
]

upd(ws2, [["Sabor", "Num Pedidos", "Ingresos estimados EUR"]], 'A1:C1')

ventas_rows = [
    [s,
     f'=COUNTIF(PEDIDOS!H:H,"*"&A{i+2}&"*")',
     f'=IFERROR(ROUND(B{i+2}*AVERAGE(PEDIDOS!G$2:G$201),2),0)']
    for i, s in enumerate(SABORES)
]
total_r = len(SABORES) + 2
ventas_rows.append(["TOTAL", f'=SUM(B2:B{total_r-1})', f'=SUM(C2:C{total_r-1})'])
upd(ws2, ventas_rows, f'A2:C{total_r}', value_input_option='USER_ENTERED')

ss.batch_update({"requests": [
    header_req(id2, 3, GREEN),
    freeze_req(id2),
    {
        "repeatCell": {
            "range": {
                "sheetId": id2,
                "startRowIndex": total_r - 1, "endRowIndex": total_r,
                "startColumnIndex": 0, "endColumnIndex": 3
            },
            "cell": {"userEnteredFormat": {
                "textFormat": {"bold": True},
                "backgroundColor": rgb(100, 200, 100)
            }},
            "fields": "userEnteredFormat(textFormat,backgroundColor)"
        }
    },
    col_w(id2, 0, 260), col_w(id2, 1, 110), col_w(id2, 2, 170),
    row_h(id2, 0, 1, 40),
]})


# ══════════════════════════════════════════════════════════════
# HOJA 3 — CLIENTES
# ══════════════════════════════════════════════════════════════
print("Configurando CLIENTES...")

upd(ws3, [[
    "Nombre", "Telefono", "Total pedidos",
    "Ultimo pedido", "Canal", "Tipo", "Total gastado EUR"
]], 'A1:G1')

ss.batch_update({"requests": [
    header_req(id3, 7, BLUE),
    freeze_req(id3),
    note_req(id3, 0, 0,
        "Para actualizar: copia los nombres unicos de la columna B "
        "(Nombre cliente) de PEDIDOS y pegales aqui. "
        "Usa COUNTIF para contar el total de pedidos por cliente."),
    col_w(id3, 0, 180), col_w(id3, 1, 120), col_w(id3, 2, 120),
    col_w(id3, 3, 130), col_w(id3, 4, 110), col_w(id3, 5, 100), col_w(id3, 6, 130),
    row_h(id3, 0, 1, 40),
]})


# ══════════════════════════════════════════════════════════════
# HOJA 4 — STOCK
# ══════════════════════════════════════════════════════════════
print("Configurando STOCK...")

upd(ws4, [["Tipo caja", "Stock inicial", "Vendidas", "Stock actual", "Estado"]], 'A1:E1')

CAJAS = [4, 8, 15, 16, 25, 35, 100]
upd(ws4, [
    [c, 20,
     f'=COUNTIF(PEDIDOS!F:F,A{i+2})',
     f'=B{i+2}-C{i+2}',
     f'=IF(D{i+2}<=5,"PEDIR YA",IF(D{i+2}<=10,"Stock bajo","OK"))']
    for i, c in enumerate(CAJAS)
], f'A2:E{len(CAJAS)+1}', value_input_option='USER_ENTERED')

upd(ws4, [["Material", "Stock inicial", "Usado", "Restante", "Estado"]], 'A12:E12')

MATERIALES = ["Cajas carton", "Cintas", "Tarjetas", "Papel seda"]
upd(ws4, [
    [m, 50, "",
     f'=B{i+13}-C{i+13}',
     f'=IF(D{i+13}<=5,"PEDIR YA",IF(D{i+13}<=10,"Stock bajo","OK"))']
    for i, m in enumerate(MATERIALES)
], f'A13:E{len(MATERIALES)+12}', value_input_option='USER_ENTERED')

ss.batch_update({"requests": [
    header_req(id4, 5, YELLOW, row=0),
    header_req(id4, 5, YELLOW, row=11),
    freeze_req(id4),
    cond_red_req(id4, 1,  8,  3, idx=0),
    cond_red_req(id4, 12, 16, 3, idx=1),
    col_w(id4, 0, 130), col_w(id4, 1, 110), col_w(id4, 2, 90),
    col_w(id4, 3, 110), col_w(id4, 4, 140),
    row_h(id4, 0, 1, 40),
    row_h(id4, 11, 12, 40),
]})


# ──────────────────────────────────────────────────────────────
url = f'https://docs.google.com/spreadsheets/d/{ss.id}'
print()
print("Spreadsheet listo")
print(f"URL: {url}")
