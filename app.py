# app.py
import streamlit as st
import pandas as pd
import io
import xlsxwriter # Asegúrate de que esta línea esté, si la necesitas para la descarga en Excel

# --- Lógica de limpieza de datos (Función) ---
def limpiar_y_transformar(df):
    # ... (tu código de limpieza que retorna df_limpio o None)
    # ...
    return df_limpio # O None si hay error


# --- Interfaz de Streamlit (Principal) ---

st.title("🧹 Limpiador de Datos Excel/CSV")
# ... (más st.markdown)

uploaded_file = st.file_uploader(
    # ... (parámetros del uploader)
)

if uploaded_file is not None:  # <-- Bloque principal de ejecución

    try:
        # ... (código para leer el archivo df_original)
        
        # Aplicar la limpieza
        df_limpio = limpiar_y_transformar(df_original) # <-- AQUÍ SE DEFINE df_limpio

        # --- El código que usa df_limpio DEBE ir aquí dentro ---
        if df_limpio is not None:
            st.success("✅ Limpieza y transformación completada!")
            st.subheader("Datos Limpios")
            st.dataframe(df_limpio)

            # 1. Crear el buffer de descarga
            output = io.BytesIO()
            
            # 2. Guardar el DataFrame en el buffer como Excel
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_limpio.to_excel(writer, index=False, sheet_name='Datos Limpios')
            
            # 3. Obtener los bytes
            processed_data = output.getvalue()

            # 4. Botón de descarga
            st.download_button(
                label="📥 Descargar datos limpios (Excel .xlsx)",
                data=processed_data,
                file_name='datos_limpios.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {e}")

# --- ¡Nada de código que use df_limpio debe estar aquí abajo! ---
