# app.py
import streamlit as st
import pandas as pd
import io

# --- Lógica de limpieza de datos ---
def limpiar_y_transformar(df):
    """
    Realiza la limpieza de datos: extrae dominio, selecciona,
    renombra y reordena columnas.
    """
    # 1. Extraer el dominio de la columna 'Content URL'
    if 'Content URL' not in df.columns:
        st.error("Error: La columna 'Content URL' no se encontró en el archivo.")
        return None

    df['Content URL'] = df['Content URL'].astype(str)
    df['Dominio'] = df['Content URL'].apply(
        lambda x: x.split('//')[-1].split('/')[0] if pd.notna(x) else None
    )

    # 2. Definir columnas y seleccionar las que existen
    columnas_base = ['Dominio', 'Domain Rating', 'Website Traffic']
    columnas_existentes = [col for col in columnas_base if col in df.columns]

    if not columnas_existentes:
        st.error("Error: No se encontraron las columnas clave ('Domain Rating', 'Website Traffic').")
        return None

    df_limpio = df[columnas_existentes].copy()

    # Renombrar 'Dominio' a 'Content URL'
    df_limpio = df_limpio.rename(columns={'Dominio': 'Content URL'})

    # 3. Asegurar las columnas 'Email' y 'WhatsApp'
    if 'Email' not in df_limpio.columns:
        df_limpio['Email'] = ''
    if 'WhatsApp' not in df_limpio.columns:
        df_limpio['WhatsApp'] = ''

    # 4. Reordenar las columnas al formato final deseado
    columnas_finales = ['Content URL', 'Domain Rating', 'Website Traffic', 'Email', 'WhatsApp']
    df_limpio = df_limpio[[col for col in columnas_finales if col in df_limpio.columns]]

    return df_limpio

# --- Interfaz de Streamlit ---

st.title("🧹 Limpiador de Datos Excel/CSV")
st.markdown("Sube tu archivo para extraer el dominio de la URL y ordenar las columnas.")

# Widget para subir el archivo
uploaded_file = st.file_uploader(
    "Sube tu archivo Excel (.xlsx) o CSV (.csv)",
    type=['xlsx', 'csv']
)

if uploaded_file is not None:
    try:
        # Detectar el tipo de archivo y leer
        if uploaded_file.name.endswith('.csv'):
            df_original = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df_original = pd.read_excel(uploaded_file)
        else:
            st.error("Tipo de archivo no soportado. Por favor, sube un .xlsx o .csv.")
            st.stop()

        st.subheader("Datos Originales (Primeras 5 Filas)")
        st.dataframe(df_original.head())

        # Aplicar la limpieza
        df_limpio = limpiar_y_transformar(df_original)

        if df_limpio is not None:
            st.success("✅ Limpieza y transformación completada!")
            st.subheader("Datos Limpios")
            st.dataframe(df_limpio)

            # Botón para descargar el resultado
            csv_data = df_limpio.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Descargar datos limpios (CSV)",
                data=csv_data,
                file_name='datos_limpios.csv',
                mime='text/csv',
            )
            
    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {e}")
