# app.py
import streamlit as st
import pandas as pd
import io
import xlsxwriter # Necesario para exportar a .xlsx

# --- Lógica de limpieza de datos (Función) ---
def limpiar_y_transformar(df):
    """
    Realiza la limpieza de datos: extrae dominio, selecciona,
    renombra y reordena columnas.
    """
    # 1. Asegurarse de que la columna 'Content URL' existe
    if 'Content URL' not in df.columns:
        st.error("Error: La columna 'Content URL' no se encontró en el archivo.")
        return None

    # 2. Extraer el dominio de la columna 'Content URL'
    df['Content URL'] = df['Content URL'].astype(str)
    df['Dominio'] = df['Content URL'].apply(
        lambda x: x.split('//')[-1].split('/')[0] if pd.notna(x) else None
    )

    # 3. Definir columnas y seleccionar las que existen
    columnas_base = ['Dominio', 'Domain Rating', 'Website Traffic']
    columnas_existentes = [col for col in columnas_base if col in df.columns]

    if len(columnas_existentes) < 3:
        columnas_faltantes = [col for col in columnas_base if col not in df.columns]
        st.warning(f"Advertencia: Faltan columnas clave: {', '.join(columnas_faltantes)}. Se continuará con las disponibles.")
        
    df_limpio = df[columnas_existentes].copy()

    # Renombrar 'Dominio' a 'Content URL'
    df_limpio = df_limpio.rename(columns={'Dominio': 'Content URL'})

    # 4. Asegurar las columnas 'Email' y 'WhatsApp' (añadirlas vacías si no existen)
    if 'Email' not in df_limpio.columns:
        df_limpio['Email'] = ''
    if 'WhatsApp' not in df_limpio.columns:
        df_limpio['WhatsApp'] = ''

    # 5. Reordenar las columnas al formato final deseado
    columnas_finales = ['Content URL', 'Domain Rating', 'Website Traffic', 'Email', 'WhatsApp']
    df_limpio = df_limpio[[col for col in columnas_finales if col in df_limpio.columns]]

    return df_limpio

# --- Interfaz de Streamlit (Principal) ---

st.title("🧹 Limpiador de Datos Excel/CSV")
st.markdown("Sube tu archivo para extraer el dominio de la URL, ordenar las columnas y añadir campos vacíos.")

# Widget para subir el archivo
uploaded_file = st.file_uploader(
    "Sube tu archivo Excel (.xlsx) o CSV (.csv)",
    type=['xlsx', 'csv']
)

if uploaded_file is not None: # <-- El procesamiento sólo ocurre si hay un archivo

    try:
        # Detectar el tipo de archivo y leer
        if uploaded_file.name.endswith('.csv'):
            df_original = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            # El uso de 'openpyxl' ya está implícito
            df_original = pd.read_excel(uploaded_file)
        else:
            st.error("Tipo de archivo no soportado. Por favor, sube un .xlsx o .csv.")
            st.stop()

        st.subheader("Datos Originales (Primeras 5 Filas)")
        st.dataframe(df_original.head())

        # Aplicar la limpieza
        df_limpio = limpiar_y_transformar(df_original) # <-- df_limpio se define aquí

        # --- A partir de aquí, df_limpio ya existe ---
        if df_limpio is not None:
            st.success("✅ Limpieza y transformación completada!")
            st.subheader("Datos Limpios")
            st.dataframe(df_limpio)

            # 1. Crear un buffer en memoria para guardar el archivo Excel
            output = io.BytesIO()
            
            # 2. Guardar el DataFrame limpio en el buffer como Excel
            # Usamos xlsxwriter para la escritura a Excel
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_limpio.to_excel(writer, index=False, sheet_name='Datos Limpios')
            
            # 3. Obtener los bytes del buffer para la descarga
            processed_data = output.getvalue()

            # 4. Botón para descargar el resultado como Excel
            st.download_button(
                label="📥 Descargar datos limpios (Excel .xlsx)",
                data=processed_data,
                file_name='datos_limpios.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
    except Exception as e:
        # Muestra el error, útil para depuración en Streamlit
        st.error(f"Ocurrió un error al procesar el archivo. Detalle: {e}")
