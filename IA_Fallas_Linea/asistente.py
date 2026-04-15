import streamlit as st
import pandas as pd

# 1. Configuración de la página 🚀
st.set_page_config(page_title="Asistente PROMINOX", page_icon="🚀", layout="wide")

# --- CONFIGURACIÓN DE LÍNEAS ---
LÍNEAS = {
    "LC2": "https://docs.google.com/spreadsheets/d/1Q-9KlzBBjOPLm9M-YsG7yf7gmyVpnGW5ML6Ej8gyidM/export?format=xlsx",
    "LC1": "https://docs.google.com/spreadsheets/d/1-f3swj7PF36MdwsWhObbPTQwd7voorG4/export?format=xlsx",
    "LPH": "AQUÍ_PEGARÁS_EL_LINK_DE_LA_LINEA_3",
    "LPR": "AQUÍ_PEGARÁS_EL_LINK_DE_LA_LINEA_4",
    "LCL": "AQUÍ_PEGARÁS_EL_LINK_DE_LA_LINEA_5",
    "MCL": "AQUÍ_PEGARÁS_EL_LINK_DE_LA_LINEA_6",
    "OSC": "AQUÍ_PEGARÁS_EL_LINK_DE_LA_LINEA_7"
}

st.title("🚀 Asistente Técnico PROMINOX")
st.info("🤖 ¡Bienvenido, equipo! Selecciona tu línea y cuéntame en qué te puedo ayudar hoy.")
st.markdown("---")

linea_seleccionada = st.selectbox("📍 ¿En qué línea estás trabajando?", list(LÍNEAS.keys()))

@st.cache_data(ttl=10) 
def cargar_datos(url):
    try:
        todas_las_hojas = pd.read_excel(url, sheet_name=None, header=0)
        tabla_maestra = pd.DataFrame()
        for nombre_hoja, datos_hoja in todas_las_hojas.items():
            datos_hoja.columns = datos_hoja.columns.astype(str).str.strip()
            datos_hoja['Maquina_o_Area'] = nombre_hoja.strip()
            tabla_maestra = pd.concat([tabla_maestra, datos_hoja], ignore_index=True)
            
        # FILTRO POKA-YOKE: Borrar filas completamente vacías
        if 'Problemas comunes' in tabla_maestra.columns:
            tabla_maestra = tabla_maestra.dropna(subset=['Problemas comunes'])
            
        return tabla_maestra
    except:
        return None

url_actual = LÍNEAS[linea_seleccionada]

if "AQUÍ_PEGARÁS" in url_actual:
    st.warning(f"Línea {linea_seleccionada} en espera de configuración por el Jefe de Procedimientos.")
else:
    tabla_maestra = cargar_datos(url_actual)
    
    if tabla_maestra is not None:
        busqueda = st.text_input(f"🔍 Escribe aquí (falla, saludo o despedida) para la {linea_seleccionada}:", placeholder="Ej: Calidad, Sensor, Hola, Gracias...")

        if busqueda:
            busqueda_limpia = busqueda.strip().lower()
            
            # 1. Saludos amables 👋
            if busqueda_limpia in ["hola", "buen dia", "buen día", "buenos dias", "buenas tardes", "buenas noches", "saludos", "que tal", "qué tal"]:
                st.info(f"¡Hola, compañero! 👋 Qué gusto saludarte. Estoy al 100% y listo para apoyarte en la {linea_seleccionada}. ¡Vamos a sacar esa producción adelante!")
                
            # 2. Agradecimientos motivadores 🙏
            elif busqueda_limpia in ["gracias", "muchas gracias", "mil gracias", "listo", "ok", "entendido", "excelente", "perfecto"]:
                st.success("¡Es un placer hacer equipo contigo! 🚀 Estamos aquí para que la máquina no pare y tu trabajo sea más fácil. ¡Mucho éxito en lo que resta del turno!")
                
            # 3. Despedidas cordiales 🚪
            elif busqueda_limpia in ["adios", "adiós", "bye", "hasta luego", "nos vemos", "hasta mañana", "ya me voy", "fin de turno"]:
                st.success("¡Hasta luego, operador! 👋 Que tengas un excelente descanso, te lo has ganado. ¡Aquí estaré esperándote para el próximo turno! 🏭✨")
                
            # 4. Búsqueda de Fallas 🔍
            else:
                mask = tabla_maestra.astype(str).apply(lambda col: col.str.contains(busqueda_limpia, case=False, na=False)).any(axis=1)
                resultados = tabla_maestra[mask]
                
                if len(resultados) == 0:
                    st.error("Hmm, no encontré esa falla en mis manuales. 🤔 ¿Podrías escribirlo con otras palabras?")
                else:
                    st.success(f"¡Excelente! Encontré {len(resultados)} posibles soluciones. Aquí te las muestro:")
                    for index, fila in resultados.iterrows():
                        with st.expander(f"📍 ÁREA: {fila['Maquina_o_Area']}", expanded=True):
                            
                            # LA MAGIA DE LA LIMPIEZA VISUAL 🧹✨
                            for col in resultados.columns:
                                val = fila[col]
                                # Ignoramos las columnas feas de Excel y los valores nulos o "None"
                                if col != 'Maquina_o_Area' and 'Unnamed' not in str(col):
                                    if pd.notna(val) and str(val).strip().lower() not in ['none', 'nan', '']:
                                        st.markdown(f"*{col}*: {val}")
    else:
        st.error(f"❌ La App no puede entrar al archivo de {linea_seleccionada}. Revisa los permisos en Google Drive.")
