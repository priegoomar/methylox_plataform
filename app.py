with tab_ingenieria:
    st.markdown('⚙️ Consola Ingenieria')
    h_param = []
    h_param.append("UMBRAL_CRITICO_DB")
    h_param.append("BACKGROUND_NOISE_PURGE")
    h_param.append("DATA_PERSISTENCE")
    h_val = []
    h_val.append("0.5910 ng/mL")
    h_val.append("BCAS3 Excluded")
    h_val.append("SQLite3 Relational")
    df_b = pd.DataFrame()
    df_b['Hyperparameter'] = h_param
    df_b['Value'] = h_val
    st.dataframe(df_b)
    
    st.markdown('### 🧪 Matriz Analitica DoE')
    corridas = []
    corridas.append("1")
    corridas.append("2")
    corridas.append("3")
    corridas.append("4")
    corridas.append("5")
    corridas.append("6")
    corridas.append("7")
    corridas.append("8")
    f_temp = []
    f_temp.append("55C")
    f_temp.append("62C")
    f_temp.append("55C")
    f_temp.append("62C")
    f_temp.append("55C")
    f_temp.append("62C")
    f_temp.append("55C")
    f_temp.append("62C")
    f_enz = []
    f_enz.append("0.5")
    f_enz.append("0.5")
    f_enz.append("2.0")
    f_enz.append("2.0")
    f_enz.append("0.5")
    f_enz.append("0.5")
    f_enz.append("2.0")
    f_enz.append("2.0")
    f_tie = []
    f_tie.append("60m")
    f_tie.append("60m")
    f_tie.append("60m")
    f_tie.append("60m")
    f_tie.append("180")
    f_tie.append("180")
    f_tie.append("180")
    f_tie.append("180")
    f_cod = []
    f_cod.append("(1)")
    f_cod.append("a")
    f_cod.append("b")
    f_cod.append("ab")
    f_cod.append("c")
    f_cod.append("ac")
    f_cod.append("bc")
    f_cod.append("abc")
    df_doe = pd.DataFrame()
    df_doe['Corrida'] = corridas
    df_doe['Temp'] = f_temp
    df_doe['Enzima'] = f_enz
    df_doe['Tiempo'] = f_tie
    df_doe['Codigo'] = f_cod
    st.dataframe(df_doe)
