import pandas as pd
import streamlit as st

# Configuración visual de la App
st.set_page_config(page_title="Asistente PROMINOX", page_icon="🤖")

# OJO: Ya NO lleva el @st.cache_data para que lea tu Excel en tiempo real
@st.cache_data(ttl=10) # Se actualiza cada 10 segundos para no tener desfases
def cargar_datos():
    url_excel = "https://docs.google.com/spreadsheets/d/1dY2n8XXTDHZ1aj1MPAnDcrTIhZt6uTBL/export?format=xlsx"
    todas_las_hojas = pd.read_excel(url_excel, sheet_name=None, header=0)
    tabla_maestra = pd.DataFrame()
    
    for nombre_hoja, datos_hoja in todas_las_hojas.items():
        # Limpieza de títulos
        datos_hoja.columns = datos_hoja.columns.astype(str).str.replace('\n', ' ').str.strip()
        
        # EL FILTRO POKA-YOKE: Borra espacios invisibles en todas las celdas
        datos_hoja = datos_hoja.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        
        datos_hoja = datos_hoja.ffill()
        datos_hoja['Maquina_o_Area'] = nombre_hoja.strip()
        tabla_maestra = pd.concat([tabla_maestra, datos_hoja], ignore_index=True)
        
    if 'Problemas comunes' in tabla_maestra.columns:
        tabla_maestra = tabla_maestra.dropna(subset=['Problemas comunes'])
        
    return tabla_maestra
tabla_maestra = cargar_datos()

st.title("🤖 Asistente de Fallas PROMINOX")
st.info("👋 *¡Bienvenido operador!* Sistema de Inteligencia Artificial activo. Ingresa tu falla para recibir la solución técnica")
st.write("Busca por máquina (Cizalla, Enganche) o por el nombre del problema.")

busqueda = st.text_input("¿Qué tenemos que resolver, operador?:")

if busqueda:
        # Ponemos lo que escribió el operador en minúsculas para que no importe si usa mayúsculas
        texto_limpio = busqueda.lower().strip()
        
        # 1. Filtro de saludos 👋
        if texto_limpio in ['hola', 'buenos dias', 'buenas tardes', 'buenas noches', 'que tal', 'buenos días', 'buenas']:
            st.success("¡Hola! Qué gusto saludarte. 👋 Soy tu asistente de PROMINOX. Dime, ¿en qué máquina o proceso te puedo ayudar hoy?")
            
        # 2. Filtro de agradecimientos 🙏
        elif texto_limpio in ['gracias', 'muchas gracias', 'excelente', 'listo', 'ok', 'va']:
            st.success("¡De nada! Para eso estamos. ¡A darle con todo a la producción! 🚀")
            
        # 3. Si no es saludo ni gracias, entonces SÍ buscamos la falla en el Excel 🔍
        else:
            mask = tabla_maestra.astype(str).apply(lambda col: col.str.contains(busqueda, case=False, na=False)).any(axis=1)
            resultados = tabla_maestra[mask]
            
            if len(resultados) == 0:
                st.warning(f"No encontré nada para '{busqueda}'.")
            else:
                st.success(f"¡Encontré {len(resultados)} soluciones!")
                for index, fila in resultados.iterrows():
                    with st.expander(f"📍 ÁREA: {fila['Maquina_o_Area']}", expanded=True):
                        for col in resultados.columns:
                            if col != 'Maquina_o_Area' and 'Unnamed' not in col and pd.notna(fila[col]):
                                st.markdown(f"*{col}*: {fila[col]}")