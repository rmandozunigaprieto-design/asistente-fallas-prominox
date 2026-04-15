import streamlit as st
import pandas as pd

# 1. Configuración de la página ¡con el cohete intacto! 🚀
st.set_page_config(page_title="Asistente PROMINOX", page_icon="🚀", layout="wide")

# --- CONFIGURACIÓN DE LÍNEAS ---
LÍNEAS = {
    "LC2": "https://docs.google.com/spreadsheets/d/1dY2n8XXTDHZ1aj1MPAnDcrTIhZt6uTBL/export?format=xlsx",
    "LC1": "https://docs.google.com/spreadsheets/d/1-f3swj7PF36MdwsWhObbPTQwd7voorG4/export?format=xlsx",
    "LPH": "AQUÍ_PEGARÁS_EL_LINK_DE_LA_LINEA_3",
    "LPR": "AQUÍ_PEGARÁS_EL_LINK_DE_LA_LINEA_4",
    "LCL": "AQUÍ_PEGARÁS_EL_LINK_DE_LA_LINEA_5",
    "MCL": "AQUÍ_PEGARÁS_EL_LINK_DE_LA_LINEA_6",
    "OSC": "AQUÍ_PEGARÁS_EL_LINK_DE_LA_LINEA_7"
}

# 2. Encabezado
st.title("🚀 Asistente Técnico PROMINOX")
st.info("🤖 ¡Bienvenido, operador! Soy tu soporte de Inteligencia Artificial. Selecciona tu línea y dime qué problema tenemos hoy.")

st.markdown("---")

# 3. Selector de Línea
linea_seleccionada = st.selectbox("📍 ¿En qué línea estás trabajando?", list(LÍNEAS.keys()))

@st.cache_data(ttl=10)
def cargar_datos(url):
    try:
        todas_las_hojas = pd.read_excel(url, sheet_name=None, header=0)
        tabla_maestra = pd.DataFrame()
        for nombre_hoja, datos_hoja in todas_las_hojas.items():
            datos_hoja.columns = datos_hoja.columns.astype(str).str.replace('\n', ' ').str.strip()
            datos_hoja = datos_hoja.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            datos_hoja = datos_hoja.ffill()
            datos_hoja['Maquina_o_Area'] = nombre_hoja.strip()
            tabla_maestra = pd.concat([tabla_maestra, datos_hoja], ignore_index=True)
        
        # VERIFICACIÓN TÉCNICA DE COLUMNAS
        if 'Problemas comunes' not in tabla_maestra.columns:
            st.error(f"⚠️ Error en el Excel: No encontré la columna 'Problemas comunes'. Revisa que esté escrita igualito.")
            return None
            
        tabla_maestra = tabla_maestra.dropna(subset=['Problemas comunes'])
        return tabla_maestra
    except Exception as e:
        st.error(f"❌ Error de conexión: No pude leer el archivo de la {linea_seleccionada}. Verifica los permisos de 'Compartir'.")
        return None

# Cargar datos
url_actual = LÍNEAS[linea_seleccionada]

if "AQUÍ_PEGARÁS" in url_actual:
    st.warning(f"Todavía no se ha configurado el sistema para la {linea_seleccionada}.")
else:
    tabla_maestra = cargar_datos(url_actual)
    
    if tabla_maestra is not None:
        busqueda = st.text_input(f"🔍 Describe la falla en {linea_seleccionada}:", placeholder="Ej: Calidad, Sensor, OT...")

        if busqueda:
            busqueda_limpia = busqueda.strip().lower()
            
            if busqueda_limpia in ["hola", "buen dia", "buenos dias", "buenas tardes", "buenas noches", "saludos"]:
                st.info(f"¡Hola, operador! 👋 Listo para apoyar en la {linea_seleccionada}.")
            elif busqueda_limpia in ["gracias", "muchas gracias", "mil gracias", "listo", "ok", "entendido"]:
                st.success("¡De nada, equipo! 🚀")
            else:
                if len(busqueda_limpia) <= 3:
                    mask = tabla_maestra.astype(str).apply(lambda col: col.str.contains(r'\b' + busqueda_limpia + r'\b', case=False, na=False, regex=True)).any(axis=1)
                else:
                    mask = tabla_maestra.astype(str).apply(lambda col: col.str.contains(busqueda_limpia, case=False, na=False)).any(axis=1)
                    
                resultados = tabla_maestra[mask]
                
                if len(resultados) == 0:
                    st.error("No encontré esa falla.")
                else:
                    st.success(f"¡Encontré {len(resultados)} soluciones!")
                    for index, fila in resultados.iterrows():
                        with st.expander(f"📍 ÁREA: {fila['Maquina_o_Area']}", expanded=True):
                            for col in resultados.columns:
                                if col != 'Maquina_o_Area' and 'Unnamed' not in col and pd.notna(fila[col]):
                                    st.markdown(f"*{col}*: {fila[col]}")
