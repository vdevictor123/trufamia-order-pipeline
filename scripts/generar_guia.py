#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera la guia PDF de uso para TrufaMia - Contabilidad 2025"""

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from fpdf import FPDF

URL = "https://docs.google.com/spreadsheets/d/YOUR_SPREADSHEET_ID_HERE"
OUTPUT = "docs/Guia_de_uso.pdf"

# Paleta de colores
ROSA       = (220, 80,  110)   # frambuesa oscuro - color marca
ROSA_CLARO = (255, 182, 193)   # encabezados PEDIDOS
VERDE      = (50,  150, 80)    # verde oscuro texto
VERDE_CLARO= (144, 238, 144)   # encabezados VENTAS
AZUL       = (30,  100, 180)   # azul oscuro texto
AZUL_CLARO = (173, 216, 230)   # encabezados CLIENTES
AMARILLO   = (255, 220, 50)    # amarillo encabezados STOCK
GRIS_CLARO = (245, 245, 245)
GRIS_MED   = (200, 200, 200)
OSCURO     = (40,  40,  40)
BLANCO     = (255, 255, 255)
CREMA      = (255, 252, 240)


class PDF(FPDF):

    def header(self):
        if self.page_no() == 1:
            return
        self.set_fill_color(*ROSA)
        self.rect(0, 0, 210, 10, "F")
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*BLANCO)
        self.set_xy(0, 2)
        self.cell(150, 6, "  TrufaMia - Guia de uso de la hoja de calculo 2025")
        self.set_font("Helvetica", "", 7)
        self.cell(0, 6, f"Pag. {self.page_no()}  ", align="R")
        self.set_text_color(*OSCURO)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-12)
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*GRIS_MED)
        self.cell(0, 5, "TrufaMia.es  |  Documento interno", align="C")
        self.set_text_color(*OSCURO)

    # ── Bloques reutilizables ────────────────────────────────

    def titulo_seccion(self, numero, texto, color_bg, color_texto=None):
        self.ln(5)
        ct = color_texto or OSCURO
        self.set_fill_color(*color_bg)
        self.set_draw_color(*color_bg)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*ct)
        self.cell(0, 11, f"  {numero}.  {texto}", fill=True, ln=True)
        self.set_draw_color(0, 0, 0)
        self.ln(2)

    def subtitulo(self, texto, color=None):
        self.ln(3)
        c = color or ROSA
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*c)
        self.cell(0, 7, texto, ln=True)
        self.set_text_color(*OSCURO)

    def paso(self, numero, negrita, detalle=""):
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(*ROSA)
        self.set_text_color(*BLANCO)
        self.cell(7, 7, str(numero), fill=True, align="C")
        self.set_text_color(*OSCURO)
        self.set_font("Helvetica", "B", 9)
        self.cell(4, 7, "")
        self.cell(0, 7, negrita, ln=True)
        if detalle:
            self.set_font("Helvetica", "", 8.5)
            self.set_x(15)
            self.set_text_color(70, 70, 70)
            self.multi_cell(0, 5, detalle)
            self.set_text_color(*OSCURO)
        self.ln(1)

    def recuadro_consejo(self, texto):
        self.set_x(self.l_margin)
        self.set_fill_color(255, 250, 220)
        self.set_draw_color(255, 180, 0)
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(80, 60, 0)
        self.multi_cell(0, 5.5, f"  CONSEJO:  {texto}", border=1, fill=True)
        self.set_text_color(*OSCURO)
        self.set_x(self.l_margin)
        self.ln(2)

    def recuadro_atencion(self, texto):
        self.set_x(self.l_margin)
        self.set_fill_color(255, 235, 235)
        self.set_draw_color(200, 50, 50)
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(150, 0, 0)
        self.multi_cell(0, 5.5, f"  ATENCION:  {texto}", border=1, fill=True)
        self.set_text_color(*OSCURO)
        self.set_x(self.l_margin)
        self.ln(2)

    def recuadro_info(self, texto, color_bg, color_borde):
        self.set_x(self.l_margin)
        self.set_fill_color(*color_bg)
        self.set_draw_color(*color_borde)
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(*OSCURO)
        self.multi_cell(0, 5.5, f"  {texto}", border=1, fill=True)
        self.set_x(self.l_margin)
        self.ln(2)

    def fila_tabla(self, col1, col2, fill=False):
        bg = GRIS_CLARO if fill else BLANCO
        self.set_fill_color(*bg)
        self.set_font("Helvetica", "B", 8.5)
        self.set_text_color(*OSCURO)
        self.cell(55, 7, col1, fill=True, border=1)
        self.set_font("Helvetica", "", 8.5)
        self.cell(0, 7, col2, fill=True, border=1, ln=True)

    def fila_tabla_3(self, c1, c2, c3, header=False):
        bg = ROSA_CLARO if header else (BLANCO if self._fila_par else GRIS_CLARO)
        if not hasattr(self, "_fila_par"):
            self._fila_par = True
        self._fila_par = not self._fila_par
        self.set_fill_color(*bg)
        estilo = "B" if header else ""
        self.set_font("Helvetica", estilo, 8.5)
        self.cell(60, 7, f"  {c1}", fill=True, border=1)
        self.cell(55, 7, f"  {c2}", fill=True, border=1)
        self.cell(0,  7, f"  {c3}", fill=True, border=1, ln=True)


# ═══════════════════════════════════════════════════════════════
# DOCUMENTO
# ═══════════════════════════════════════════════════════════════
pdf = PDF()
pdf.set_margins(15, 15, 15)
pdf.set_auto_page_break(True, margin=18)


# ───────────────────────────────────────────────────────────────
# PAGINA 1 — PORTADA
# ───────────────────────────────────────────────────────────────
pdf.add_page()

# Fondo rosa
pdf.set_fill_color(*ROSA)
pdf.rect(0, 0, 210, 297, "F")

# Franja decorativa central
pdf.set_fill_color(200, 40, 70)
pdf.rect(0, 110, 210, 90, "F")

# Chocolatina decorativa (cuadrados)
for i in range(6):
    for j in range(4):
        pdf.set_fill_color(180 + i*5, 30 + j*5, 55 + i*3)
        pdf.rect(15 + i*30, 120 + j*18, 25, 14, "F")

# Titulo principal
pdf.set_y(38)
pdf.set_font("Helvetica", "B", 48)
pdf.set_text_color(*BLANCO)
pdf.cell(0, 22, "TrufaMia", align="C", ln=True)

pdf.set_font("Helvetica", "", 15)
pdf.set_text_color(255, 210, 220)
pdf.cell(0, 8, "Brigadeiros artesanales", align="C", ln=True)

pdf.ln(6)
pdf.set_fill_color(*BLANCO)
pdf.set_fill_color(255, 255, 255)
pdf.rect(40, pdf.get_y(), 130, 1, "F")
pdf.ln(8)

pdf.set_font("Helvetica", "B", 20)
pdf.set_text_color(*BLANCO)
pdf.cell(0, 11, "GUIA DE USO", align="C", ln=True)

pdf.set_font("Helvetica", "", 13)
pdf.set_text_color(255, 220, 230)
pdf.cell(0, 8, "Hoja de calculo - Contabilidad 2025", align="C", ln=True)

# Descripcion sobre la franja
pdf.set_y(215)
pdf.set_font("Helvetica", "B", 11)
pdf.set_text_color(*BLANCO)
pdf.cell(0, 8, "Todo lo que necesitas para gestionar tu negocio:", align="C", ln=True)
pdf.ln(2)

iconos = ["Registrar pedidos",  "Control de stock",
          "Ranking de sabores", "Base de clientes"]
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(255, 230, 235)
for item in iconos:
    pdf.cell(0, 7, f"           {item}", ln=True)

# Pie portada
pdf.set_y(268)
pdf.set_font("Helvetica", "", 8)
pdf.set_text_color(255, 190, 200)
pdf.cell(0, 5, "Documento confidencial  |  TrufaMia.es  |  Espana 2025", align="C", ln=True)


# ───────────────────────────────────────────────────────────────
# PAGINA 2 — INDICE + ACCESO
# ───────────────────────────────────────────────────────────────
pdf.add_page()
pdf.set_y(18)

pdf.set_font("Helvetica", "B", 20)
pdf.set_text_color(*ROSA)
pdf.cell(0, 11, "Indice", ln=True)
pdf.ln(2)

indice = [
    ("1", "Como acceder a la hoja",      "Enlace, movil y ordenador",           3),
    ("2", "Registrar un pedido",          "Hoja PEDIDOS - paso a paso",          4),
    ("3", "Consultar ventas y sabores",   "Hoja VENTAS - se actualiza sola",     6),
    ("4", "Gestionar el stock",           "Hoja STOCK - alertas en rojo",        7),
    ("5", "Base de clientes",             "Hoja CLIENTES",                       8),
    ("6", "Preguntas frecuentes",         "Soluciones a dudas comunes",          9),
]

for num, titulo, desc, pag in indice:
    pdf.set_fill_color(252, 242, 246)
    pdf.set_draw_color(*ROSA_CLARO)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*ROSA)
    pdf.cell(9, 9, num, fill=True, border=1, align="C")
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*OSCURO)
    pdf.cell(100, 9, f"   {titulo}", fill=True, border="TB")
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 9, f"   {desc}", fill=True, border="TBR", ln=True)
    pdf.ln(1)

pdf.ln(6)

# --- SECCION 1: ACCESO ---
pdf.titulo_seccion("1", "Como acceder a la hoja", ROSA_CLARO)

pdf.set_font("Helvetica", "", 9.5)
pdf.set_text_color(*OSCURO)
pdf.multi_cell(0, 6,
    "La hoja de calculo esta en Google Sheets y se puede abrir desde cualquier "
    "dispositivo con conexion a internet. No hace falta instalar nada.")
pdf.ln(3)

pdf.subtitulo("Desde el ordenador (recomendado para introducir datos)")
pdf.paso(1, "Abre Google Chrome o cualquier navegador")
pdf.paso(2, "Copia y pega este enlace en la barra de direcciones:",
    URL)
pdf.paso(3, "Inicia sesion con tu cuenta de Google si te lo pide")
pdf.paso(4, "La hoja se abre directamente lista para usar")

pdf.subtitulo("Desde el movil (para consultas rapidas)")
pdf.paso(1, "Instala la app gratuita 'Hojas de calculo de Google' (Google Sheets)")
pdf.paso(2, "Abre el enlace desde WhatsApp o el navegador del movil")
pdf.paso(3, "Se abrira directamente en la app")

pdf.recuadro_consejo(
    "Guarda el enlace en tus favoritos del navegador o en la pantalla de inicio "
    "del movil para acceder con un solo toque.")


# ───────────────────────────────────────────────────────────────
# PAGINA 3 — PEDIDOS (parte 1)
# ───────────────────────────────────────────────────────────────
pdf.add_page()
pdf.set_y(18)

pdf.titulo_seccion("2", "Registrar un pedido - Hoja PEDIDOS", ROSA_CLARO)

pdf.set_font("Helvetica", "", 9.5)
pdf.multi_cell(0, 6,
    "Esta es la hoja principal. Cada fila es un pedido. "
    "Rellena de izquierda a derecha. Algunas columnas se calculan solas.")
pdf.ln(3)

pdf.subtitulo("Paso a paso para cada pedido nuevo")

pdf.paso(1, "Abre la pestana PEDIDOS",
    "En la parte inferior de la hoja veras cuatro pestanas: "
    "PEDIDOS | VENTAS | CLIENTES | STOCK. Haz clic en PEDIDOS.")

pdf.paso(2, "Ve a la primera fila vacia",
    "Despues de la cabecera rosa, los datos empiezan en la fila 2. "
    "Busca la primera fila donde no haya nada escrito.")

pdf.paso(3, "Columna A - Fecha",
    "Escribe la fecha del pedido en formato DD/MM/AAAA.\n"
    "Ejemplo: 15/05/2025")

pdf.paso(4, "Columna B - Nombre cliente",
    "Escribe el nombre completo del cliente tal como lo conoces.\n"
    "IMPORTANTE: usa siempre el mismo formato para que el sistema detecte "
    "correctamente si es cliente nuevo o repetidor.")

pdf.paso(5, "Columna C - Telefono",
    "Escribe el numero de telefono. Puedes incluir el prefijo +34 o no.")

pdf.paso(6, "Columna D - Canal",
    "Haz clic en la celda. Aparecera una flecha con un desplegable.\n"
    "Selecciona de donde vino el pedido:\n"
    "   - WhatsApp\n"
    "   - Instagram\n"
    "   - En persona")

pdf.paso(7, "Columna E - Metodo de pago",
    "Selecciona del desplegable:\n"
    "   - Bizum\n"
    "   - Efectivo")

pdf.paso(8, "Columna F - Unidades caja",
    "Selecciona del desplegable el tamano de la caja:\n"
    "   4 / 8 / 15 / 16 / 25 / 35 / 100 unidades")

pdf.recuadro_atencion(
    "No escribas el numero directamente. Usa SIEMPRE el desplegable para que "
    "el precio se calcule automaticamente y el stock se actualice bien.")


# ───────────────────────────────────────────────────────────────
# PAGINA 4 — PEDIDOS (parte 2)
# ───────────────────────────────────────────────────────────────
pdf.add_page()
pdf.set_y(18)

pdf.set_font("Helvetica", "B", 14)
pdf.set_text_color(*ROSA)
pdf.cell(0, 9, "2.  Registrar un pedido (continuacion)", ln=True)
pdf.ln(2)

pdf.paso(9, "Columna G - Precio EUR  (automatica, no tocar)",
    "Esta columna se rellena SOLA segun las unidades que elegiste.\n"
    "No escribas nada aqui. Si ves un numero, es correcto.")

# Tabla de precios
pdf.set_y(pdf.get_y() + 2)
pdf.set_font("Helvetica", "B", 9)
pdf.set_fill_color(*ROSA_CLARO)
pdf.set_text_color(*OSCURO)
pdf.cell(40, 7, "  Unidades caja", fill=True, border=1)
pdf.cell(40, 7, "  Precio automatico", fill=True, border=1, ln=True)

precios = [("4 unidades","6 EUR"), ("8 unidades","11 EUR"), ("15 unidades","20 EUR"),
           ("16 unidades","21 EUR"), ("25 unidades","32 EUR"), ("35 unidades","45 EUR"),
           ("100 unidades","120 EUR")]
for i, (u, p) in enumerate(precios):
    bg = GRIS_CLARO if i % 2 == 0 else BLANCO
    pdf.set_fill_color(*bg)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.cell(40, 6, f"  {u}", fill=True, border=1)
    pdf.cell(40, 6, f"  {p}", fill=True, border=1, ln=True)
pdf.ln(3)

pdf.paso(10, "Columna H - Sabores",
    "Escribe los sabores que lleva la caja, separados por comas.\n"
    "Ejemplo: Coco, Chocolate con leche, Ferrero Rocher\n\n"
    "Usa los nombres exactos de la lista (los mismos que aparecen en la hoja VENTAS) "
    "para que el contador de sabores funcione correctamente.")

pdf.paso(11, "Columna I - Nuevo o repetidor  (automatica)",
    "Se detecta SOLA. Si el nombre del cliente ya aparece en una fila anterior, "
    "pondra 'Repetidor'. Si es la primera vez, pondra 'Nuevo'.\n"
    "No escribas nada aqui.")

pdf.paso(12, "Columna J - Semana  (automatica)",
    "Calcula automaticamente el numero de semana del ano a partir de la fecha. "
    "Util para ver cuantos pedidos tienes por semana.\n"
    "No escribas nada aqui.")

pdf.paso(13, "Columna K - Notas",
    "Campo libre para cualquier observacion:\n"
    "   - 'Entrega a domicilio calle Mayor 5'\n"
    "   - 'Sin frutos secos por alergia'\n"
    "   - 'Pago pendiente'\n"
    "   - 'Regalo, incluir tarjeta'")

pdf.ln(2)
pdf.recuadro_consejo(
    "Cuando termines de rellenar una fila, el pedido queda registrado automaticamente. "
    "No hay que guardar ni hacer nada mas. Los cambios se guardan solos en la nube.")

pdf.ln(3)

# Mini ejemplo visual
pdf.set_font("Helvetica", "B", 9)
pdf.set_text_color(*ROSA)
pdf.cell(0, 7, "Ejemplo de pedido completo:", ln=True)

pdf.set_font("Helvetica", "B", 7.5)
pdf.set_fill_color(*ROSA_CLARO)
pdf.set_text_color(*OSCURO)
cols  = ["Fecha", "Nombre", "Tel.", "Canal", "Pago", "Uds", "Precio", "Sabores", "Tipo", "Sem.", "Notas"]
widths= [18, 25, 18, 18, 14, 10, 12, 38, 18, 10, 0]
for c, w in zip(cols, widths):
    if w == 0:
        pdf.cell(0, 6, c, fill=True, border=1, ln=True)
    else:
        pdf.cell(w, 6, c, fill=True, border=1)

pdf.set_font("Helvetica", "", 7.5)
pdf.set_fill_color(*GRIS_CLARO)
vals   = ["10/05/25", "Test Cliente", "600000000", "WhatsApp", "Bizum", "8", "11", "Coco, Oreo, Limon...", "Nuevo", "19", "Caja regalo"]
for v, w in zip(vals, widths):
    if w == 0:
        pdf.cell(0, 6, v, fill=True, border=1, ln=True)
    else:
        pdf.cell(w, 6, v, fill=True, border=1)


# ───────────────────────────────────────────────────────────────
# PAGINA 5 — LISTA DE SABORES
# ───────────────────────────────────────────────────────────────
pdf.add_page()
pdf.set_y(18)

pdf.set_font("Helvetica", "B", 14)
pdf.set_text_color(*ROSA)
pdf.cell(0, 9, "2.  Nombres exactos de los sabores", ln=True)
pdf.ln(2)

pdf.set_font("Helvetica", "", 9.5)
pdf.set_text_color(*OSCURO)
pdf.multi_cell(0, 6,
    "Cuando escribas los sabores en la columna H de PEDIDOS, usa exactamente "
    "estos nombres para que el contador de la hoja VENTAS los reconozca bien:")
pdf.ln(3)

sabores = [
    ("1",  "Coco"),
    ("2",  "Chocolate con leche"),
    ("3",  "Chocolate blanco"),
    ("4",  "Chocolate 50%"),
    ("5",  "Maracuya"),
    ("6",  "Limon"),
    ("7",  "Churros"),
    ("8",  "Ferrero Rocher"),
    ("9",  "Oreo"),
    ("10", "Leche nido con Nutella"),
    ("11", "Sorpresa de uva"),
    ("12", "Queso Mahon con dulce de guayaba"),
    ("13", "Chocolate belga"),
    ("14", "Prestigio"),
    ("15", "Casadinho"),
    ("16", "Fresa"),
    ("17", "Pistacho"),
    ("18", "Caramelo salado"),
]

# Dos columnas
mid = len(sabores) // 2 + 1
col_izq = sabores[:mid]
col_der = sabores[mid:]

pdf.set_font("Helvetica", "B", 9)
pdf.set_fill_color(*ROSA_CLARO)
pdf.set_text_color(*OSCURO)
pdf.cell(8, 7, "N", fill=True, border=1, align="C")
pdf.cell(78, 7, "  Sabor", fill=True, border=1)
pdf.cell(4, 7, "")
pdf.cell(8, 7, "N", fill=True, border=1, align="C")
pdf.cell(0, 7, "  Sabor", fill=True, border=1, ln=True)

for i in range(max(len(col_izq), len(col_der))):
    bg = GRIS_CLARO if i % 2 == 0 else BLANCO
    pdf.set_fill_color(*bg)
    pdf.set_font("Helvetica", "", 8.5)

    if i < len(col_izq):
        n1, s1 = col_izq[i]
        pdf.cell(8, 7, f" {n1}", fill=True, border=1, align="C")
        pdf.cell(78, 7, f"  {s1}", fill=True, border=1)
    else:
        pdf.cell(86, 7, "", fill=True, border=1)
    pdf.cell(4, 7, "")
    if i < len(col_der):
        n2, s2 = col_der[i]
        pdf.cell(8, 7, f" {n2}", fill=True, border=1, align="C")
        pdf.cell(0, 7, f"  {s2}", fill=True, border=1, ln=True)
    else:
        pdf.cell(0, 7, "", fill=True, border=1, ln=True)

pdf.ln(4)
pdf.recuadro_consejo(
    "Puedes escribir varios sabores separados por comas: "
    "'Coco, Limon, Oreo, Ferrero Rocher'. "
    "El sistema buscara cada sabor individualmente y sumara uno al contador de cada uno.")

pdf.ln(4)
pdf.recuadro_atencion(
    "Si escribes 'chocolate' en lugar de 'Chocolate con leche', el contador NO lo contara. "
    "Usa siempre el nombre completo de la lista de arriba.")


# ───────────────────────────────────────────────────────────────
# PAGINA 6 — VENTAS
# ───────────────────────────────────────────────────────────────
pdf.add_page()
pdf.set_y(18)

pdf.titulo_seccion("3", "Consultar ventas y sabores - Hoja VENTAS", VERDE_CLARO)

pdf.set_font("Helvetica", "", 9.5)
pdf.multi_cell(0, 6,
    "La hoja VENTAS se actualiza automaticamente cada vez que introduces "
    "un pedido en PEDIDOS. No necesitas escribir nada aqui.")
pdf.ln(3)

pdf.subtitulo("Que contiene esta hoja", VERDE)

pdf.set_font("Helvetica", "B", 9)
pdf.set_fill_color(*VERDE_CLARO)
pdf.set_text_color(*OSCURO)
pdf.cell(60, 7, "  Columna", fill=True, border=1)
pdf.cell(0,  7, "  Que muestra", fill=True, border=1, ln=True)

filas_ventas = [
    ("Columna A - Sabor",           "El nombre de cada uno de los 18 sabores"),
    ("Columna B - N Pedidos",       "Cuantas veces se ha pedido ese sabor (se actualiza solo)"),
    ("Columna C - Ingresos estim.", "Estimacion de ingresos generados por ese sabor"),
    ("Fila TOTAL",                  "Suma total de todos los pedidos e ingresos"),
]
for i, (c, q) in enumerate(filas_ventas):
    bg = GRIS_CLARO if i % 2 == 0 else BLANCO
    pdf.set_fill_color(*bg)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.cell(60, 7, f"  {c}", fill=True, border=1)
    pdf.cell(0,  7, f"  {q}", fill=True, border=1, ln=True)

pdf.ln(4)
pdf.subtitulo("Como leer los datos", VERDE)

pdf.set_font("Helvetica", "", 9.5)
pdf.multi_cell(0, 6,
    "Mirando la columna B (N Pedidos) de mayor a menor, puedes ver facilmente "
    "cuales son tus sabores mas populares y cuales se venden menos.\n\n"
    "Usa esta informacion para decidir que sabores preparar cada semana "
    "y cuales promocionar en redes sociales.")
pdf.ln(3)

pdf.recuadro_consejo(
    "Si quieres ordenar los sabores de mas a menos vendido, haz clic en "
    "la columna B, luego en 'Datos' > 'Ordenar rango' > De mayor a menor.")

pdf.ln(4)
pdf.subtitulo("Cuando se actualizan los datos", VERDE)
pdf.set_font("Helvetica", "", 9.5)
pdf.multi_cell(0, 6,
    "Los contadores se recalculan en tiempo real cada vez que:\n"
    "   - Introduces un nuevo pedido en PEDIDOS\n"
    "   - Editas un pedido existente\n"
    "   - Borras un pedido\n\n"
    "No hace falta hacer nada especial. La hoja lo hace todo sola.")


# ───────────────────────────────────────────────────────────────
# PAGINA 7 — STOCK
# ───────────────────────────────────────────────────────────────
pdf.add_page()
pdf.set_y(18)

pdf.titulo_seccion("4", "Gestionar el stock - Hoja STOCK", (255, 230, 80))

pdf.set_font("Helvetica", "", 9.5)
pdf.multi_cell(0, 6,
    "La hoja STOCK tiene dos tablas: una para los tipos de caja y otra "
    "para los materiales. Las columnas de 'Vendidas' y 'Stock actual' "
    "se actualizan solas. Solo necesitas actualizar el Stock inicial cuando recibas nuevo material.")
pdf.ln(3)

pdf.subtitulo("Tabla 1: Stock de cajas (filas 2-8)", (160, 120, 0))

filas_stock = [
    ("Tipo caja",    "El tamano de la caja (4, 8, 15, 16, 25, 35 o 100 uds)"),
    ("Stock inicial","Cuantas cajas tienes en total. ACTUALIZA este numero cuando recibas mas"),
    ("Vendidas",     "Se calcula solo. Cuenta los pedidos de ese tamano en PEDIDOS"),
    ("Stock actual", "Se calcula solo. Es Stock inicial - Vendidas"),
    ("Estado",       "OK si tienes mas de 10 / Stock bajo si tienes 10 o menos / PEDIR YA si 5 o menos"),
]
pdf.set_font("Helvetica", "B", 9)
pdf.set_fill_color(255, 230, 80)
pdf.cell(38, 7, "  Columna", fill=True, border=1)
pdf.cell(0,  7, "  Que significa y que hacer", fill=True, border=1, ln=True)
for i, (c, q) in enumerate(filas_stock):
    bg = GRIS_CLARO if i % 2 == 0 else BLANCO
    pdf.set_fill_color(*bg)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.cell(38, 7, f"  {c}", fill=True, border=1)
    pdf.cell(0,  7, f"  {q}", fill=True, border=1, ln=True)

pdf.ln(3)

pdf.subtitulo("Que hacer cuando recibes nuevas cajas", (160, 120, 0))
pdf.paso(1, "Ve a la hoja STOCK")
pdf.paso(2, "Busca la fila del tamano de caja que has recibido")
pdf.paso(3, "Haz clic en la celda de la columna 'Stock inicial'",
    "Escribe el nuevo total de cajas que tienes ahora.\n"
    "Ejemplo: si tenias 20 y recibes 30 mas, escribe 50.")
pdf.paso(4, "El stock actual se recalcula solo")

pdf.recuadro_atencion(
    "La columna 'Stock inicial' es la UNICA que debes editar manualmente. "
    "No toques las columnas Vendidas, Stock actual ni Estado.")

pdf.ln(2)
pdf.subtitulo("Alertas de color", (160, 120, 0))
pdf.set_font("Helvetica", "", 9.5)
pdf.multi_cell(0, 6,
    "La columna 'Stock actual' cambia de color automaticamente:\n"
    "   - Fondo ROJO: tienes 5 o menos unidades. Hay que pedir ya.\n"
    "   - Sin color: todo esta bien.")
pdf.ln(3)

pdf.subtitulo("Tabla 2: Materiales (filas 12-16)", (160, 120, 0))
pdf.set_font("Helvetica", "", 9.5)
pdf.multi_cell(0, 6,
    "Funciona igual que la tabla de cajas pero para: Cajas carton, Cintas, Tarjetas y Papel seda.\n"
    "La columna 'Usado' la rellenas manualmente segun vayas gastando material. "
    "El 'Restante' se calcula solo.")


# ───────────────────────────────────────────────────────────────
# PAGINA 8 — CLIENTES + FAQ
# ───────────────────────────────────────────────────────────────
pdf.add_page()
pdf.set_y(18)

pdf.titulo_seccion("5", "Base de clientes - Hoja CLIENTES", AZUL_CLARO)

pdf.set_font("Helvetica", "", 9.5)
pdf.multi_cell(0, 6,
    "La hoja CLIENTES es una ficha de cada cliente. A diferencia de las otras, "
    "esta se actualiza manualmente cuando quieras tener el registro al dia.")
pdf.ln(2)

pdf.subtitulo("Como anadir un cliente nuevo", AZUL)
pdf.paso(1, "Ve a la hoja PEDIDOS y busca el nombre del nuevo cliente")
pdf.paso(2, "Ve a la hoja CLIENTES y baja hasta la primera fila vacia")
pdf.paso(3, "Rellena los datos: nombre, telefono, canal habitual y tipo (mayorista/particular)")
pdf.paso(4, "Las columnas 'Total pedidos' y 'Total gastado' las calculas tu mirando PEDIDOS",
    "Puedes usar la funcion COUNTIF si quieres que se calcule sola, "
    "o simplemente contar los pedidos a mano.")

pdf.recuadro_consejo(
    "Esta hoja es especialmente util para clientes habituales. "
    "Te permite ver de un vistazo cuanto ha gastado cada cliente y cuando fue su ultimo pedido.")

pdf.ln(4)

# ── PREGUNTAS FRECUENTES ──
pdf.titulo_seccion("6", "Preguntas frecuentes", (200, 200, 220))

faqs = [
    ("El precio no aparece automaticamente",
     "Asegurate de que seleccionaste las unidades del desplegable (columna F). "
     "Si escribiste el numero a mano en lugar de usar el desplegable, el precio "
     "no se calculara. Borra el numero y vuelve a seleccionarlo del desplegable."),

    ("Pone 'Repetidor' pero es un cliente nuevo",
     "Esto ocurre cuando el mismo nombre ya aparece en una fila anterior. "
     "Revisa si el nombre esta escrito exactamente igual en ambas filas. "
     "Si es realmente un cliente nuevo, puede que otro cliente tenga el mismo nombre: "
     "en ese caso anade el apellido para diferenciarlos."),

    ("No puedo escribir en una celda con desplegable",
     "Las celdas de Canal, Metodo de pago y Unidades caja solo aceptan los valores "
     "del desplegable. Haz clic en la celda y luego en la flecha que aparece."),

    ("La columna Semana muestra un numero raro",
     "Comprueba que la fecha en la columna A esta en formato correcto (DD/MM/AAAA). "
     "Si escribiste la fecha como texto (ej: '15 mayo') la formula no puede calcular la semana."),

    ("Borre una fila por error",
     "Pulsa Ctrl+Z (deshacer) inmediatamente. Google Sheets guarda el historial de cambios. "
     "Si ya cerraste la hoja, ve a Archivo > Historial de versiones > Ver historial de versiones."),

    ("La hoja va lenta o no carga",
     "Prueba a recargar la pagina (F5). "
     "Si usas el movil, cierra la app y vuelve a abrirla. "
     "Comprueba que tienes conexion a internet."),
]

for pregunta, respuesta in faqs:
    pdf.set_x(pdf.l_margin)
    pdf.set_fill_color(235, 235, 255)
    pdf.set_draw_color(150, 130, 210)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*AZUL)
    pdf.multi_cell(0, 6.5, f"  {pregunta}", border=1, fill=True)
    pdf.set_x(pdf.l_margin)
    pdf.set_fill_color(248, 248, 255)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 5.5, f"  {respuesta}", border=1, fill=True)
    pdf.set_text_color(*OSCURO)
    pdf.set_x(pdf.l_margin)
    pdf.ln(2)


# ───────────────────────────────────────────────────────────────
# PAGINA 9 — TARJETA DE REFERENCIA RAPIDA
# ───────────────────────────────────────────────────────────────
pdf.add_page()
pdf.set_y(18)

pdf.set_font("Helvetica", "B", 18)
pdf.set_text_color(*ROSA)
pdf.cell(0, 11, "Referencia rapida", ln=True)
pdf.set_font("Helvetica", "", 9.5)
pdf.set_text_color(*OSCURO)
pdf.cell(0, 6, "Recorta o guarda esta pagina en el movil como captura de pantalla", ln=True)
pdf.ln(4)

# Enlace
pdf.set_fill_color(250, 240, 245)
pdf.set_draw_color(*ROSA)
pdf.set_font("Helvetica", "B", 9)
pdf.set_text_color(*ROSA)
pdf.cell(0, 8, "  Enlace a la hoja:", fill=True, border="TLR", ln=True)
pdf.set_font("Helvetica", "", 7.5)
pdf.set_text_color(*AZUL)
pdf.cell(0, 7, f"  {URL}", fill=True, border="BLR", ln=True)
pdf.ln(4)

# Mini checklist de pedido
pdf.set_font("Helvetica", "B", 11)
pdf.set_text_color(*ROSA)
pdf.cell(0, 8, "Checklist: nuevo pedido en PEDIDOS", ln=True)
pdf.ln(1)

checks = [
    ("A", "Fecha (DD/MM/AAAA)"),
    ("B", "Nombre del cliente"),
    ("C", "Telefono"),
    ("D", "Canal (desplegable: WhatsApp / Instagram / En persona)"),
    ("E", "Metodo de pago (desplegable: Bizum / Efectivo)"),
    ("F", "Unidades caja (desplegable: 4 / 8 / 15 / 16 / 25 / 35 / 100)"),
    ("G", "Precio EUR  <- SE CALCULA SOLO"),
    ("H", "Sabores (separados por comas)"),
    ("I", "Nuevo o repetidor  <- SE DETECTA SOLO"),
    ("J", "Semana  <- SE CALCULA SOLA"),
    ("K", "Notas (opcional)"),
]

for col, desc in checks:
    auto = "SE CALCULA" in desc or "SE DETECTA" in desc
    bg = (240, 255, 240) if auto else BLANCO
    borde_c = (100, 180, 100) if auto else GRIS_MED
    pdf.set_fill_color(*bg)
    pdf.set_draw_color(*borde_c)
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.set_text_color(*ROSA)
    pdf.cell(8, 7, col, fill=True, border=1, align="C")
    pdf.set_font("Helvetica", "B" if auto else "", 8.5)
    pdf.set_text_color(*VERDE if auto else OSCURO)
    pdf.cell(0, 7, f"  {desc}", fill=True, border=1, ln=True)

pdf.ln(5)

# Resumen hojas
pdf.set_font("Helvetica", "B", 11)
pdf.set_text_color(*ROSA)
pdf.cell(0, 8, "Las 4 hojas de un vistazo", ln=True)
pdf.ln(1)

hojas = [
    (ROSA_CLARO,   "PEDIDOS",   "Registra cada pedido manualmente"),
    (VERDE_CLARO,  "VENTAS",    "Ranking de sabores - se actualiza sola"),
    (AZUL_CLARO,   "CLIENTES",  "Ficha de clientes - se actualiza manualmente"),
    (AMARILLO,     "STOCK",     "Control de cajas y materiales"),
]
for color, nombre, desc in hojas:
    pdf.set_fill_color(*color)
    pdf.set_draw_color(*GRIS_MED)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*OSCURO)
    pdf.cell(32, 8, f"  {nombre}", fill=True, border=1)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.cell(0, 8, f"  {desc}", fill=True, border=1, ln=True)

pdf.ln(6)

# Pie final
pdf.set_fill_color(*ROSA)
pdf.rect(15, pdf.get_y(), 180, 18, "F")
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(*BLANCO)
pdf.set_y(pdf.get_y() + 3)
pdf.cell(0, 6, "TrufaMia - Brigadeiros artesanales", align="C", ln=True)
pdf.set_font("Helvetica", "", 8)
pdf.set_text_color(255, 210, 220)
pdf.cell(0, 6, "TrufaMia.es  |  Contabilidad 2025", align="C", ln=True)


# ═══════════════════════════════════════════════════════════════
# GUARDAR
# ═══════════════════════════════════════════════════════════════
pdf.output(OUTPUT)
print(f"PDF generado: {OUTPUT}")
print(f"Paginas: {pdf.page}")
