import streamlit as st
import pandas as pd

# 1. Configuración de la página ¡con el cohete intacto! 🚀
st.set_page_config(page_title="Asistente PROMINOX", page_icon="🚀", layout="wide")

# --- CONFIGURACIÓN DE LÍNEAS (Links Maestros) ---
LÍNEAS = {
    "LC2": "https://docs.google.com/spreadsheets/d/1Q-9KlzBBjOPLm9M-YsG7yf7gmyVpnGW5ML6Ej8gyidM/export?format=xlsx",
    "LC1": "https://docs.google.com/spreadsheets/d/1-f3swj7PF36MdwsWhObbPTQwd7voorG4/export?format=xlsx",
    "LPH": "AQUÍ_PEGARÁS_EL_LINK_DE_LA_LINEA_3",
    "LPR": "AQUÍ_PEGARÁS_EL_LINK_DE_LA_LINEA_4",
    "LCL": "AQUÍ_PEGARÁS_EL_LINK_DE_LA_LINEA_5",
    "MCL": "AQUÍ_PEGARÁS_EL_LINK_DE_LA_LINEA_6",
    "OSC": "AQUÍ_PEGARÁS_EL_LINK_DE_LA_LINEA_7"
}

# 2. Encabezado de la App
st.title("🚀 Asistente Técnico PROMINOX")
st.info("🤖 ¡Bienvenido, operador! Soy tu soporte de Inteligencia Artificial. Selecciona tu línea y dime qué falla tenemos hoy.")

st.markdown("---")

# 3. Selector de Línea
linea_seleccionada = st.selectbox("📍 ¿En qué línea estás trabajando?", list(LÍNEAS.keys()))

@st.cache_data(ttl=10) # Actualiza cada 10 segundos
def cargar_datos(url):
    try:
        # Intenta descargar el Excel desde Google Drive
        todas_las_hojas = pd.read_excel(url, sheet_name=None, header=0)
        tabla_maestra = pd.DataFrame()
        
        for nombre_hoja, datos_hoja in todas_las_hojas.items():
            # Limpieza Poka-Yoke de nombres de columnas
            datos_hoja.columns = datos_hoja.columns.astype(str).str.replace('\n', ' ').str.strip()
            # Limpieza de espacios en las celdas
            datos_hoja = datos_hoja.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            datos_hoja = datos_hoja.ffill()
            datos_hoja['Maquina_o_Area'] = nombre_hoja.strip()
            tabla_maestra = pd.concat([tabla_maestra, datos_hoja], ignore_index=True)
        
        # Validación de columna clave
        if 'Problemas comunes' not in tabla_maestra.columns:
            st.error(f"⚠️ Error en el Excel: No encontré la columna 'Problemas comunes'.")
            return None
            
        tabla_maestra = tabla_maestra.dropna(subset=['Problemas comunes'])
        return tabla_maestra
    except Exception as e:
        # Si falla el link, nos avisa qué pasó
        st.error(f"❌ Error de conexión con {linea_seleccionada}: Verifica los permisos de 'Compartir' en Drive.")
        return None

# Ejecución de la App
url_actual = LÍNEAS[linea_seleccionada]

if "AQUÍ_PEGARÁS" in url_actual:
    st.warning(f"Todavía no se ha configurado el sistema para la {linea_seleccionada}.")
else:
    tabla_maestra = cargar_datos(url_actual)
    
    if tabla_maestra is not None:
        busqueda = st.text_input(f"🔍 Describe la falla en {linea_seleccionada}:", placeholder="Ej: Calidad, Sensor, OT...")

        if busqueda:
            busqueda_limpia = busqueda.strip().lower()
            
            # Respuestas automáticas (Chat básico)
            if busqueda_limpia in ["hola", "buen dia", "buenos dias", "buenas tardes", "buenas noches", "saludos"]:
                st.info(f"¡Hola, operador! 👋 Listo para apoyar en la {linea_seleccionada}.")
            elif busqueda_limpia in ["gracias", "muchas gracias", "mil gracias", "listo", "ok", "entendido"]:
                st.success("¡De nada! Estamos para que la producción no se detenga. 🚀")
            else:
                # Buscador de fallas
                if len(busqueda_limpia) <= 3:
                    mask = tabla_maestra.astype(str).apply(lambda col: col.str.contains(r'\b' + busqueda_limpia + r'\b', case=False, na=False, regex=True)).any(axis=1)
                else:
                    mask = tabla_maestra.astype(str).apply(lambda col: col.str.contains(busqueda_limpia, case=False, na=False)).any(axis=1)
                    
                resultados = tabla_maestra[mask]
                
                if len(resultados) == 0:
                    st.error("No encontré esa falla. Intenta con otra palabra.")
                else:
                    st.success(f"¡Encontré {len(resultados)} soluciones para {linea_seleccionada}!")
                    for index, fila in resultados.iterrows():
                        with st.expander(f"📍 ÁREA: {fila['Maquina_o_Area']}", expanded=True):
                            for col in resultados.columns:
                                if col != 'Maquina_o_Area' and 'Unnamed' not in col and pd.notna(fila[col]):
                                    st.markdown(f"*{col}*: {fila[col]}")
[11:36 a.m., 15/4/2026] Armando Zúñiga.: L
[11:36 a.m., 15/4/2026] Armando Zúñiga.: import streamlit as st
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
