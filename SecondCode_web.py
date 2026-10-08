import streamlit as st
import pandas as pd
import io

# Configuración de la página
st.set_page_config(
    page_title="Levantamiento Etapa 2 - ERGOSOLAR",
    page_icon="Ergogo.png",
    layout="wide"
)

st.title("Levantamiento Preventa - Etapa 2")
st.write("Captura los datos del levantamiento preventa en campo y exporta la información en formato Excel.")

# Pestañas para organizar la captura de datos
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Fotografías",
    "2. Techumbre, Estructural y Obstáculos",
    "3. Levantamiento Eléctrico",
    "4. Evaluación y Descarga"
])

# ---------------------------------------------------------
# PESTAÑA 1: FOTOGRAFÍAS 
# ---------------------------------------------------------
with tab1:
    st.header("Checklist de Fotografías")
    st.info("Marca las vistas que hayan sido capturadas correctamente en sitio (mínimo 3 fotos por vista).")

    col1, col2 = st.columns(2)
    with col1:
        drone_techumbre = st.checkbox("Techumbre", value=True)
        drone_aguila = st.checkbox("Vistas aéreas (Vista de águila)", value=True)
        drone_frontales = st.checkbox("Vistas frontales", value=True)
        drone_laterales = st.checkbox("Vistas laterales", value=True)
        drone_traseras = st.checkbox("Vistas traseras", value=True)

    with col2:
        drone_lamina = st.checkbox("Fotos de la lámina (Identificación de tipo y medidas)", value=True)
        drone_obstaculos = st.checkbox("Fotos de obstáculos", value=True)
        drone_video = st.checkbox("Video de drone (Recorrido de techo)", value=False)
        drone_terreno = st.checkbox("Terreno y periferia de la propiedad", value=True)

# ---------------------------------------------------------
# PESTAÑA 2: TECHUMBRE, ESTRUCTURAL Y OBSTÁCULOS
# ---------------------------------------------------------
with tab2:
    st.header("Levantamiento en Techumbre")
    
    col1, col2 = st.columns(2)
    with col1:
        facil_acceso = st.radio("¿Existe un acceso a techumbre de fácil acceso?", ["Si", "No"], index=0)
        obs_acceso = st.text_input("Observaciones de acceso")

        equipo_adic = st.radio("¿Para acceso a techumbre se requiere equipo adicional? (Escalera, arnés, anclaje móvil, etc.)?", ["No", "Si"], index=0)
        obs_equipo = st.text_input("Observaciones equipo adicional")

        lineas_energ = st.radio("¿Existen líneas energizadas en el área a instalar?", ["No", "Si"], index=0)
        obs_lineas = st.text_input("Observaciones líneas energizadas")

        esc_marina = st.radio("Escalera marina", ["Si", "No"], index=0)
        obs_esc = st.text_input("Observaciones Escalera Marina", value="Está de fácil acceso")

    with col2:
        estado_techo = st.radio("¿El estado físico del techo losa o terreno es buena?", ["Si", "No"], index=0)
        obs_estado = st.text_input("Observaciones estado del techo")

        pasos_gato = st.radio("¿Existen pasos de gato*?", ["No", "Si"], index=0)
        obs_pasos = st.text_input("Observaciones pasos de gato")

        lineas_vida = st.radio("¿Existen líneas de vida*?", ["No", "Si"], index=0)
        obs_vida = st.text_input("Observaciones líneas de vida")

        toma_agua = st.radio("Toma de agua cercana", ["Si", "No"], index=0)
        obs_agua = st.text_input("Observaciones Toma de Agua", value="Se requiere obra hidráulica")

        pararrayos = st.radio("Sistema de pararrayos", ["Si", "No"], index=0)
        obs_pararrayos = st.text_input("Observaciones Pararrayos", value="Medidas en retensores")

    st.markdown("---")
    st.header("Levantamiento Estructural")
    
    cant_naves = st.number_input("¿Cuántas naves hay?", min_value=1, max_value=10, value=1, step=1)
    
    naves_estructural_data = {}
    
    for i in range(1, int(cant_naves) + 1):
        with st.expander(f"Detalles de Nave {i}", expanded=(i == 1)):
            st.subheader(f"Nave {i}")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                num_aguas = st.number_input(f"Número de aguas - Nave {i}", value=1, step=1, key=f"aguas_{i}")
                ancho = st.number_input(f"Ancho (m) - Nave {i}", value=33.60, key=f"ancho_{i}")
                largo = st.number_input(f"Largo (m) - Nave {i}", value=46.20, key=f"largo_{i}")
            with c2:
                altura_mayor = st.number_input(f"Altura mayor (m) - Nave {i}", value=10.70, key=f"alt_may_{i}")
                altura_menor = st.number_input(f"Altura menor (m) - Nave {i}", value=8.66, key=f"alt_men_{i}")
            with c3:
                orientacion = st.text_input(f"Orientación - Nave {i}", value="Este-Oeste", key=f"orient_{i}")
                inclinacion = st.number_input(f"Inclinación (°) - Nave {i}", value=2.40, key=f"inc_{i}")

            st.markdown("#### Lámina")
            l_col1, l_col2, l_col3, l_col4, l_col5 = st.columns(5)
            with l_col1:
                tipo_lamina = st.text_input(f"Tipo Lámina - Nave {i}", value="Engargolada", key=f"t_lam_{i}")
            with l_col2:
                ancho_lamina = st.number_input(f"Ancho Lámina - Nave {i}", value=1.0, key=f"a_lam_{i}")
            with l_col3:
                alto_lamina = st.number_input(f"Alto Lámina - Nave {i}", value=0.05, key=f"h_lam_{i}")
            with l_col4:
                largo_lamina = st.number_input(f"Largo Lámina - Nave {i}", value=12.0, key=f"l_lam_{i}")
            with l_col5:
                calibre_lamina = st.text_input(f"Calibre Lámina - Nave {i}", value="Cal 24", key=f"c_lam_{i}")

            l_col6, l_col7, l_col8 = st.columns(3)
            with l_col6:
                dist_cresta = st.number_input(f"Distancia entre crestas - Nave {i}", value=0.4, key=f"d_cresta_{i}")
            with l_col7:
                alt_cresta = st.number_input(f"Altura de cresta - Nave {i}", value=0.05, key=f"h_cresta_{i}")
            with l_col8:
                ancho_cresta = st.number_input(f"Ancho de cresta - Nave {i}", value=0.1, key=f"w_cresta_{i}")

            st.markdown("#### Montén")
            m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
            with m_col1:
                tipo_monten = st.text_input(f"Tipo Montén - Nave {i}", value="Canal U", key=f"t_mon_{i}")
            with m_col2:
                ancho_monten = st.number_input(f"Ancho Montén - Nave {i}", value=0.15, key=f"a_mon_{i}")
            with m_col3:
                alto_monten = st.number_input(f"Alto Montén - Nave {i}", value=0.05, key=f"h_mon_{i}")
            with m_col4:
                largo_monten = st.number_input(f"Largo Montén - Nave {i}", value=6.0, key=f"l_mon_{i}")
            with m_col5:
                calibre_monten = st.text_input(f"Calibre Montén - Nave {i}", value="Cal 14", key=f"c_mon_{i}")

            m_col6, m_col7 = st.columns(2)
            with m_col6:
                dist_montenes = st.number_input(f"Distancia entre montenes - Nave {i}", value=1.5, key=f"d_mon_{i}")
            with m_col7:
                num_montenes = st.number_input(f"Número de montenes - Nave {i}", value=10, step=1, key=f"n_mon_{i}")

            st.markdown("#### Viga")
            v_col1, v_col2, v_col3, v_col4, v_col5 = st.columns(5)
            with v_col1:
                tipo_viga = st.text_input(f"Tipo Viga - Nave {i}", value="IPN", key=f"t_vig_{i}")
            with v_col2:
                ancho_viga = st.number_input(f"Ancho Viga - Nave {i}", value=0.2, key=f"a_vig_{i}")
            with v_col3:
                alto_viga = st.number_input(f"Alto Viga - Nave {i}", value=0.3, key=f"h_vig_{i}")
            with v_col4:
                largo_viga = st.number_input(f"Largo Viga - Nave {i}", value=15.0, key=f"l_vig_{i}")
            with v_col5:
                calibre_viga = st.text_input(f"Calibre/Espesor Viga - Nave {i}", value="3/8\"", key=f"c_vig_{i}")

            v_col6, v_col7 = st.columns(2)
            with v_col6:
                dist_vigas = st.number_input(f"Distancia entre vigas - Nave {i}", value=5.0, key=f"d_vig_{i}")
            with v_col7:
                num_vigas = st.number_input(f"Número de vigas - Nave {i}", value=8, step=1, key=f"n_vig_{i}")

            st.markdown("#### Columna")
            co_col1, co_col2, co_col3, co_col4, co_col5 = st.columns(5)
            with co_col1:
                tipo_col = st.text_input(f"Tipo Columna - Nave {i}", value="Perfil H", key=f"t_col_{i}")
            with co_col2:
                ancho_col = st.number_input(f"Ancho Columna - Nave {i}", value=0.3, key=f"a_col_{i}")
            with co_col3:
                alto_col = st.number_input(f"Alto Columna - Nave {i}", value=0.3, key=f"h_col_{i}")
            with co_col4:
                largo_col = st.number_input(f"Largo Columna - Nave {i}", value=10.0, key=f"l_col_{i}")
            with co_col5:
                calibre_col = st.text_input(f"Calibre/Espesor Columna - Nave {i}", value="1/2\"", key=f"c_col_{i}")

            co_col6, co_col7 = st.columns(2)
            with co_col6:
                dist_cols = st.number_input(f"Distancia entre columnas - Nave {i}", value=6.0, key=f"d_col_{i}")
            with co_col7:
                num_cols = st.number_input(f"Número de columnas - Nave {i}", value=10, step=1, key=f"n_col_{i}")

            naves_estructural_data[f"Nave {i}"] = {
                "N° Aguas": num_aguas, "Ancho": ancho, "Largo": largo, 
                "Altura Mayor": altura_mayor, "Altura Menor": altura_menor, 
                "Orientación": orientacion, "Inclinación": inclinacion,
                "Lámina Tipo": tipo_lamina, "Lámina Ancho": ancho_lamina, "Lámina Alto": alto_lamina, "Lámina Largo": largo_lamina, "Lámina Calibre": calibre_lamina,
                "Dist. Cresta": dist_cresta, "Altura Cresta": alt_cresta, "Ancho Cresta": ancho_cresta,
                "Montén Tipo": tipo_monten, "Montén Ancho": ancho_monten, "Montén Alto": alto_monten, "Montén Largo": largo_monten, "Montén Calibre": calibre_monten,
                "Dist. Montén": dist_montenes, "N° Montén": num_montenes,
                "Viga Tipo": tipo_viga, "Viga Ancho": ancho_viga, "Viga Alto": alto_viga, "Viga Largo": largo_viga, "Viga Calibre": calibre_viga,
                "Dist. Viga": dist_vigas, "N° Viga": num_vigas,
                "Columna Tipo": tipo_col, "Columna Ancho": ancho_col, "Columna Alto": alto_col, "Columna Largo": largo_col, "Columna Calibre": calibre_col,
                "Dist. Columna": dist_cols, "N° Columna": num_cols
            }

    st.markdown("---")
    st.header("Obstáculos")
    
    cant_obstaculos = st.number_input("¿Cuántos obstáculos hay?", min_value=0, max_value=20, value=1, step=1)
    
    obstaculos_data = {}
    for j in range(1, int(cant_obstaculos) + 1):
        with st.expander(f"Obstáculo {j}", expanded=(j == 1)):
            oc1, oc2 = st.columns(2)
            with oc1:
                nombre_obs = st.text_input(f"Nombre - Obstáculo {j}", value=f"Chimenea {j}", key=f"nom_obs_{j}")
                ubicacion_obs = st.text_input(f"Ubicación - Obstáculo {j}", value="Centro de techo", key=f"ubic_obs_{j}")
                foto_obs = st.text_input(f"Fotografía (Referencia) - Obstáculo {j}", value="Foto_Obs_1.jpg", key=f"foto_obs_{j}")
            with oc2:
                largo_obs = st.number_input(f"Largo (m) - Obstáculo {j}", value=1.5, key=f"l_obs_{j}")
                ancho_obs = st.number_input(f"Ancho (m) - Obstáculo {j}", value=1.0, key=f"a_obs_{j}")
                alto_obs = st.number_input(f"Alto (m) - Obstáculo {j}", value=2.0, key=f"h_obs_{j}")
            
            obstaculos_data[f"Obstáculo {j}"] = {
                "Nombre": nombre_obs,
                "Ubicación": ubicacion_obs,
                "Fotografía": foto_obs,
                "Largo": largo_obs,
                "Ancho": ancho_obs,
                "Alto": alto_obs
            }

# ---------------------------------------------------------
# PESTAÑA 3: LEVANTAMIENTO ELÉCTRICO (Anidado + Tableros, Armónicos y Baterías)
# ---------------------------------------------------------
with tab3:
    st.header("⚡ Levantamiento Eléctrico")
    
    st.subheader("Acometida")
    ac_col1, ac_col2, ac_col3 = st.columns(3)
    with ac_col1:
        voltaje_mt = st.text_input("Voltaje Media Tensión", value="13.2 kV")
    with ac_col2:
        calibre_cable_ac = st.text_input("Cableado - Calibre", value="2/0 AWG")
        tipo_cable_ac = st.text_input("Cableado - Tipo", value="AAC")
    with ac_col3:
        obs_acometida = st.text_input("Observaciones de Acometida", value="Sin novedad")

    st.markdown("---")
    st.subheader("Subestaciones y sus Equipos")
    
    cant_subestaciones = st.number_input("¿Cuántas subestaciones hay?", min_value=1, max_value=10, value=1, step=1)
    
    subestaciones_data = []
    transformadores_data = []
    itm_data = []

    for s in range(1, int(cant_subestaciones) + 1):
        with st.expander(f"Subestación {s}", expanded=(s == 1)):
            s_col1, s_col2 = st.columns(2)
            with s_col1:
                voltaje_bt = st.text_input(f"Voltaje Baja Tensión - Subestación {s}", value="440/254 V", key=f"volt_bt_{s}")
                tipo_sub = st.text_input(f"Tipo - Subestación {s}", value="Tipo pedestal", key=f"tipo_sub_{s}")
            with s_col2:
                ubicacion_sub = st.text_input(f"Ubicación - Subestación {s}", value="Patio central", key=f"ubic_sub_{s}")
                obs_sub = st.text_input(f"Observaciones - Subestación {s}", value="Buena ventilación", key=f"obs_sub_{s}")
            
            subestaciones_data.append({
                "Subestación": f"Subestación {s}",
                "Voltaje Baja Tensión": voltaje_bt,
                "Tipo": tipo_sub,
                "Ubicación": ubicacion_sub,
                "Observaciones": obs_sub
            })

            st.markdown(f"##### Transformadores de la Subestación {s}")
            cant_transformadores = st.number_input(f"¿Con cuántos transformadores cuenta la Subestación {s}?", min_value=0, max_value=10, value=1, step=1, key=f"cant_trans_s_{s}")
            
            for t in range(1, int(cant_transformadores) + 1):
                with st.expander(f"Transformador {t} (Subestación {s})"):
                    t_col1, t_col2, t_col3 = st.columns(3)
                    with t_col1:
                        volt_mt_trans = st.text_input(f"Voltaje Media Tensión", value="13.2 kV", key=f"v_mt_t_{s}_{t}")
                        volt_bt_trans = st.text_input(f"Voltaje Baja Tensión", value="440 V", key=f"v_bt_t_{s}_{t}")
                    with t_col2:
                        tipo_trans = st.text_input(f"Tipo", value="Seco", key=f"tipo_t_{s}_{t}")
                        capacidad_trans = st.text_input(f"Capacidad", value="500 kVA", key=f"cap_t_{s}_{t}")
                    with t_col3:
                        ubicacion_trans = st.text_input(f"Ubicación", value="Interior Subestación", key=f"ubic_t_{s}_{t}")
                        obs_trans = st.text_input(f"Observación", value="Operativo", key=f"obs_t_{s}_{t}")
                    
                    transformadores_data.append({
                        "Subestación": f"Subestación {s}",
                        "Transformador": f"Transformador {t}",
                        "Voltaje Media Tensión": volt_mt_trans,
                        "Voltaje Baja Tensión": volt_bt_trans,
                        "Tipo": tipo_trans,
                        "Capacidad": capacidad_trans,
                        "Ubicación": ubicacion_trans,
                        "Observación": obs_trans
                    })

                    st.markdown(f"###### ITM del Transformador {t} (Subestación {s})")
                    cant_itm = st.number_input(f"¿Con cuántos ITM cuenta el Transformador {t}?", min_value=0, max_value=20, value=1, step=1, key=f"cant_itm_s_{s}_t_{t}")
                    
                    for m in range(1, int(cant_itm) + 1):
                        i_col1, i_col2, i_col3 = st.columns(3)
                        with i_col1:
                            calibre_itm = st.text_input(f"Calibre - ITM {m}", value="3/0 AWG", key=f"cal_itm_{s}_{t}_{m}")
                        with i_col2:
                            material_cond = st.text_input(f"Material - ITM {m}", value="Cobre", key=f"mat_itm_{s}_{t}_{m}")
                            tipo_cond = st.text_input(f"Tipo Cond. - ITM {m}", value="THHW-LS", key=f"tipo_cond_{s}_{t}_{m}")
                        with i_col3:
                            tipo_canal = st.text_input(f"Canalización Tipo - ITM {m}", value="Conduit", key=f"t_canal_{s}_{t}_{m}")
                            tamano_canal = st.text_input(f"Canalización Tamaño - ITM {m}", value="2 pulgadas", key=f"tam_canal_{s}_{t}_{m}")
                        
                        itm_data.append({
                            "Subestación": f"Subestación {s}",
                            "Transformador": f"Transformador {t}",
                            "ITM": f"ITM {m}",
                            "Calibre": calibre_itm,
                            "Material Conductores": material_cond,
                            "Tipo Conductores": tipo_cond,
                            "Tipo Canalización": tipo_canal,
                            "Tamaño Canalización": tamano_canal
                        })

    st.markdown("---")
    st.subheader("Tableros")
    cant_tableros = st.number_input("¿Cuántos tableros hay?", min_value=0, max_value=20, value=1, step=1)
    
    tableros_data = []
    normas_tableros_data = []

    for tb in range(1, int(cant_tableros) + 1):
        with st.expander(f"Tablero {tb}", expanded=(tb == 1)):
            tb_c1, tb_c2 = st.columns(2)
            with tb_c1:
                modelo_tb = st.text_input(f"Modelo - Tablero {tb}", value="SquareD QO", key=f"mod_tb_{tb}")
                capacidad_tb = st.text_input(f"Capacidad - Tablero {tb}", value="225 A", key=f"cap_tb_{tb}")
                voltaje_tb = st.text_input(f"Voltaje - Tablero {tb}", value="220/127 V", key=f"volt_tb_{tb}")
                fases_tb = st.text_input(f"Fases e hilos - Tablero {tb}", value="3 Fases, 4 Hilos", key=f"fases_tb_{tb}")
            with tb_c2:
                itm_ppal_tb = st.text_input(f"ITM principal - Tablero {tb}", value="100 A", key=f"itm_p_tb_{tb}")
                itm_der_tb = st.text_input(f"ITM derivados - Tablero {tb}", value="Varios (15A, 20A, 30A)", key=f"itm_d_tb_{tb}")
                proviene_tb = st.text_input(f"Proviene de - Tablero {tb}", value="Subestación 1", key=f"prov_tb_{tb}")
                distancia_tb = st.text_input(f"Distancia - Tablero {tb}", value="15 metros", key=f"dist_tb_{tb}")

            st.markdown(f"###### Conductores y Canalización - Tablero {tb}")
            tc_c1, tc_c2 = st.columns(2)
            with tc_c1:
                cal_cond_tb = st.text_input(f"Calibre Conductores - Tablero {tb}", value="1/0 AWG", key=f"cal_c_tb_{tb}")
                mat_cond_tb = st.text_input(f"Material Conductores - Tablero {tb}", value="Cobre", key=f"mat_c_tb_{tb}")
                cant_fase_tb = st.text_input(f"Cantidad por fase - Tablero {tb}", value="1", key=f"cant_f_tb_{tb}")
                neutro_tb = st.text_input(f"Neutro - Tablero {tb}", value="Sí", key=f"neut_tb_{tb}")
                espacios_tb = st.radio(f"¿El tablero cuenta con espacios disponibles? - Tablero {tb}", ["Si", "No"], key=f"esp_tb_{tb}")
                cuantos_esp = st.number_input(f"¿Cuántos espacios? - Tablero {tb}", min_value=0, max_value=42, value=4, key=f"c_esp_tb_{tb}")
            with tc_c2:
                tipo_canal_tb = st.text_input(f"Canalización Tipo - Tablero {tb}", value="Conduit EMT", key=f"t_can_tb_{tb}")
                tam_canal_tb = st.text_input(f"Canalización Tamaño - Tablero {tb}", value="1.5 pulgadas", key=f"tam_can_tb_{tb}")

            tableros_data.append({
                "Tablero": f"Tablero {tb}",
                "Modelo": modelo_tb,
                "Capacidad": capacidad_tb,
                "Voltaje": voltaje_tb,
                "Fases e hilos": fases_tb,
                "ITM Principal": itm_ppal_tb,
                "ITM Derivados": itm_der_tb,
                "Proviene de": proviene_tb,
                "Distancia": distancia_tb,
                "Calibre Conductores": cal_cond_tb,
                "Material Conductores": mat_cond_tb,
                "Cantidad por fase": cant_fase_tb,
                "Neutro": neutro_tb,
                "Espacios disponibles": espacios_tb,
                "Cuántos espacios": cuantos_esp,
                "Canalización Tipo": tipo_canal_tb,
                "Canalización Tamaño": tam_canal_tb
            })

            st.markdown(f"###### ¿Cumple con la norma? - Tablero {tb}")
            n1 = st.checkbox(f"¿Tiene ITM principal? - Tablero {tb}", value=True, key=f"norm_1_{tb}")
            n2 = st.checkbox(f"Respeta código de colores - Tablero {tb}", value=True, key=f"norm_2_{tb}")
            n3 = st.checkbox(f"Los circuitos sin utilizar están libres/protegidos - Tablero {tb}", value=True, key=f"norm_3_{tb}")
            n4 = st.checkbox(f"El tablero está cerrado - Tablero {tb}", value=True, key=f"norm_4_{tb}")
            n5 = st.checkbox(f"El cable se encuentra en buen estado - Tablero {tb}", value=True, key=f"norm_5_{tb}")
            n6 = st.checkbox(f"Se encuentra debidamente identificado/etiquetado - Tablero {tb}", value=True, key=f"norm_6_{tb}")
            n7 = st.checkbox(f"Presenta daño o deterioro - Tablero {tb}", value=False, key=f"norm_7_{tb}")

            normas_tableros_data.append({
                "Tablero": f"Tablero {tb}",
                "¿Tiene ITM principal?": n1,
                "Respeta código de colores": n2,
                "Circuitos sin utilizar correctos": n3,
                "El tablero está cerrado": n4,
                "Cable en buen estado": n5,
                "Debidamente identificado": n6,
                "Presenta daño o deterioro": n7
            })

    st.markdown("---")
    st.subheader("Identificación de Armónicos")
    giro_empresa = st.text_input("¿Cuál es el giro de la empresa?", value="Manufactura metalmecánica")

    st.markdown("¿La instalación cuenta con los siguientes equipos?")
    equipos_armonicos = [
        "Soldadura industrial",
        "Fuentes de alimentación",
        "Variadores de Frecuencia (VF)",
        "Equipos electrónicos modernos sensibles",
        "Hornos de arco",
        "Rectificadores conmutados en línea",
        "Balastros para iluminación",
        "Mención directa por parte del cliente"
    ]

    armonicos_data = []
    for eq in equipos_armonicos:
        eq_col1, eq_col2 = st.columns(2)
        with eq_col1:
            existe_eq = st.checkbox(f"Existe: {eq}", value=False, key=f"chk_eq_{eq}")
        with eq_col2:
            cant_eq = st.number_input(f"Cantidad - {eq}", min_value=0, max_value=100, value=0, step=1, key=f"cant_eq_{eq}")
        
        armonicos_data.append({
            "Equipo": eq,
            "Existe": "Sí" if existe_eq else "No",
            "Cantidad": cant_eq
        })

    st.markdown("---")
    st.subheader("Espacio para Baterías")
    b_c1, b_c2 = st.columns(2)
    with b_c1:
        temp_amb = st.text_input("Temperatura ambiente", value="25 °C")
        tipo_terr = st.text_input("Tipo de terreno", value="Concreto planchado")
        def_terr = st.text_input("¿El terreno tiene alguna deformación o desnivel?", value="Ninguno")
        medidas_baterias = st.text_input("Medidas (LxA)", value="3m x 2m")
    with b_c2:
        espacio_int_ext = st.radio("Espacio interior o exterior", ["Interior", "Exterior"], index=0)
        inst_adic_bat = st.text_input("¿Cuenta con instalación adicional (gas, hidráulica, etc.)?", value="Ninguna")
        otro_bat = st.text_input("En el lugar de instalación existen factores / Otro", value="Área ventilada")

    baterias_data = [{
        "Temperatura ambiente": temp_amb,
        "Tipo de terreno": tipo_terr,
        "Deformación o desnivel": def_terr,
        "Medidas (LxA)": medidas_baterias,
        "Espacio interior/exterior": espacio_int_ext,
        "Instalación adicional": inst_adic_bat,
        "Otros factores": otro_bat
    }]

# ---------------------------------------------------------
# PESTAÑA 4: EVALUACIÓN Y DESCARGA
# ---------------------------------------------------------
with tab4:
    st.header("🏗️ Evaluación Estructural General")
    eval_estructural = st.text_area("Comentarios sobre evaluación estructural (requiere DRO / refuerzos):")

    st.markdown("---")
    st.subheader("📄 Generar y Descargar Archivo Excel de Etapa 2")

    def generar_excel_etapa2():
        output = io.BytesIO()
        
        # 1. Datos de Drone
        df_drone = pd.DataFrame({
            "Vista / Fotografía": [
                "Techumbre", "Vistas aéreas (Vista de águila)", "Vistas frontales", 
                "Vistas laterales", "Vistas traseras", "Fotos de lámina", 
                "Fotos de obstáculos", "Video de drone", "Terreno y periferia"
            ],
            "Estatus": [
                "✔" if drone_techumbre else "X",
                "✔" if drone_aguila else "X",
                "✔" if drone_frontales else "X",
                "✔" if drone_laterales else "X",
                "✔" if drone_traseras else "X",
                "✔" if drone_lamina else "X",
                "✔" if drone_obstaculos else "X",
                "✔" if drone_video else "X",
                "✔" if drone_terreno else "X"
            ]
        })

        # 2. Seguridad y Acceso
        df_seguridad = pd.DataFrame({
            "Concepto": [
                "Existe un acceso a techumbre de fácil acceso",
                "¿Para acceso a techumbre se requiere equipo adicional? (Escalera, arnés, anclaje móvil, etc.)?",
                "Existen líneas energizadas en el área a instalar",
                "El estado físico del techo losa o terreno es buena",
                "Existen pasos de gato*",
                "Existen líneas de vida*",
                "Escalera marina",
                "Toma de agua cercana",
                "Sistema de pararrayos"
            ],
            "Respuesta": [
                facil_acceso, equipo_adic, lineas_energ, estado_techo, 
                pasos_gato, lineas_vida, esc_marina, toma_agua, pararrayos
            ],
            "Observaciones": [
                obs_acceso, obs_equipo, obs_lineas, obs_estado, 
                obs_pasos, obs_vida, obs_esc, obs_agua, obs_pararrayos
            ]
        })

        # 3. Estructural y Obstáculos
        df_estructural = pd.DataFrame(naves_estructural_data).T.reset_index().rename(columns={"index": "Nave"}) if naves_estructural_data else pd.DataFrame()
        df_obstaculos = pd.DataFrame(obstaculos_data).T.reset_index().rename(columns={"index": "Obstáculo"}) if obstaculos_data else pd.DataFrame()

        # 4. Eléctrico
        df_acometida = pd.DataFrame({
            "Concepto": ["Acometida"],
            "Voltaje Media Tensión": [voltaje_mt],
            "Cableado Calibre": [calibre_cable_ac],
            "Cableado Tipo": [tipo_cable_ac],
            "Observaciones": [obs_acometida]
        })
        df_subestaciones = pd.DataFrame(subestaciones_data) if subestaciones_data else pd.DataFrame()
        df_transformadores = pd.DataFrame(transformadores_data) if transformadores_data else pd.DataFrame()
        df_itm = pd.DataFrame(itm_data) if itm_data else pd.DataFrame()
        
        df_tableros = pd.DataFrame(tableros_data) if tableros_data else pd.DataFrame()
        df_normas_tableros = pd.DataFrame(normas_tableros_data) if normas_tableros_data else pd.DataFrame()
        df_armonicos = pd.DataFrame([{"Giro empresa": giro_empresa}])
        df_equipos_arm = pd.DataFrame(armonicos_data) if armonicos_data else pd.DataFrame()
        df_baterias = pd.DataFrame(baterias_data) if baterias_data else pd.DataFrame()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_drone.to_excel(writer, sheet_name='Drone', index=False)
            df_seguridad.to_excel(writer, sheet_name='Acceso y Seguridad', index=False)
            if not df_estructural.empty:
                df_estructural.to_excel(writer, sheet_name='Levantamiento Estructural', index=False)
            if not df_obstaculos.empty:
                df_obstaculos.to_excel(writer, sheet_name='Obstáculos', index=False)
            
            df_acometida.to_excel(writer, sheet_name='Eléctrico - Acometida', index=False)
            if not df_subestaciones.empty:
                df_subestaciones.to_excel(writer, sheet_name='Eléctrico - Subestaciones', index=False)
            if not df_transformadores.empty:
                df_transformadores.to_excel(writer, sheet_name='Eléctrico - Transformadores', index=False)
            if not df_itm.empty:
                df_itm.to_excel(writer, sheet_name='Eléctrico - ITM', index=False)
            if not df_tableros.empty:
                df_tableros.to_excel(writer, sheet_name='Eléctrico - Tableros', index=False)
            if not df_normas_tableros.empty:
                df_normas_tableros.to_excel(writer, sheet_name='Eléctrico - Normas Tableros', index=False)
            if not df_armonicos.empty:
                df_armonicos.to_excel(writer, sheet_name='Eléctrico - Armónicos', index=False)
            if not df_equipos_arm.empty:
                df_equipos_arm.to_excel(writer, sheet_name='Eléctrico - Equipos Armónicos', index=False)
            if not df_baterias.empty:
                df_baterias.to_excel(writer, sheet_name='Eléctrico - Baterías', index=False)

        output.seek(0)
        return output

    excel_file = generar_excel_etapa2()

    st.download_button(
        label="📥 Descargar Reporte Etapa 2 en Excel (.xlsx)",
        data=excel_file,
        file_name="Levantamiento_Etapa2_Completado.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary"
    )
