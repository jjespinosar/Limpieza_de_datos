# --- Interfaz de Streamlit (Sección de Descarga) ---
if df_limpio is not None:
    st.success("✅ Limpieza y transformación completada!")
    st.subheader("Datos Limpios")
    st.dataframe(df_limpio)

    # --- CAMBIO CLAVE AQUÍ ---
    # 1. Crear un buffer en memoria para guardar el archivo Excel
    output = io.BytesIO()
    
    # 2. Guardar el DataFrame limpio en el buffer como Excel
    # El motor 'xlsxwriter' es eficiente para esto
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # No incluimos el índice (index=False)
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
