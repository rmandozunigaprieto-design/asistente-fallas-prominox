import streamlit as st
import pandas as pd

st.set_page_config(page_title="Asistente de Fallas PROMINOX", layout="wide")

# --- CONFIGURACIÓN DE LÍNEAS ---
# Aquí irás pegando los links de los Excels de cada línea conforme los crees
LÍNEAS = {
    "Línea 1": "https://docs.google.com/spreadsheets/d/1dY2n8XXTDHZ1aj1MPAnDcrTIhZt6uTBL/export?format=xlsx",
    "Línea 2": "AQUÍ_PEGARÁS_EL_LINK_DE_LA_LINEA_2",
    "Línea 3": "AQUÍ_PEGARÁS_EL_LINK_DE_LA_LINEA_3"
}

st.title("🚀 Asistente Técnico PROMINOX")
st.markdown("---")

# 1. Selector de Línea (Poka-Yoke de ubicación)
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
        return tabla_maestra
    except:
        return None

# Cargar datos de la línea elegida
url_actual = LÍNEAS[linea_seleccionada]

if "AQUÍ_PEGARÁS" in url_actual:
    st.warning(f"Todavía no has configurado el Excel para la {linea_seleccionada}, Jefe.")
else:
    tabla_maestra = cargar_datos(url_actual)
    
    busqueda = st.text_input(f"🔍 Describe la falla en {linea_seleccionada}:", placeholder="Ej: Calidad, Apilado, Sensor...")

    if busqueda:
        busqueda_limpia = busqueda.strip().lower()
        if busqueda_limpia in ["hola", "buen dia", "saludos"]:
            st.write(f"¡Hola Armando! Listo para apoyar en la {linea_seleccionada}. ¿Qué falla reportan?")
        else:
            # Búsqueda inteligente
            mask = tabla_maestra.astype(str).apply(lambda col: col.str.contains(busqueda_limpia, case=False, na=False)).any(axis=1)
            resultados = tabla_maestra[mask]
            
            if len(resultados) == 0:
                st.error("No encontré esa falla. ¿Gustas intentar con otra palabra?")
            else:
                st.success(f"¡Encontré {len(resultados)} soluciones para {linea_seleccionada}!")
                for index, fila in resultados.iterrows():
                    with st.expander(f"📍 ÁREA: {fila['Maquina_o_Area']}", expanded=True):
                        for col in resultados.columns:
                            if col != 'Maquina_o_Area' and 'Unnamed' not in col and pd.notna(fila[col]):
                                st.markdown(f"*{col}*: {fila[col]}")