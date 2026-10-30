import io
import os
from datetime import date

import openpyxl
import streamlit as st

# ---------------------------------------------------------------------------
# Paleta corporativa Ergo Solar
# ---------------------------------------------------------------------------
NARANJA = "#ff5e00"
NARANJA_CLARO = "#ffae7f"
AZUL = "#001489"
GRIS_OSCURO = "#686666"
GRIS_CLARO = "#e0e0e0"

TEMPLATE_PATH = os.path.join("template", "Levantamiento_ErgoSolar_Template.xlsx")
LOGO_PATH = os.path.join("assets", "Ergologo.png")

st.set_page_config(
    page_title="Levantamiento Comercial Etapa 1",
    page_icon="Ergogo.png",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Estilos (CSS) con la identidad corporativa
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: #e0e0e0;
        }}
        h1, h2, h3 {{
            color: {AZUL};
        }}
        .bloque-seccion {{
            background-color: {AZUL};
            color: white;
            padding: 10px 16px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 1.05rem;
            margin-top: 1.6rem;
            margin-bottom: 0.8rem;
        }}
        .nota-instruccion {{
            background-color: {NARANJA_CLARO};
            color: {AZUL};
            padding: 10px 14px;
            border-radius: 6px;
            font-style: italic;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }}
        div.stButton > button, div.stFormSubmitButton > button {{
            background-color: {NARANJA};
            color: white;
            font-weight: 700;
            border: none;
            border-radius: 6px;
        }}
        div.stButton > button:hover, div.stFormSubmitButton > button:hover {{
            background-color: {AZUL};
            color: white;
        }}
        div[data-testid="stDownloadButton"] button {{
            background-color: {AZUL};
            color: white;
            font-weight: 700;
            border-radius: 6px;
            border: none;
        }}
        section[data-testid="stSidebar"] {{
            background-color: {GRIS_CLARO};
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(SCRIPT_DIR, "Ergologo.png")

col_logo, col_vacia = st.columns([2, 3])
with col_logo:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, use_container_width=True)

st.title("LEVANTAMIENTO COMERCIAL - ETAPA 1")
st.caption("Ergo Solar · Entrevista y perfil del cliente potencial")

st.markdown(
    '<div class="nota-instruccion">El levantamiento se debe realizar cuando '
    'se tenga la firma de la solicitud de factibilidad o el visto bueno del '
    'área gerencial. Completa cada sección con la información recabada '
    'durante la visita.</div>',
    unsafe_allow_html=True,
)

RATING_HELP = "5 = muy importante · 1 = menos importante"
CANALES_CONTACTO = [
    "Referido", "Redes sociales", "Página web / Google",
    "Llamada en frío", "Evento / Feria", "Otro",
]

# ---------------------------------------------------------------------------
# Formulario
# ---------------------------------------------------------------------------
with st.form("levantamiento_form", clear_on_submit=False):

    # -- Datos para nombrar el archivo (no se escriben en ninguna celda) --
    c1, c2 = st.columns(2)
    with c1:
        fecha_visita = st.date_input("Fecha de la visita", value=date.today())
    with c2:
        nombre_asesor = st.text_input("Nombre del asesor / líder booster")

    # ---------------- Entrevista con el cliente ----------------
    st.markdown('<div class="bloque-seccion">ENTREVISTA CON EL CLIENTE</div>', unsafe_allow_html=True)
    nombre_cliente = st.text_input("Nombre del cliente *")
    colA, colB = st.columns(2)
    with colA:
        contacto_medio = st.selectbox("¿Cómo nos contactó?", CANALES_CONTACTO)
        contacto_otro = ""
        if contacto_medio == "Otro":
            contacto_otro = st.text_input("Especifica el medio de contacto")
    with colB:
        nivel_influencia = st.select_slider(
            "Nivel de influencia sobre la decisión de compra *",
            options=["Baja", "Media", "Alta"], value="Media",
        )

    # ---------------- Investigación sobre el perfil del cliente ----------------
    st.markdown('<div class="bloque-seccion">INVESTIGACIÓN SOBRE EL PERFIL DEL CLIENTE</div>', unsafe_allow_html=True)
    pasiones = st.text_area("¿Qué le apasiona al cliente? *")
    miedos = st.text_area("¿Qué no le gusta, le preocupa o cuáles son los miedos de la implementación del proyecto?")
    valora_proveedores = st.text_area(
        "¿Qué es lo que más valora de sus proveedores favoritos y cuál cree que es "
        "el factor que más influye en esa buena comunicación? *"
    )
    hobbies = st.text_input("Gustos y Hobbies")
    descripcion_visual = st.text_area("Descripción visual (¿Cómo viste?, lenguaje, decoración de la oficina, etc.)")
    afiliacion = st.text_input("Afiliación a cámara / asociación / comunidad")
    fobia_pagos = st.text_input("Fobia / opinión respecto de realizar pagos diferidos")
    experiencia_previa = st.text_area("Experiencia anterior respecto de sistemas fotovoltaicos o baterías")
    expectativa_compra = st.text_area("Expectativa en la compra de sistema fotovoltaico o BESS")
    tipo_contrato = st.text_input("Tipo de contrato (PPA, financiamiento, inversión directa, otro) y plazo *")
    interes_poliza = st.selectbox(
        "¿Al cliente le interesa adquirir póliza de mantenimiento con nosotros en caso de CAPEX?",
        ["Sí", "No", "Tal vez / no definido"],
    )
    tarifa_horaria = st.text_area(
        "Tarifa horaria, suministrador, posibles descuentos, penalización por bajo "
        "consumo y si la facturación es cinco-minutal"
    )
    kwh_verdes = st.text_input("¿El cliente busca cumplir objetivos de energía específicos (kWh verdes)?")
    ideas_regalo = st.text_input("Ideas para un futuro regalo espectacular")

    # ---------------- Condiciones actuales y planes a futuro ----------------
    st.markdown('<div class="bloque-seccion">CONDICIONES ACTUALES Y PLANES A FUTURO</div>', unsafe_allow_html=True)
    st.caption(
        "Estas preguntas te las puede contestar el dueño o el encargado de "
        "mantenimiento; procura que sea el dueño quien las responda."
    )

    def campo_si_no_detalle(pregunta, texto_detalle, key):
        resp = st.radio(pregunta, ["No", "Sí"], horizontal=True, key=f"{key}_radio")
        detalle = ""
        if resp == "Sí":
            detalle = st.text_input(texto_detalle, key=f"{key}_detalle")
        return f"Sí – {detalle}" if resp == "Sí" and detalle else resp

    remodelacion = campo_si_no_detalle(
        "¿Se realizará próximamente una remodelación?", "¿Cuál?", "remodelacion")
    anos_renta = st.text_input(
        "Si el cliente renta el inmueble: ¿cuántos años tiene firmado su contrato de arrendamiento?"
    )
    incremento_carga = campo_si_no_detalle(
        "¿Se tiene planeado un incremento, reducción o modificación de la carga? *",
        "¿De cuánto?", "incremento_carga")
    adecuacion_electrica = campo_si_no_detalle(
        "¿El cliente tiene que realizar alguna adecuación en su instalación eléctrica "
        "acorde a normativa para la interconexión? *",
        "Especifica cuál", "adecuacion_electrica")
    garantias_afectadas = campo_si_no_detalle(
        "¿El cliente cuenta con garantías que se puedan ver afectadas por nuestro "
        "trabajo (impermeabilizante, trabajos eléctricos, equipos, pintado, etc.)?",
        "Especifica cuál", "garantias_afectadas")
    aseguradora = campo_si_no_detalle(
        "¿El cliente cuenta con alguna aseguradora?", "Especifica cuál", "aseguradora")
    anos_instalacion = st.text_input("¿Cuántos años tiene la instalación eléctrica?")
    ver_modulos = campo_si_no_detalle(
        "¿El cliente quiere que se vean los módulos?", "¿Por qué?", "ver_modulos")

    st.markdown(f"**¿Qué tan importante es para el cliente los siguientes aspectos?** _{RATING_HELP}_")
    rc1, rc2 = st.columns(2)
    with rc1:
        r_servicio = st.slider("Servicio", 1, 5, 3)
        r_precio = st.slider("Precio", 1, 5, 3)
        r_tiempo = st.slider("Tiempo", 1, 5, 3)
        r_garantias = st.slider("Garantías", 1, 5, 3)
        r_calidad = st.slider("Calidad", 1, 5, 3)
        r_estetica = st.slider("Estética", 1, 5, 3)
    with rc2:
        r_pago = st.slider("Formas de pago", 1, 5, 3)
        r_rentabilidad = st.slider("Rentabilidad / Ahorros", 1, 5, 3)
        r_fiscal = st.slider("Beneficio fiscal", 1, 5, 3)
        r_ambiente = st.slider("Beneficio medio ambiente", 1, 5, 3)
        r_recomendacion = st.slider("Recomendación de amigo", 1, 5, 3)
        r_respaldo = st.slider("Respaldo de proveedor", 1, 5, 3)

    st.markdown("**Si te comparten los siguientes documentos, ¿el cliente los tiene?**")
    dc1, dc2 = st.columns(2)
    with dc1:
        doc_plano_electrico = st.checkbox("Plano eléctrico / diagramas unifilares")
        doc_plano_estructural = st.checkbox("Plano estructural")
    with dc2:
        doc_layout = st.checkbox("Lay Out")
        doc_planos_construccion = st.checkbox("Planos de construcción")
    doc_dictamen_dro = st.checkbox("Dictamen estructural u opinión de DRO")

    otro_aspecto = st.text_input("¿Qué otro aspecto importante considera el cliente? Anótalo")

    # ---------------- Documentación necesaria para la prefactibilidad ----------------
    st.markdown('<div class="bloque-seccion">DOCUMENTACIÓN NECESARIA PARA LA PREFACTIBILIDAD</div>', unsafe_allow_html=True)
    st.caption("Comenta con el cliente si cuenta con la siguiente documentación:")
    doc_cfe = st.checkbox("Último recibo de CFE *")
    doc_id = st.checkbox("Copia digitalizada de identificación oficial del representante legal o titular del servicio")
    doc_fiscal = st.checkbox("Constancia de situación fiscal (menor a 30 días)")
    doc_acta = st.checkbox("Acta constitutiva (persona moral)")
    doc_poder = st.checkbox("Poder notarial (persona moral)")
    doc_contacto = st.checkbox("Datos de contacto (correo y teléfono) *")
    doc_dro = st.checkbox("¿Cuentan con la opinión estructural o análisis de un DRO?")

    st.caption("Solo si se propone un proyecto tipo CARPORT:")
    doc_planos_gas = st.checkbox("Planos de instalación de gas o eléctrico subterráneo")
    doc_licencia_suelo = st.checkbox("Licencia de uso de suelo (actualizada)")

    # ---------------- Fotografías ----------------
    st.markdown('<div class="bloque-seccion">FOTOGRAFÍAS DE RESPALDO</div>', unsafe_allow_html=True)
    st.caption(
        "Después de realizar estas preguntas, y de no tener herramientas para "
        "realizar mediciones o drone, toma las siguientes fotos:"
    )
    fc1, fc2 = st.columns(2)
    with fc1:
        foto_fachada = st.checkbox("Foto de la fachada del inmueble", value=True)
        foto_panoramica = st.checkbox("Panorámica de la acometida", value=True)
        foto_cortacircuitos = st.checkbox("Cortacircuitos", value=True)
        foto_nicho = st.checkbox("Nicho de medición", value=True)
    with fc2:
        foto_accesos = st.checkbox("Accesos del inmueble", value=True)
        foto_lamina = st.checkbox("Foto de lámina (al menos desde abajo)", value=True)
        foto_techumbre = st.checkbox("Foto de acceso a techumbre", value=True)
        foto_almacenamiento = st.checkbox("Foto para almacenamiento", value=True)

    firma_factibilidad = st.checkbox("Se buscó la firma de la solicitud de factibilidad *")

    # ---------------- Cierre ----------------
    st.markdown('<div class="bloque-seccion">CIERRE</div>', unsafe_allow_html=True)
    link_drive = st.text_input('Anexar el link de carpeta en drive "Guerreros": *')

    enviado = st.form_submit_button("Generar archivo Excel")

# ---------------------------------------------------------------------------
# Al enviar: abrir la plantilla, escribir cada respuesta y ofrecer descarga
# ---------------------------------------------------------------------------
if enviado:
    campos_obligatorios = {
        "Nombre del cliente": nombre_cliente,
        "Link de carpeta en drive": link_drive,
    }
    faltantes = [nombre for nombre, valor in campos_obligatorios.items() if not valor]

    if faltantes:
        st.error("Falta completar campos obligatorios: " + ", ".join(faltantes))
    else:
        wb = openpyxl.load_workbook(TEMPLATE_PATH)
        ws = wb["Hoja1"]

        contacto_final = contacto_otro if (contacto_medio == "Otro" and contacto_otro) else contacto_medio

        valores = {
            "C6": nombre_cliente,
            "I6": contacto_final,
            "E7": nivel_influencia,

            "D9": pasiones,
            "A11": miedos,
            "A13": valora_proveedores,
            "C14": hobbies,
            "A16": descripcion_visual,
            "E17": afiliacion,
            "E18": fobia_pagos,
            "A20": experiencia_previa,
            "A22": expectativa_compra,
            "G23": tipo_contrato,
            "H24": interes_poliza,
            "A26": tarifa_horaria,
            "D27": kwh_verdes,
            "D28": ideas_regalo,

            "G31": remodelacion,
            "I32": anos_renta,
            "I33": incremento_carga,
            "J34": adecuacion_electrica,
            "C37": garantias_afectadas,
            "G38": aseguradora,
            "D39": anos_instalacion,
            "J39": ver_modulos,

            "B41": r_servicio, "D41": r_pago,
            "B42": r_precio, "D42": r_rentabilidad,
            "B43": r_tiempo, "D43": r_fiscal,
            "B44": r_garantias, "D44": r_ambiente,
            "B45": r_calidad, "D45": r_recomendacion,
            "B46": r_estetica, "D46": r_respaldo,
            "J42": "Sí" if doc_plano_electrico else "No",
            "J43": "Sí" if doc_plano_estructural else "No",
            "J44": "Sí" if doc_layout else "No",
            "J45": "Sí" if doc_planos_construccion else "No",
            "J46": "Sí" if doc_dictamen_dro else "No",
            "E47": otro_aspecto,

            "G50": "Sí" if doc_cfe else "No",
            "G51": "Sí" if doc_id else "No",
            "G52": "Sí" if doc_fiscal else "No",
            "G53": "Sí" if doc_acta else "No",
            "G54": "Sí" if doc_poder else "No",
            "G55": "Sí" if doc_contacto else "No",
            "G56": "Sí" if doc_dro else "No",
            "J51": "Sí" if doc_planos_gas else "No",
            "J53": "Sí" if doc_licencia_suelo else "No",

            "D58": "✔" if foto_fachada else "",
            "H58": "✔" if foto_accesos else "",
            "D59": "✔" if foto_panoramica else "",
            "H59": "✔" if foto_lamina else "",
            "D60": "✔" if foto_cortacircuitos else "",
            "H60": "✔" if foto_techumbre else "",
            "D61": "✔" if foto_nicho else "",
            "H61": "✔" if foto_almacenamiento else "",

            "A65": link_drive,
        }

        for celda, valor in valores.items():
            ws[celda] = valor

        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        nombre_archivo = f"Levantamiento_Etapa1_{nombre_cliente.strip().replace(' ', '_')}_{fecha_visita.isoformat()}.xlsx"

        st.success("¡Listo! El archivo se generó con la misma organización y formato del original.")
        st.download_button(
            label="⬇️ Descargar Excel",
            data=buffer,
            file_name=nombre_archivo,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
