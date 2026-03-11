import streamlit as st
from xhtml2pdf import pisa
from io import BytesIO
import qrcode
import base64
import os
from datetime import datetime
import re
import textwrap
import locale


try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8') 
except:
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES')
    except:
        try:
            locale.setlocale(locale.LC_TIME, 'spanish')
        except:
            pass

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="FUT UNSCH PROFESIONAL", page_icon="🎓", layout="wide")

# --- DATA MAESTRA (Cuadros Seleccionables) ---
FACULTADES = ["FACULTAD DE CIENCIAS AGRARIAS", "FACULTAD DE CIENCIAS BIOLÓGICAS", "FACULTAD DE CIENCIAS DE LA EDUCACIÓN", "FACULTAD DE CIENCIAS ECONÓMICAS, ADMINISTRATIVAS Y CONTABLES", "FACULTAD DE CIENCIAS SOCIALES", "FACULTAD DE DERECHO Y CIENCIAS POLÍTICAS", "FACULTAD DE INGENIERÍA DE MINAS, GEOLOGÍA Y CIVIL", "FACULTAD DE INGENIERÍA QUÍMICA Y METALURGIA", "FACULTAD DE CIENCIAS DE LA SALUD"]
ESCUELAS = ["ADMINISTRACIÓN DE EMPRESAS", "AGRONOMÍA", "MATEMÁTICA", "FÍSICA", "ESTADÍSTICA", "CONTABILIDAD Y AUDITORÍA", "ECONOMÍA", "INGENIERÍA AGRÍCOLA", "INGENIERÍA AGROFORESTAL", "INGENIERÍA AGROINDUSTRIAL", "INGENIERÍA CIVIL", "INGENIERÍA DE MINAS", "INGENIERÍA DE SISTEMAS", "INGENIERÍA EN INDUSTRIAS ALIMENTARIAS", "INGENIERÍA QUÍMICA", "ARQUITECTURA", "INGENIERÍA AMBIENTAL", "ANTROPOLOGÍA SOCIAL", "ARQUEOLOGÍA – ARQUEOLOGÍA", "ARQUEOLOGÍA – HISTORIA", "CIENCIAS DE LA COMUNICACIÓN", "DERECHO", "EDUCACIÓN FÍSICA", "EDUCACIÓN INICIAL", "EDUCACIÓN PRIMARIA", "EDUCACIÓN SECUNDARIA", "TRABAJO SOCIAL", "BIOLOGÍA", "ENFERMERÍA", "FARMACIA Y BIOQUÍMICA", "MEDICINA HUMANA", "MEDICINA VETERINARIA", "OBSTETRICIA", "PSICOLOGÍA"]
GRADOS = ["CIENCIAS AGRÍCOLAS", "MEDICINA VETERINARIA", "BIOLOGÍA", "CIENCIAS ADMINISTRATIVAS", "CIENCIAS CONTABLES", "ECONOMÍA", "MATEMÁTICAS", "CIENCIA INGENIERÍA AGRÍCOLA", "CIENCIA INGENIERÍA AGROFORESTAL", "INGENIERÍA AGROINDUSTRIAL", "CIENCIAS DE LA INGENIERÍA CIVIL", "CIENCIAS DE LA INGENIERÍA DE MINAS", "INGENIERÍA DE SISTEMAS", "INGENIERÍA EN INDUSTRIAS ALIMENTARIAS", "INGENIERÍA QUÍMICA", "ARQUITECTURA", "INGENIERÍA AMBIENTAL", "CIENCIA SOCIAL: ANTROPOLOGÍA SOCIAL", "CIENCIA SOCIAL: ARQUEOLOGÍA E HISTORIA", "CIENCIAS DE LA COMUNICACIÓN", "DERECHO", "CIENCIAS DE LA EDUCACION", "CIENCIA SOCIAL: TRABAJO SOCIAL", "CIENCIAS DE LA ENFERMERÍA", "FARMACIA Y BIOQUÍMICA", "MEDICINA HUMANA", "OBSTETRICIA", "PSICOLOGÍA", "EN CIENCIAS BIOLOGICAS"]
PUEBLOS = ["QUECHUA", "AYMARA", "ASHÁNINKA", "AWAJÚN", "SHIPIBO-KONIBO", "AFROPERUANO", "OTRO"]
LENGUAS = ["QUECHUA", "AIMARA", "ASHÁNINKA", "AWAJÚN", "SHIPIBO", "CASTELLANO", "OTRO"]

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return ""

def get_qr_base64(text):
    qr = qrcode.make(text)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"

def insertar_saltos(texto, max_chars=12): # Bajamos a 12 para que entre en los 90px
    if not texto: 
        return ""
    # Esta versión corta la cadena cada N caracteres sin importar qué sean
    return '\n'.join([texto[i:i+max_chars] for i in range(0, len(texto), max_chars)])

# --- GENERADOR HTML ---
def build_html(d):
    def chk(v, t): return f'<span style="color:red; font-weight:bold;">( X )</span>' if v == t else '( &nbsp; )'
    logo_full = get_image_base64("LOGOQ.jpg")
    qr = get_qr_base64(f"UNSCH|{d['dni']}|{d['nombre']}")
    mod_final = f"EXONERADO- {d['i_m']}" if d['i_m'] not in ["ORDINARIO", "ADJUDICADO- CEPRE UNSCH"] else d['i_m']

    return f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{ size: a4; margin: 0.5cm 0.8cm; }}
            body {{ font-family: Helvetica; font-size: 7.5pt; color: #000; line-height: 1.2; }}
            .table {{ width: 100%; border-collapse: collapse; table-layout: fixed; margin-bottom: 2px; }}
            .table td {{ border: 0.5pt solid black; padding: 2px; text-align: center; vertical-align: middle; word-wrap: break-word; overflow-wrap: break-word; hyphens: auto; overflow: hidden;}}
            .bg {{ background-color: #e2efda; font-weight: bold; font-size: 7pt; }}
            .red-text {{ color: #000000; font-weight: bold; text-transform: uppercase; font-size: 9pt; }}
            .nota-pequena {{ font-size: 6pt; text-align: left; margin-bottom: 4px; font-style: italic; }}
            .fundamento {{ text-align: justify; padding: 12px; border: 0.5pt solid black; min-height: 130px; font-size: 10pt; margin-bottom: 5px; }}
            .doc-list {{ text-align: left; padding: 10px; border: 0.5pt solid black; font-size: 7.5pt; line-height: 1.4; min-height: 140px; }}
            .huella-box {{ border: 1pt solid black; height: 2.4cm; width: 1.9cm; margin: 0 auto; }}
            .resolucion-text {{line-height: 1.0; font-size: 6.5pt; font-weight: bold; display: block; white-space: normal; word-wrap: break-word; overflow-wrap: break-word; word-break: break-all; hyphens: auto; max-width: 85px; padding: 2px 4px; text-align: center;}}
        </style>
    </head>
    <body>
        <div style="text-align: left;"><img src="{logo_full}" width="280"></div>
        <div style="text-align: center; font-weight: bold; font-size: 12pt; margin-top: -20px; margin-bottom: 15px;">
            FORMATO ÚNICO DE TRÁMITE<br><span style="font-size: 9pt;">GRADO ACADÉMICO DE BACHILLER</span>
        </div>

        <div style="border: 0.5pt solid black; padding: 6px; text-align: center; font-weight: bold; margin-bottom: 8px;">
            SEÑOR DIRECTOR DE LA ESCUELA PROFESIONAL DE <span class="red-text">{d['esc_dir']}</span>
        </div>

        <table class="table">
            <tr><td class="bg">SOLICITO</td></tr>
            <tr><td class="red-text" style="padding: 8px;">OTORGAMIENTO DE GRADO ACADÉMICO DE BACHILLER EN {d['grado']}</td></tr>
        </table>
        <div class="nota-pequena">*Indicar correctamente la denominación del título profesional y la especialidad cuando corresponda</div>

        <table class="table">
            <tr><td class="bg" width="75%">Apellidos y Nombres (Conforme al DNI)</td><td class="bg" width="25%">DNI</td></tr>
            <tr><td class="red-text" style="height: 18pt;">{d['nombre']}</td><td class="red-text">{d['dni']}</td></tr>
        </table>

        <table class="table" style="margin-top: 5px;">
            <tr><td class="bg" width="15%">Facultad</td><td class="red-text" width="45%" style="text-align: left;">{d['facultad']}</td><td class="bg" colspan="2">Modalidad de Grado de Bachiller</td></tr>
            <tr><td class="bg">Escuela Profesional</td><td class="red-text" style="text-align: left;">{d['escuela']}</td>
                <td width="20%">{chk(d['m_bach'],'Automático')}<br>Automático</td>
                <td width="20%">{chk(d['m_bach'],'Curso de Trabajo de Investigacion')}<br>Curso de Trabajo de Investigacion</td>
            </tr>
        </table>

        <table class="table" style="margin-top: 5px;">
            <tr><td class="bg" rowspan="2" width="10%">Código de Estudiante</td><td class="bg" colspan="3" width="46%">Ingreso</td><td class="bg" colspan="2" width="22%">Primera Matrícula</td><td class="bg" colspan="2" width="22%">Egreso</td></tr>
            <tr style="font-size: 6pt;"><td class="bg">Año</td><td class="bg">Modalidad</td><td class="bg">Resolución</td><td class="bg">Fecha</td><td class="bg">Semestre</td><td class="bg">Fecha</td><td class="bg">Semestre</td></tr>
            <tr class="red-text" style="font-size: 8pt;">
                <td>{d['cod']}</td><td>{d['i_a']}</td>
                <td style="font-size: 6.5pt;" class="resolucion-text">{mod_final}</td>
                <td class="resolucion-text" width="85">{d['i_r']}</td>
                <td>{d['m_f']}</td><td>{d['m_s']}</td>
                <td>{d['e_f']}</td><td>{d['e_s']}</td>
            </tr>
        </table>
        <div class="nota-pequena">* Si la modalidad de ingreso es exonerados detallar el tipo de exoneración</div>

        <table class="table">
            <tr><td class="bg" width="15%">Celular</td><td class="bg" width="50%">Dirección</td><td class="bg" width="35%">Correo Electrónico*</td></tr>
            <tr class="red-text"><td>{d['cel']}</td><td style="font-size: 8pt;">{d['dir']}</td><td style="text-transform: lowercase;">{d['cor']}</td></tr>
        </table>

        <table class="table" style="margin-top: 5px;">
            <tr><td class="bg" colspan="5">Información Étnica: Por sus costumbres y antepasados se siente parte de:(Marque con X)</td><td class="bg" colspan="4">Habla alguna lengua indígena u originaria</td></tr>
            <tr style="height: 55px;">
                <td width="14%">{chk(d['et_c'],'Si')}<br>Si Pertenece a un publo indígena u origianario</td>
                <td width="12%">Especifique:<br><span class="red-text" style="font-size: 7pt;">{d['et_e'] if d['et_c'] in ['Si', 'Afro'] else ''}</span></td>
                <td width="18%">{chk(d['et_c'],'Afro')}<br>Población afroperuana, negra, morena, zamba, mulata, afrodescendiente o parte del pueblo afroperuano</td>
                <td width="8%">{chk(d['et_c'],'No')}<br>No</td>
                <td width="10%">{chk(d['et_c'],'NS')}<br>No Sabe / No Responde</td>
                <td width="8%">{chk(d['le_c'],'Si')}<br>Si</td>
                <td width="15%">Especifique:<br><span class="red-text" style="font-size: 7pt;">{d['le_e'] if d['le_c'] == 'Si' else ''}</span></td>
                <td width="7%">{chk(d['le_c'],'No')}<br>No</td>
                <td width="8%">{chk(d['le_c'],'NS')}<br>No Sabe / No Responde</td>
                
            </tr>
        </table>
        <div class="nota-pequena">* Especificar según los Anexos 1 y 2 adjuntos mediante el Código QR ubicado en la parte inferior.</div>

        <div class="bg" style="border: 0.5pt solid black; border-bottom: none; padding: 4px;">Fundamento de lo solicitado:</div>
        <div class="fundamento">
            <span class="red-text">QUE, HABIENDO CULMINADO MIS ESTUDIOS SUPERIORES SATISFACTORIAMENTE EN LA ESCUELA PROFESIONAL DE {d['esc_dir']}, RECURRO A SU DIGNO DESPACHO, SE SIRVA DISPONER SE ME OTORGUE EL GRADO ACADÉMICO DE BACHILLER EN {d['grado']}, MOTIVO POR EL CUAL ADJUNTO LOS REQUISITOS EXIGIDOS PARA SU ATENCIÓN OPORTUNA.</span>
        </div>

        <div class="bg" style="border: 0.5pt solid black; border-bottom: none; padding: 4px;">Documentos que se adjuntan:</div>
        <div class="doc-list" style="border: 0.5pt solid black; padding: 10px; text-align: left; font-size: 8pt; min-height: 150px;">
            {d['doc_list']}
        </div>

        <div class="nota-pequena" style="font-size: 7pt; font-style: italic; margin-top: 5px;">
            (*) {d['nota_pie']}
        </div>
        <p style="font-weight: bold; margin: 15px 0 5px 0;">POR LO EXPUESTO: A usted, Señor Director, pido acceder a mi solicitud por ser de justicia.</p>
        
<table class="table" style="width: 92%; margin-left: 20%; border-collapse: collapse; margin-top: 15px; table-layout: fixed;">
    <tr>
        <td class="bg" width="35%" style="border: 0.5pt solid black; text-align: center; padding: 5px; background-color: #e8f3e8;">Lugar y Fecha</td>
        <td class="bg" width="40%" style="border: 0.5pt solid black; text-align: center; padding: 5px; background-color: #e8f3e8;">Firma del Solicitante:</td>
        <td class="bg" width="25%" style="border: 0.5pt solid black; text-align: center; padding: 5px; background-color: #e8f3e8;">Huella dactilar</td>
    </tr>
    <tr style="height: 75px;">
        <td style="border: 0.5pt solid black; text-align: center; vertical-align: middle;">
            <div class="red-text" style="font-size: 10pt; font-weight: bold; color: black;">
                {d['lugar']}, {d['fecha']}
            </div>
        </td>
        <td style="border: 0.5pt solid black; text-align: center; vertical-align: bottom; padding-bottom: 5px;">
            <div style="font-size: 8pt; border-top: 0.5pt solid black; width: 80%; margin: 0 auto; margin-bottom: 3px;"></div>
            <div style="font-size: 8pt; font-weight: bold;"></div>
        </td>
        <td style="border: 0.5pt solid black;">
            </td>
    </tr>
</table>

<table style="width: 100%; margin-top: 10px; border: none;">
    <tr>
        <td style="font-size: 7.5pt; text-align: left; border: none; vertical-align: top;">
            * Autorizo la notificación por correo electrónico (TUO de la Ley Nº 27444, Art. 20º)<br>
            * Según Resolución Directoral N.º 0012-2025-SUNEDU-DS-DIRGRATU
        </td>
        <td style="text-align: right; border: none;">
            <img src="{qr}" width="65">
        </td>
    </tr>
</table>
          </body>
    </html>
    """

# --- INTERFAZ STREAMLIT ---
st.title("FUT UNSCH-LLENADO AUTOMATICO V.3")

# Selectores de Cuadro 1, 2 y 4
with st.container():
    c1, c2 = st.columns(2)
    f_esc_dir = c1.selectbox("Cuadro 1: Señor Director de la E.P. de:", ESCUELAS)
    f_gra = c2.selectbox("Cuadro 2: Grado Académico Solicitado:", GRADOS)

# Cuadro 3 y 6
with st.expander("👤 DATOS DEL SOLICITANTE", expanded=True):
    col31, col32 = st.columns([3, 1])
    f_nom = col31.text_input("Apellidos y Nombres (DNI)")
    f_dni = col32.text_input("DNI", max_chars=8)
    
    col61, col62, col63 = st.columns(3)
    f_cel = col61.text_input("Celular")
    f_dir = col62.text_input("Dirección")
    f_cor = col63.text_input("Correo Electrónico")

# Cuadro 4 y 5
with st.expander("🎓 INFORMACIÓN ACADÉMICA"):
    f_fac = st.selectbox("Cuadro 4: Facultad:", FACULTADES)
    f_esc = st.selectbox("Cuadro 4: Escuela Profesional:", ESCUELAS)
    f_mba = st.radio("Modalidad de Grado:", ["Automático", "Curso de Trabajo de Investigacion"], horizontal=True)
    
    st.divider()
    h1, h2, h3, h4 = st.columns([1, 1, 2, 2])
    f_cod = h1.text_input("Código Est.")
    f_ia = h2.text_input("Año Ingreso")
    f_im = h3.selectbox(
    "Modalidad Ingreso",
    [
        "ORDINARIO",
        "TRASLADO",
        "ADJUDICADO - CEPRE UNSCH",
        "PRIMEROS PUESTOS",
        "DEPORTISTA CALIFICADO",
        "PERSONA CON DISCAPACIDAD",
        "CONVENIO INTERNACIONAL"
    ]
)
    f_ir = h4.text_input("Resolución de Ingreso")
    
    f_d1, f_d2, f_d3, f_d4 = st.columns(4)
    v_mf = f_d1.text_input("Fecha 1ra Mat.")
    v_ms = f_d2.text_input("Sem. 1ra Mat.")
    v_ef = f_d3.text_input("Fecha Egreso")
    v_es = f_d4.text_input("Sem. Egreso")

# Cuadro 7
with st.expander("🌍 INFORMACIÓN ÉTNICA"):
    et1, et2 = st.columns(2)
    with et1:
        f_etc = st.radio("Autoidentificación:", ["No", "Si", "Afro", "NS"], horizontal=True)
        f_ete = st.selectbox("Pueblo/Etnia:", PUEBLOS, disabled=(f_etc not in ["Si", "Afro"]))
    with et2:
        f_lec = st.radio("Lengua Originaria:", ["No", "Si", "NS"], horizontal=True)
        f_lee = st.selectbox("Especifique Lengua:", LENGUAS, disabled=(f_lec != "Si"))

        
   
    
   
# --- COLOCA ESTO DONDE ESTABA TU EXPANDER DE DOCUMENTOS ---
with st.expander("📝 DOCUMENTOS ADJUNTOS"):
    st.info("Borra o edita los documentos aquí abajo.")
    
    # Solo definimos los iniciales si el casillero está vacío
    if "mis_docs" not in st.session_state:
        st.session_state["mis_docs"] = (
            "a) Solicitud.\n"
            "b) Recibo de pago por derecho de grado académico de bachiller.\n"
            "c) Copia simple de DNI.\n"
            "d) Dos (02) fotografías pasaporte.\n"
            "e) Copia simple de Certificado de Estudios.\n"
            "f) Declaración jurada de no adeudar a la Facultad, Dirección de Bienestar Universitario y Unidad de Biblioteca.\n"
            "g) Declaración jurada de no tener antecedentes judiciales y penales segun reglamento de Grados y Títulos.\n"
            "h) Otros Segun Reglamento de grados titulos."
        )
    
    # El text_area se conecta directamente al casillero de memoria
    st.text_area("Documentos a incluir:", key="mis_docs", height=250)    
    
# Cuadro 10
f_lug = st.sidebar.text_input("Lugar", value="Ayacucho")
f_fec = st.sidebar.text_input("Fecha", value=datetime.now().strftime("%d de %B de %Y"))
# TRADUCTOR MANUAL (Cópialo tal cual si lo anterior falla)
f_fec = f_fec.replace("January", "enero").replace("February", "febrero").replace("March", "marzo") \
             .replace("April", "abril").replace("May", "mayo").replace("June", "junio") \
             .replace("July", "julio").replace("August", "agosto").replace("September", "septiembre") \
             .replace("October", "octubre").replace("November", "noviembre").replace("December", "diciembre")
if st.button("🚀 GENERAR FUT", use_container_width=True):
    if f_nom and f_dni:
        lista_final_para_pdf = st.session_state["mis_docs"].replace("\n", "<br>")
        data = {
            "esc_dir": f_esc_dir, 
            "grado": f_gra, 
            "nombre": f_nom.upper(),
            "dni": f_dni,
            "facultad": f_fac,
            "escuela": f_esc, 
            "m_bach": f_mba,
            "cod": f_cod,
            "i_a": f_ia,
            "i_m": f_im,
            "i_r": insertar_saltos(f_ir.upper()),
            "m_f": v_mf,
            "m_s": v_ms,
            "e_f": v_ef,
            "e_s": v_es,
            "cel": f_cel,
            "dir": f_dir,
            "cor": f_cor,
            "et_c": f_etc,
            "et_e": f_ete, 
            "le_c": f_lec,
            "le_e": f_lee,
            "lugar": f_lug, 
            "fecha": f_fec,
            "doc_list": lista_final_para_pdf, # Reemplazamos saltos de línea por <br> para HTML
            "nota_pie": "El Certificado de Idiomas, para aquellos que no están en su Currículo de Estudios."
        }
        pdf_out = BytesIO()
        pisa.CreatePDF(BytesIO(build_html(data).encode("UTF-8")), dest=pdf_out)
        st.session_state.pdf_final = pdf_out.getvalue()
        st.success("¡Documento generado con el espaciado correcto!")

if 'pdf_final' in st.session_state:
    st.download_button("📥 DESCARGAR FUT LLENADO", st.session_state.pdf_final, f"FUT_{f_dni}.pdf", "application/pdf", use_container_width=True)