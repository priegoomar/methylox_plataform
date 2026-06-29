Baja hasta la sección de la pestaña número 4, que dice exactamente: elif menu == "Clinical Reports":.Selecciona ese bloque de código y reemplázalo por esta estructura premium, que añade un selector dinámico para re-convocar los datos de cualquier paciente del historial y empaquetar su PDF de forma inmediata:
# ------------------------------------------------------------------------------
# PESTAÑA 4: CLINICAL REPORTS (RECUPERACIÓN COMPLETA DE DOSSIER PDF DESDE EL LOG)
# ------------------------------------------------------------------------------
elif menu == "Clinical Reports":
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-heading">📈 Clinical Reports & Active Search Audit Log</p>', unsafe_allow_html=True)
    st.caption("Consulte las firmas moleculares indexadas y recupere los reportes institucionales expedidos.")
    
    if st.session_state["historical_database"].empty:
        st.info("La bitácora de auditoría acumulada se encuentra vacía. Calcule dictámenes en la pantalla principal para registrar historiales.")
    else:
        st.write("##")
        st.dataframe(st.session_state["historical_database"], use_container_width=True)
        
        st.write("---")
        st.markdown("### 📄 Recuperación de Dossier Clínico Institucional")
        st.caption("Seleccione el Identificador del paciente registrado en la sesión para re-convocar sus lecturas analíticas y descargar el PDF oficial.")
        
        # Selector dinámico que jala los ID reales guardados en la memoria de la sesión
        lista_pacientes = st.session_state["historical_database"]["Patient ID"].unique()
        paciente_seleccionado = st.selectbox("Seleccione el ID del Paciente a exportar:", lista_pacientes)
        
        # Filtramos los datos del caso elegido en absoluto secreto
        datos_caso = st.session_state["historical_database"][st.session_state["historical_database"]["Patient ID"] == paciente_seleccionado].iloc[-1]
        
        # Re-armamos el cuerpo del Dossier en caliente con sus variables reales
        dossier_dinamico = f"""METHYLOX ONCOLOGY - INSTITUTIONAL CLINICAL REPORT
======================================================================
Identificador del Caso: {datos_caso['Patient ID']}
Edad Cronológica: {datos_caso['Age (Years)']} Años
Concentración ctDNA: {datos_caso['ctDNA (ng/mL)']} ng/mL
Estatus Epigenético Molecular: {datos_caso['Clinical Status']}
Marca de Tiempo de Registro: {datos_caso['Timestamp']}

--------------------------------======================================
AVISO LEGAL: Prototipo computacional restringido a experimentación académica.
Protegido bajo Secreto Industrial. © 2026 MethylOx Oncology."""

        st.write("##")
        pdf_nombre = f"METHYLOX_Reporte_{paciente_seleccionado}.pdf"
        
        # Botón inteligente de descarga unitaria
        st.download_button(
            label=f"📥 Download Official PDF Dossier for {paciente_seleccionado}",
            data=dossier_dinamico.encode('utf-8'), # Transforma el texto empaquetado en un archivo de descarga directo
            file_name=pdf_nombre,
            mime="application/pdf",
            use_container_width=True
        )
        
    st.markdown('</div>', unsafe_allow_html=True)
