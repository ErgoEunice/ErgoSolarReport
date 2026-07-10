import streamlit as st
from fpdf import FPDF
from datetime import datetime
import io

# --- CONFIGURACIÓN DE LA PÁGINA WEB ---
st.set_page_config(page_title="ErgoSolar Report App", page_icon="☀️", layout="centered")

# Estilos CSS personalizados para simular una app nativa en el celular
st.markdown("""
    <style>
    .main-title { font-size: 26px; font-weight: bold; color: #1A365D; text-align: center; margin-bottom: 5px; }
    .sub-title { font-size: 14px; color: #4A5568; text-align: center; margin-bottom: 25px; }
    div[data-testid="stForm"] { border: none; padding: 0; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">☀️ ERGOSOLAR</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Plataforma Móvil de Reportes de Mantenimiento</div>', unsafe_allow_html=True)

# --- CLASE DEL REPORTE PDF (ID CORPORATIVA DE ERGOSOLAR) ---
class ReporteErgosolar(FPDF):
    def header(self):
        # Franja azul superior de ingeniería
        self.set_fill_color(26, 54, 93) 
        self.rect(0, 0, 210, 32, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", style="B", size=14)
        self.cell(0, 5, "ERGOSOLAR - INGENIERÍA FOTOVOLTAICA", ln=True, align="L")
        self.set_font("Arial", style="I", size=9)
        self.cell(0, 5, "Reporte Oficial de Mantenimiento en Sitio", ln=True, align="L")
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", style="I", size=8)
        self.set_text_color(113, 128, 150)
        self.cell(0, 10, f"ErgoSolar Asset Management - Página {self.page_no()} de {{nb}}", align="L")

# --- INTERFAZ DE USUARIO: TABS PARA EL CELULAR ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 General", 
    "🛠️ Actividades", 
    "⚡ Mediciones CA/CD", 
    "📊 Resultados", 
    "✍️ Cierre"
])

# Inicializar un diccionario para recolectar datos en las diferentes pestañas
if 'datos' not in st.session_state:
    st.session_state.datos = {}

with tab1:
    st.markdown("### 1. Información del Cliente y de la Planta")
    planta = st.text_input("Nombre de la planta / Sitio Solar:", value="Paseo destino Terminal")
    responsable = st.text_input("Responsable / Atendió:", value="Lic. Gabriela")
    direccion = st.text_area("Dirección de la Instalación:", value="Av. Las Torres 1923, Reserva Territorial Atlixcáyotl, Puebla")
    fecha_visita = st.date_input("Fecha del Servicio:", datetime.now())
    
    st.markdown("### 2. Inspección General del Sistema")
    inspeccion_obs = st.text_area("Observaciones de la Inspección Inicial:", 
                                  value="Durante la inspección se observó contaminación normal en los paneles principalmente por polvo.")
    foto_antes_1 = st.camera_input("Foto 1: Paneles antes de la limpieza (Cámara)")

with tab2:
    st.markdown("### 3. Registro de Actividades Realizadas")
    act_limpieza = st.text_area("3.1. Limpieza de Módulos:", value="Limpieza con agua y herramienta adecuada para garantizar el buen rendimiento de los módulos.")
    foto_despues_1 = st.camera_input("Foto 2: Paneles después de la limpieza (Cámara)")
    
    act_torque = st.text_area("3.2. Reapriete de sujeciones y estructura:", value="Se verificó el torque de las fijaciones de módulos y estructura metálica.")
    act_mc4 = st.text_area("3.3. Inspección de Conectores MC4:", value="Revisión de conectores para verificar posibles fallas, desgaste o desconexiones.")
    act_tierra = st.text_area("3.4. Conexiones a Tierra Física:", value="Verificación del estado de las conexiones a tierra y sus continuidades.")
    act_protecciones = st.text_area("3.5. Revisión de Protecciones y Tableros:", 
                                     value="Verificación de funcionamiento y estado de los dispositivos de protección. Durante la revisión se detecta calentamiento en portafusibles, se realiza reemplazo de todos los portafusibles y fusibles.")
    foto_tablero = st.camera_input("Foto 3: Evidencia de trabajos en tableros/inversores")

with tab3:
    st.markdown("### 4. Mediciones Eléctricas en Circuitos")
    st.markdown("**Circuitos de Corriente Alterna (CA)**")
    v_ca_min = st.text_input("Voltaje Mínimo registrado en CA (V):", value="221.0")
    v_ca_max = st.text_input("Voltaje Máximo registrado en CA (V):", value="222.6")
    desbalance = st.text_input("Porcentaje de desbalance calculado (%):", value="0.2%")
    
    st.markdown("**Circuitos de Corriente Directa (CD)**")
    v_cd_cadenas = st.text_input("Voltaje de circuito abierto por cadena (V):", value="796V - 798V")
    v_fallo_tierra = st.text_input("Voltaje de fallo a tierra registrado (V):", value="> 40V")

with tab4:
    st.markdown("### 5. Tabla de Criterios y Conclusiones")
    st.info("Configura los veredictos que se imprimirán en la matriz formal del reporte.")
    
    concl_ca = st.selectbox("Conclusión de Voltaje CA:", ["Excelente", "Aceptable", "Fuera de Rango"], index=0)
    concl_cd = st.selectbox("Conclusión de Cadenas CD:", ["Estables / Correcto", "Falla detectada"], index=0)
    concl_aisl = st.selectbox("Conclusión de Aislamiento:", ["Aislamiento correcto; sin falla activa", "Bajo aislamiento"], index=0)

with tab5:
    st.markdown("### 6. Conclusión Final del Servicio")
    conclusion_final = st.text_area("Dictamen General:", value="El sistema fotovoltaico opera en condiciones óptimas tras el mantenimiento correctivo de portafusibles y la limpieza general de módulos.")
    firma_nombre = st.text_input("Nombre de quien dictamina:", value="Hugo Malpica")
    firma_puesto = st.text_input("Puesto / Cargo:", value="Subgerente de Asset Management")
    
    st.markdown("---")
    # BOTÓN PRINCIPAL DE GENERACIÓN
    generar_pdf = st.button("🚀 COMPILAR Y GENERAR REPORTE OFICIAL PDF", use_container_width=True)

# --- PROCESO DE GENERACIÓN Y DESCARGA DEL PDF ---
if generar_pdf:
    with st.spinner("Estructurando PDF bajo normas ErgoSolar..."):
        pdf = ReporteErgosolar()
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.ln(12) # Margen inicial después del header fixed
        
        # --- SECCIÓN 1: DATOS GENERALES ---
        pdf.set_font("Arial", style="B", size=11)
        pdf.set_text_color(26, 54, 93)
        pdf.cell(0, 8, "1. INFORMACIÓN DEL CLIENTE Y DE LA PLANTA", ln=True)
        pdf.set_draw_color(26, 54, 93)
        pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
        pdf.ln(3)
        
        pdf.set_font("Arial", size=10)
        pdf.set_text_color(45, 55, 72)
        pdf.set_fill_color(247, 250, 252)
        
        pdf.cell(45, 7, "Nombre de la planta:", border=1, fill=True)
        pdf.cell(145, 7, f" {planta}", border=1, ln=True)
        pdf.cell(45, 7, "Responsable:", border=1)
        pdf.cell(145, 7, f" {responsable}", border=1, ln=True)
        pdf.cell(45, 7, "Fecha del Servicio:", border=1, fill=True)
        pdf.cell(145, 7, f" {fecha_visita.strftime('%d de %B de %Y')}", border=1, ln=True)
        
        pdf.cell(45, 10, "Dirección Sitio:", border=1)
        pdf.multi_cell(145, 5, f" {direccion}", border=1)
        pdf.ln(5)
        
        # --- SECCIÓN 2: INSPECCIÓN VISUAL ---
        pdf.set_font("Arial", style="B", size=11)
        pdf.set_text_color(26, 54, 93)
        pdf.cell(0, 8, "2. INSPECCIÓN GENERAL DEL SISTEMA", ln=True)
        pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
        pdf.ln(3)
        
        pdf.set_font("Arial", size=10)
        pdf.set_text_color(45, 55, 72)
        pdf.multi_cell(190, 5, f"Observaciones iniciales: {inspeccion_obs}")
        pdf.ln(3)
        
        # Inyección dinámica de foto "Antes"
        if foto_antes_1:
            img_bytes = io.BytesIO(foto_antes_1.getvalue())
            with open("temp_antes.jpg", "wb") as f:
                f.write(img_bytes.getbuffer())
            try:
                pdf.image("temp_antes.jpg", w=85)
                pdf.set_font("Arial", style="I", size=8)
                pdf.cell(0, 5, "Ilustración: Estado de paneles solares previo al mantenimiento.", ln=True)
                pdf.ln(4)
            except:
                pass

        # --- SECCIÓN 3: ACTIVIDADES ---
        pdf.set_font("Arial", style="B", size=11)
        pdf.set_text_color(26, 54, 93)
        pdf.cell(0, 8, "3. ACTIVIDADES TÉCNICAS REALIZADAS", ln=True)
        pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
        pdf.ln(3)
        
        pdf.set_font("Arial", size=10)
        pdf.set_text_color(45, 55, 72)
        
        pdf.set_font("Arial", style="B", size=10)
        pdf.cell(0, 5, "3.1. Limpieza de Módulos Fotovoltaicos", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(190, 5, act_limpieza)
        
        if foto_despues_1:
            img_bytes2 = io.BytesIO(foto_despues_1.getvalue())
            with open("temp_despues.jpg", "wb") as f:
                f.write(img_bytes2.getbuffer())
            try:
                pdf.ln(2)
                pdf.image("temp_despues.jpg", w=85)
                pdf.set_font("Arial", style="I", size=8)
                pdf.cell(0, 5, "Ilustración: Estado de paneles posterior a las tareas de limpieza.", ln=True)
            except:
                pass
                
        pdf.ln(4)
        pdf.set_font("Arial", style="B", size=10)
        pdf.cell(0, 5, "3.2. Reapriete de Estructura y Conectores", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(190, 5, f"- Estructuras: {act_torque}\n- Conectores MC4: {act_mc4}\n- Tierras: {act_tierra}")
        
        pdf.ln(4)
        pdf.set_font("Arial", style="B", size=10)
        pdf.cell(0, 5, "3.3. Protecciones y Componentes de Inversores", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(190, 5, act_protecciones)
        
        if foto_tablero:
            img_bytes3 = io.BytesIO(foto_tablero.getvalue())
            with open("temp_tablero.jpg", "wb") as f:
                f.write(img_bytes3.getbuffer())
            try:
                pdf.ln(2)
                pdf.image("temp_tablero.jpg", w=75)
                pdf.set_font("Arial", style="I", size=8)
                pdf.cell(0, 5, "Ilustración: Evidencia técnica de revisión y torqueado en tableros.", ln=True)
            except:
                pass

        # --- SECCIÓN 4: MATRIZ DE MEDICIONES Y RESULTADOS ---
        pdf.add_page() # Forzamos cambio de hoja para que la tabla quede unificada
        pdf.ln(12)
        pdf.set_font("Arial", style="B", size=11)
        pdf.set_text_color(26, 54, 93)
        pdf.cell(0, 8, "4. CUADRO RESUMEN DE MEDICIONES Y CONCLUSIONES", ln=True)
        pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
        pdf.ln(4)
        
        # Tabla estilizada
        pdf.set_font("Arial", style="B", size=9)
        pdf.set_fill_color(43, 108, 176)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(55, 8, " Parámetro / Medición", border=1, fill=True)
        pdf.cell(45, 8, " Valor Registrado", border=1, fill=True)
        pdf.cell(45, 8, " Criterio de Norma", border=1, fill=True)
        pdf.cell(45, 8, " Conclusión", border=1, fill=True, ln=True)
        
        pdf.set_font("Arial", size=9)
        pdf.set_text_color(45, 55, 72)
        
        pdf.cell(55, 8, " Voltaje Circuito Alterna (CA)", border=1)
        pdf.cell(45, 8, f" Min:{v_ca_min}V / Max:{v_ca_max}V", border=1)
        pdf.cell(45, 8, f" Desbalance {desbalance}", border=1)
        pdf.cell(45, 8, f" {concl_ca}", border=1, ln=True)
        
        pdf.cell(55, 8, " Voltaje Abierto por Cadena", border=1)
        pdf.cell(45, 8, f" {v_cd_cadenas}", border=1)
        pdf.cell(45, 8, " Estabilidad VCD", border=1)
        pdf.cell(45, 8, f" {concl_cd}", border=1, ln=True)
        
        pdf.cell(55, 8, " Voltaje de Fallo a Tierra", border=1)
        pdf.cell(45, 8, f" {v_fallo_tierra}", border=1)
        pdf.cell(45, 8, " < 5% o > 40V Aisl.", border=1)
        pdf.cell(45, 8, f" {concl_aisl}", border=1, ln=True)
        pdf.ln(6)
        
        # --- SECCIÓN 5: CONCLUSIÓN Y FIRMAS ---
        pdf.set_font("Arial", style="B", size=11)
        pdf.set_text_color(26, 54, 93)
        pdf.cell(0, 8, "5. CONCLUSIÓN Y DICTAMEN FINAL", ln=True)
        pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
        pdf.ln(3)
        
        pdf.set_font("Arial", size=10)
        pdf.set_text_color(45, 55, 72)
        pdf.multi_cell(190, 5, conclusion_final)
        pdf.ln(15)
        
        # Bloque de firma formal
        pdf.set_font("Arial", style="B", size=10)
        pdf.cell(0, 5, f"{firma_nombre}", ln=True, align="C")
        pdf.set_font("Arial", size=9)
        pdf.cell(0, 5, f"{firma_puesto}", ln=True, align="C")
        pdf.cell(0, 5, "ErgoSolar Asset Management Division", ln=True, align="C")

        # fpdf2 ya genera los bytes por defecto al no ponerle nombre de archivo
        pdf_output = bytes(pdf.output())
        
        st.success("✅ ¡El Reporte ha sido estructurado y procesado de forma exitosa!")
        st.download_button(
            label="⬇️ Descargar Reporte PDF de ErgoSolar",
            data=pdf_output,
            file_name=f"Reporte_Mantenimiento_{planta.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )