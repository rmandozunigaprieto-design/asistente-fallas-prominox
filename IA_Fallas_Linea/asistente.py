import streamlit as st
import pandas as pd

# 1. Configuración de la página 🚀
st.set_page_config(page_title="Asistente PROMINOX", page_icon="🚀", layout="wide")

# --- CONFIGURACIÓN DE LÍNEAS (Links Seguros) ---
LÍNEAS = {
    # Este es el link del archivo nuevo que creaste (Hoja de Google)
    "LC2": "https://docs.google.com/spreadsheets/d/1Q-9KlzBBjOPLm9M-YsG7yf7gmyVpnGW5ML6Ej8gyidM/export?format=xlsx",
    "LC1": "https://docs.google.com/spreadsheets/d/1-f3swj7PF36MdwsWhObbPTQwd7voorG4/export?format=xlsx",
    "LPH": "AQUÍ_PEGARÁS_EL_LINK_DE_LA_LINEA_3",
    "LPR": "AQUÍ_PEGARÁS_EL_LINK_DE_LA_LINEA_4",
    "LCL": "AQUÍ_PEGARÁS_EL_LINK_DE_LA_LINEA_5",
    "MCL": "AQUÍ_PEGARÁS_EL_LINK_DE_LA_LINEA_6",
    "OSC": "AQUÍ_PEGARÁS_EL_LINK_DE_LA_LINEA_7"
}

st.title("🚀 Asistente Técnico PROMINOX")
st.info("🤖 ¡Bienvenido! Selecciona tu línea para resolver la falla.")

st.markdown("---")

linea_seleccionada = st.selectbox("📍 ¿En qué línea estás trabajando?", list(LÍNEAS.keys()))

@st.cache_data(ttl=10) 
def cargar_datos(url):
    try:
        # Aquí la App usa el "túnel" secreto para leer tu Drive
        todas_las_hojas = pd.read_excel(url, sheet_name=None, header=0)
        tabla_maestra = pd.DataFrame()
        for nombre_hoja, datos_hoja in todas_las_hojas.items():
            datos_hoja.columns = datos_hoja.columns.astype(str).str.strip()
            datos_hoja['Maquina_o_Area'] = nombre_hoja.strip()
            tabla_maestra = pd.concat([tabla_maestra, datos_hoja], ignore_index=True)
        return tabla_maestra
    except:
        return None

url_actual = LÍNEAS[linea_seleccionada]

if "AQUÍ_PEGARÁS" in url_actual:
    st.warning(f"Línea {linea_seleccionada} en espera de configuración.")
else:
    tabla_maestra = cargar_datos(url_actual)
    
    # SI LOS DATOS CARGAN, LA BARRA APARECE
    if tabla_maestra is not None:
        busqueda = st.text_input(f"🔍 Describe la falla en {linea_seleccionada}:", placeholder="Ej: Calidad, Sensor, OT...")

        if busqueda:
            busqueda_limpia = busqueda.strip().lower()
            mask = tabla_maestra.astype(str).apply(lambda col: col.str.contains(busqueda_limpia, case=False, na=False)).any(axis=1)
            resultados = tabla_maestra[mask]
            
            if len(resultados) == 0:
                st.error("No encontré esa falla.")
            else:
                st.success(f"¡Encontré {len(resultados)} soluciones!")
                for index, fila in resultados.iterrows():
                    with st.expander(f"📍 ÁREA: {fila['Maquina_o_Area']}", expanded=True):
                        st.write(fila)
    else:
        # Esto te avisará si el permiso de Drive está cerrado
        st.error(f"❌ La App no puede entrar al archivo de {linea_seleccionada}. Revisa que en el Drive el botón azul diga 'Cualquier usuario con el enlace'.")
