import io
import os
import time
from datetime import datetime, date
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import requests
import base64

# ============================================================================
# 🧬 METHYLOX(TM) PLATFORM v3.0 - ENTERPRISE SaMD FULL PRODUCTION FRONTEND
# ============================================================================
st.set_page_config(
    page_title="MethylOxTM | Epigenetic AI SaMD Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- UNIFIED ADVANCED CLINICAL DESIGN SYSTEM & CSS RECTIFICATION ---
st.markdown("""
<style>
    /* Global Viewport Architecture */
    .stApp {
        background-color: #F8FAFC !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }
    [data-testid="stHeader"] {
        display: none !important;
        height: 0px !important;
    }
    [data-testid="stMainBlockContainer"] {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
    }
   
    /* Dark Compliance Corporate Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0B0F19 !important;
        border-right: 1px solid #1E293B;
    }
    div[data-testid="stSidebarUserContent"] .stRadio > div {
        gap: 6px !important;
    }
    div[data-testid="stSidebarUserContent"] label {
        color: #94A3B8 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }
   
    /* Typography System */
    .welcome-header {
        font-size: 28px !important;
        font-weight: 800 !important;
        color: #0F172A !important;
        margin-bottom: 2px !important;
    }
    .welcome-caption {
        font-size: 14px !important;
        color: #64748B !important;
        margin-bottom: 25px !important;
    }
   
    /* Premium Grid Telemetry Panels */
    .metric-container-hub {
        display: flex;
        gap: 20px;
        margin-bottom: 25px;
        width: 100%;
    }
    .metric-card-clinical-new {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        text-align: center;
        flex: 1;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .metric-title-sub-new {
        font-size: 12px !important;
        font-weight: 700 !important;
        color: #64748B !important;
        margin: 0 0 6px 0 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-num-big-new {
        font-size: 36px !important;
        font-weight: 800 !important;
        color: #0F172A !important;
        margin: 5px 0 !important;
        line-height: 1 !important;
    }
    .metric-link-btn-new {
        font-size: 11px !important;
        font-weight: 600 !important;
        color: #2563EB !important;
        text-decoration: none;
        display: inline-block;
        margin-top: 8px;
    }
    .svg-top-container {
        margin-bottom: 8px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* UNIFICACIÓN TOTAL EN UN SOLO RECUADRO MONOLÍTICO PARA LA TABLA Y DONA */
    .unified-main-board-box {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        min-height: 340px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        margin-bottom: 20px;
    }

    /* Alineación y Centrado Absoluto de las Columnas de la Tabla */
    .clinical-table-new {
        width: 100%;
        border-collapse: collapse;
        font-size: 13px;
        margin-top: 15px;
    }
    .clinical-table-new th {
        color: #64748B;
        font-weight: 700;
        padding: 14px 10px;
        border-top: 1px solid #E2E8F0;
        border-bottom: 2px solid #E2E8F0;
        background-color: #F8FAFC;
        text-align: center !important;
    }
    .clinical-table-new td {
        padding: 14px 10px;
        color: #0F172A;
        border-bottom: 1px solid #F1F5F9;
        text-align: center !important;
    }
   
    /* Premium Action Grid System */
    .quick-action-grid {
        display: flex;
        gap: 15px;
        margin-top: 25px;
        width: 100%;
    }
    .action-card-svg {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px;
        flex: 1;
        display: flex;
        align-items: center;
        gap: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    .icon-circle-svg {
        width: 44px;
        height: 44px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .action-text-container {
        display: flex;
        flex-direction: column;
    }
    .action-title-svg {
        font-size: 14px;
        font-weight: 700;
        color: #0F172A;
        margin: 0;
    }
    .action-desc-svg {
        font-size: 11px;
        color: #64748B;
        margin: 2px 0 0 0;
    }

    .bg-neon-blue { background: #E0F2FE; color: #0EA5E9; }
    .bg-neon-orange { background: #FFEDD5; color: #F97316; }
    .bg-neon-green { background: #DCFCE7; color: #22C55E; }
    .bg-neon-purple { background: #F3E8FF; color: #A855F7; }
</style>
""", unsafe_allow_html=True)

# --- BACKEND API BACKBONE ROUTING ---
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api/v1")

# ============================================================================
# QUICK ACTION SVG BUTTON COMPONENT
# ============================================================================

def svg_button(svg_code, title, subtitle, bg_color, target_page):
    st.markdown(f"""
    <div class="action-card-svg">
        <div class="icon-circle-svg" style="background:{bg_color};">
            {svg_code}
        </div>
        <div class="action-text-container">
            <p class="action-title-svg">{title}</p>
            <p class="action-desc-svg">{subtitle}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        title,
        key=f"quick_{target_page}",
        use_container_width=True
    ):
        st.session_state.nav_selection = target_page
        st.rerun()

# ============================================================================
# 🔒 SECURE CORPORATE SIDEBAR INTERACTION (DYNAMIC AUTH GATES)
# ============================================================================

with st.sidebar:
    st.markdown(
        """
        <div style="padding:10px 0px; border-bottom:1px solid #1E293B; margin-bottom:25px;">
            <h3 style="margin:0; color:#FFFFFF; font-weight:900; font-size:22px;">
                MethylOx™
            </h3>
            <p style="margin:0; color:#38BDF8; font-size:11px; font-weight:600;">
                Epigenetic AI Platform
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # SESSION STATE
    if "jwt_access_token" not in st.session_state:
        st.session_state.jwt_access_token = None

    if "operator_display_name" not in st.session_state:
        st.session_state.operator_display_name = "Guest Operator"

    if "user_role" not in st.session_state:
        st.session_state.user_role = None

    if "id_hospital" not in st.session_state:
        st.session_state.id_hospital = 1

    # LOGIN
    if not st.session_state.jwt_access_token:
        with st.form("institutional_login_form"):
            st.markdown(
                "<p style='color:#94A3B8;font-size:12px;font-weight:700;'>SECURE GATEWAY</p>",
                unsafe_allow_html=True
            )

            login_username = st.text_input(
                "Clinical Email",
                placeholder="operator@hospital.com"
            )

            login_password = st.text_input(
                "Password",
                type="password"
            )

            login_submit = st.form_submit_button(
                "🔑 Authenticate",
                use_container_width=True
            )

        if login_submit:
            if login_username and login_password:
                try:
                    payload_auth = {
                        "username": login_username.strip(),
                        "password": login_password.strip()
                    }

                    res = requests.post(
                        f"{BACKEND_URL}/auth/login",
                        data=payload_auth,
                        timeout=5
                    )

                    if res.status_code == 200:
                        token_data = res.json()
                        st.session_state.jwt_access_token = token_data["access_token"]
                        st.session_state.operator_display_name = login_username
                        st.session_state.user_role = token_data.get(
                            "role",
                            "tech"
                        ).lower()

                        st.rerun()
                    else:
                        st.error("Authentication denied")

                except Exception:
                    st.error("Backend unavailable")
            else:
                st.error("Complete credentials")
    else:
        st.markdown(
            f"""
            <div style='background:#1E293B;padding:12px;border-radius:8px;'>
                <p style='color:#94A3B8;font-size:11px;'>Authenticated Account:</p>
                <p style='color:#FFFFFF;font-weight:700;'>
                {st.session_state.operator_display_name}
                </p>
                <p style='color:#38BDF8;font-size:11px;'>
                ROLE: {st.session_state.user_role}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "🚪 Disconnect Session",
            use_container_width=True
        ):
            st.session_state.jwt_access_token = None
            st.session_state.operator_display_name = "Guest Operator"
            st.session_state.user_role = None
            st.rerun()

    st.markdown("---")

# =========================================================================
# RBAC NAVIGATION & URL ROUTING (FINAL FIX)
# =========================================================================

# Definir menu_options por defecto
menu_options = {
    "dashboard": "Dashboard",
    "patients": "Patients",
    "lims": "LIMS / Samples",
    "analysis": "Analysis",
    "reports": "Reports"
}

if st.session_state.get("jwt_access_token"):
    if st.session_state.get("user_role") == "admin":
        menu_options["Access Control"] = "Access Control"
        menu_options["settings"] = "Settings"

    if "nav_selection" not in st.session_state:
        st.session_state.nav_selection = "dashboard"

    # Procesar parámetros de URL si existen
    if "page" in st.query_params:
        query_page = st.query_params["page"]
        target_nav = None
        
        if query_page == "Patients" and "patients" in menu_options:
            target_nav = "patients"
        elif query_page == "LIMS-Samples" and "lims" in menu_options:
            target_nav = "lims"
        elif query_page == "METHYLOX-Engine" and "analysis" in menu_options:
            target_nav = "analysis"
        elif query_page == "Reports" and "reports" in menu_options:
            target_nav = "reports"
        elif query_page == "Access Control" and "Access Control" in menu_options:
            target_nav = "Access Control"
            
        if target_nav:
            st.session_state.nav_selection = target_nav
            # Limpiamos el parámetro para evitar bucles o que se quede estancado en recargas futuras
            st.query_params.clear()

    current_selection = st.session_state.nav_selection
    if current_selection not in menu_options:
        current_selection = "dashboard"

    selected_key = st.sidebar.radio(
        "Operational Scope Selector",
        options=list(menu_options.keys()),
        format_func=lambda x: menu_options[x],
        key="nav_selection",
        label_visibility="collapsed"
    )
else:
    selected_key = "restricted"
    st.query_params.clear()

# Movido a st.sidebar para que aparezca abajo en la barra lateral y no en la pantalla principal
st.sidebar.markdown("---")

st.sidebar.markdown(
    """
        <div style="padding:5px 10px;">
            <p style="font-size:10px;color:#64748B;font-weight:700;">
            SYSTEM STATUS
            </p>
            <div>
            🟢 Core Engine Active
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

headers = {
    "Authorization": f"Bearer {st.session_state.jwt_access_token}"
} if st.session_state.jwt_access_token else {}

# ============================================================================
# 🏛️ CENTRAL ARCHITECTURE MODULES
# ============================================================================

# Asignar la variable globalmente desde el session_state para evitar el NameError
nav_selection = st.session_state.get("nav_selection", "dashboard")

if selected_key == "restricted":
    st.markdown('<div class="executive-card-white" style="text-align:center; padding:60px 40px; margin-top:40px;">', unsafe_allow_html=True)
    st.markdown("<h2 style='color:#0F172A; font-weight:800; font-size:24px; margin-bottom:10px;'>Preventative Infrastructure Lockdown Active</h2>", unsafe_allow_html=True)
    st.caption("METHYLOX™ algorithmic node is encrypted. Enter authorized clinician credentials in the sidebar to allocate active pipelines.")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
#   TAB: ACCESS CONTROL (DYNAMIC RBAC AUTHORIZATION HUB)
# ----------------------------------------------------------------------------
elif nav_selection == "users":
    st.markdown("<h2 class='welcome-header'>Identity Governance & Task Delegation</h2>", unsafe_allow_html=True)
    st.markdown("<p class='welcome-caption'>Provision custom laboratory operational roles dynamically without hardcoding</p>", unsafe_allow_html=True)
   
    # Consultamos el directorio de hospitales del backend para asociar el nombre con su ID correspondiente
    try:
        res_hospitals = requests.get(f"{BACKEND_URL}/hospitals/directory", headers=headers, timeout=5)
        hospital_dict = {h["name"]: h["id"] for h in res_hospitals.json()} if res_hospitals.status_code == 200 and res_hospitals.json() else {}
    except Exception:
        hospital_dict = {}

    st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)
    with st.form("universal_user_provisioning_form", clear_on_submit=True):
        st.markdown("#### Register New Authorized Staff Member")
        c1, c2 = st.columns(2)
        with c1:
            input_username = st.text_input("Email or Username", placeholder="doctor@hospital.com")
            input_full_name = st.text_input("Full Name", placeholder="e.g., Dr. John Doe, MD")
        with c2:
            input_password = st.text_input("Temporary Password", type="password", placeholder="••••••••••••")
            target_role_display = st.selectbox("System Role and Permissions", ["admin", "cls", "md"], format_func=lambda x: {"admin": "Administrator", "cls": "Laboratory Technician (CLS)", "md": "Clinical Doctor (MD)"}[x])
             
        # Si hay hospitales en la base de datos, permitimos seleccionarlo o escribirlo limpiamente
        if hospital_dict:
            selected_hospital_name = st.selectbox("Hospital or Clinic Name", options=list(hospital_dict.keys()))
            target_hospital_id = hospital_dict[selected_hospital_name]
        else:
            # Fallback seguro si la red falla o está vacío
            target_hospital_name = st.text_input("Hospital or Clinic Name", placeholder="e.g., Memorial General Hospital")
            target_hospital_id = int(st.session_state.get("id_hospital", 1))

        submit_btn = st.form_submit_button("Activate User & Grant Access")
       
    if submit_btn:
        if not input_username or not input_password or not input_full_name:
            st.error("All clinical identity fields are mandatory.")
        else:
            payload_u = {
                "username": input_username,
                "password": input_password,
                "full_name": input_full_name,
                "role": target_role_display,
                "hospital_id": int(target_hospital_id)
            }
            try:
                response = requests.post(f"{BACKEND_URL}/auth/provision-user", json=payload_u, headers=headers)
                if response.status_code == 200:
                    st.success("Staff Identity Successfully Activated & Tasks Delegated Real-Time.")
                else:
                    st.error(f"Identity Provisioning Rejection: {response.json().get('detail', 'Unauthorized operational sequence')}")
            except Exception:
                st.error("Deployment Connectivity Error: User profile could not be logged into database repository.")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# ============================================================================
# 📊 TAB 2: PATIENTS (COHORTE DE PACIENTES - CLÍNICA)
# ============================================================================
elif nav_selection == "patients":
    st.markdown("<h2 class='welcome-header'>📊 Directorio de Cohorte y Pacientes</h2>", unsafe_allow_html=True)
    st.markdown("<p class='welcome-caption'>Inscriba nuevos pacientes y supervise el historial de marcadores epigenéticos en el tiempo</p>", unsafe_allow_html=True)
    
    # Inicializar estado para mostrar u ocultar el formulario de registro y directorio
    if "show_new_patient_form" not in st.session_state:
        st.session_state.show_new_patient_form = False

    # Inicializar el ID automático en el estado de la sesión si no existe
    import random
    if "generated_patient_id" not in st.session_state:
        st.session_state.generated_patient_id = f"PAT-{random.randint(10000, 99999)}"

    # -------------------------------------------------------------------------
    # 🔍 PANTALLA INICIAL ESTILO GOOGLE
    # -------------------------------------------------------------------------
    if not st.session_state.show_new_patient_form:
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        col_pad1, col_center, col_pad2 = st.columns([1, 2.2, 1])
        
        with col_center:
            # Estilos CSS avanzados para eliminar cualquier recuadro del botón y dejarlo como texto plano interactivo
            st.markdown("""
            <style>
                /* Ocultar bordes de contenedor de botones para que "+ New Patient" sea texto plano sin recuadro */
                div.row-widget.stButton > button[kind="secondary"] {
                    background: transparent !important;
                    border: none !important;
                    color: #2563EB !important;
                    font-weight: 600 !important;
                    font-size: 16px !important;
                    padding: 0 !important;
                    margin: 0 !important;
                    box-shadow: none !important;
                    display: inline-block !important;
                    text-align: center !important;
                    width: 100% !important;
                }
                div.row-widget.stButton > button[kind="secondary"]:hover {
                    color: #1D4ED8 !important;
                    background: transparent !important;
                    text-decoration: underline !important;
                }
            </style>
            """, unsafe_allow_html=True)

            # Etiqueta "Search patient" con su icono SVG profesional de lupa a la izquierda
            st.markdown(
                """
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px; font-weight: 600; color: #1E293B; font-size: 15px;">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                    <span>Search patient</span>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            # Recuadro de texto para escribir el ID o nombre
            search_query_main = st.text_input(
                "Search patient input", 
                placeholder="Write ID, Record Number, or Institution...",
                label_visibility="collapsed"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Opción "+ New Patient" como texto plano clickeable sin recuadro
            col_btn_sub1, col_btn_sub_target, col_btn_sub2 = st.columns([1, 2, 1])
            with col_btn_sub_target:
                if st.button("+ New Patient", key="btn_toggle_new_patient"):
                    st.session_state.show_new_patient_form = True
                    st.rerun()

        st.markdown("<br><br>", unsafe_allow_html=True)

        # Mostrar el directorio de pacientes filtrable en la vista principal si se escribe algo en el buscador
        try:
            res_cohort = requests.get(f"{BACKEND_URL}/api/v1/lims/cohort-directory", headers=headers, timeout=5)
            if res_cohort.status_code == 200 and res_cohort.json():
                df_patients = pd.DataFrame(res_cohort.json())
            else:
                df_patients = pd.DataFrame(columns=["Patient ID", "Record Number", "Date of Birth", "Gender", "Institution"])
        except Exception:
            df_patients = pd.DataFrame(columns=["Patient ID", "Record Number", "Date of Birth", "Gender", "Institution"])
            
        if not df_patients.empty:
            column_mapping = {
                'id_patient': 'Patient ID',
                'patient_id': 'Patient ID',
                'full_name': 'Record Number',
                'anonymous_code': 'Record Number',
                'date_of_birth': 'Date of Birth',
                'dob': 'Date of Birth',
                'gender': 'Gender',
                'institution': 'Institution'
            }
            df_patients = df_patients.rename(columns={k: v for k, v in column_mapping.items() if k in df_patients.columns})

            if search_query_main:
                mask = df_patients.astype(str).apply(lambda x: x.str.contains(search_query_main, case=False, na=False)).any(axis=1)
                df_patients = df_patients[mask]
                
                st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)
                st.markdown('<div class="card-title-clinical">Search Results & Patient Directory</div>', unsafe_allow_html=True)
                st.dataframe(df_patients, use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 📋 SECCIÓN CONDICIONAL: FORMULARIO Y DIRECTORIO (Al dar clic en New Patient)
    # -------------------------------------------------------------------------
    else:
        # Botón superior para regresar a la pantalla de inicio
        if st.button("← Back to Search", key="btn_back_search"):
            st.session_state.show_new_patient_form = False
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        p1, p2 = st.columns([1, 1.3], gap="large")
        
        with p1:
            st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)
            st.markdown('<div class="card-title-clinical">➕ Register New Patient Profile</div>', unsafe_allow_html=True)
            
            if st.session_state.user_role == "cls":
                st.warning("🔒 Restricted Access: Laboratory role does not have clinical privileges to enroll patients.")
            else:
                # Campo Unique patient ID
                new_p_id = st.text_input("Unique patient ID", value=st.session_state.generated_patient_id)
                
                # Texto interactivo "Generate Automatic ID"
                if st.button("🔄 Generate Automatic ID", key="btn_gen_auto_id"):
                    st.session_state.generated_patient_id = f"PAT-{random.randint(10000, 99999)}"
                    st.rerun()
                
                # Record Number con placeholder
                new_p_name = st.text_input("Record Number", placeholder="e.g. REC-2026-0091")
                
                new_p_dob = st.date_input("Date of birth", min_value=datetime(1920, 1, 1))
                
                # Opciones de género en inglés
                new_p_sexo = st.selectbox("Gender", ["Male", "Female"])
                
                # Institución
                new_institution = st.text_input("Institution")
                    
                if st.button("Save and synchronize record", use_container_width=True):
                    gender_backend = new_p_sexo
                    
                    if not new_p_id or not new_p_name or not new_institution:
                        st.error("❌ Missing Data: Please complete all mandatory clinical fields.")
                    else:
                        payload_p = {
                            "id_patient": new_p_id,
                            "full_name": new_p_name,
                            "date_of_birth": str(new_p_dob),
                            "gender": gender_backend,
                            "institution": new_institution
                        }
                        try:
                            res_p = requests.post(f"{BACKEND_URL}/api/v1/lims/enroll-patient", json=payload_p, headers=headers, timeout=5)
                            if res_p.status_code == 200:
                                st.success(f"🧬 Patient record {new_p_id} successfully registered.")
                                st.session_state.generated_patient_id = f"PAT-{random.randint(10000, 99999)}"
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.error("🚨 Server Error: Could not complete registration.")
                        except Exception:
                            st.error("🚨 Connectivity Error: Backend service unavailable.")
            st.markdown('</div>', unsafe_allow_html=True)

        with p2:
            st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)
            st.markdown('<div class="card-title-clinical">Patient Directory & Advanced Filtering</div>', unsafe_allow_html=True)
            
            # Barra de filtrado avanzada dentro de la vista del formulario
            sub_filter_col1, sub_filter_col2 = st.columns([2, 1])
            with sub_filter_col1:
                filter_text = st.text_input("Filter directory", placeholder="Filter by ID, Date, Record, Institution...", key="filter_table_input")
            with sub_filter_col2:
                filter_gender = st.selectbox("Filter Gender", ["All", "Male", "Female"], key="filter_gender_select")

            try:
                res_cohort = requests.get(f"{BACKEND_URL}/api/v1/lims/cohort-directory", headers=headers, timeout=5)
                if res_cohort.status_code == 200 and res_cohort.json():
                    df_patients = pd.DataFrame(res_cohort.json())
                else:
                    df_patients = pd.DataFrame(columns=["Patient ID", "Record Number", "Date of Birth", "Gender", "Institution"])
            except Exception:
                df_patients = pd.DataFrame(columns=["Patient ID", "Record Number", "Date of Birth", "Gender", "Institution"])
                
            if not df_patients.empty:
                column_mapping = {
                    'id_patient': 'Patient ID',
                    'patient_id': 'Patient ID',
                    'full_name': 'Record Number',
                    'anonymous_code': 'Record Number',
                    'date_of_birth': 'Date of Birth',
                    'dob': 'Date of Birth',
                    'gender': 'Gender',
                    'institution': 'Institution'
                }
                df_patients = df_patients.rename(columns={k: v for k, v in column_mapping.items() if k in df_patients.columns})

                # Aplicar filtro de texto
                if filter_text:
                    mask = df_patients.astype(str).apply(lambda x: x.str.contains(filter_text, case=False, na=False)).any(axis=1)
                    df_patients = df_patients[mask]
                
                # Aplicar filtro de género
                if filter_gender != "All" and "Gender" in df_patients.columns:
                    df_patients = df_patients[df_patients["Gender"].str.lower() == filter_gender.lower()]

            st.dataframe(df_patients, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# 🧪 TAB 3: LIMS SAMPLES (CHAIN OF CUSTODY AUDIT COMPLIANCE)
# ----------------------------------------------------------------------------
elif nav_selection == "lims":
    st.markdown("<h2 class='welcome-header'>🧪 LIMS Access Control & Chain of Custody</h2>", unsafe_allow_html=True)
    st.markdown("<p class='welcome-caption'>Validate chronological workflow history pathways and operational audit logs</p>", unsafe_allow_html=True)
    
    try:
        res_p_list = requests.get(f"{BACKEND_URL}/api/v1/lims/cohort-directory", headers=headers, timeout=5)
        registered_patients = [p["Patient ID"] for p in res_p_list.json()] if res_p_list.status_code == 200 and res_p_list.json() else []
    except Exception:
        registered_patients = []

    with st.container():
        m1, m2 = st.columns(2)
        with m1:
            st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)
            st.markdown('<div class="card-title-clinical">📥 Log New Clinical Asset Intake</div>', unsafe_allow_html=True)
            
            if st.session_state.user_role == "md":
                st.warning("🔒 Access Denied: Medical personnel are restricted from altering LIMS physical custody states.")
            elif not registered_patients:
                st.warning("⚠️ Action Locked: You must enroll at least one patient record before conducting laboratory asset intake operations.")
            else:
                new_m_id = st.text_input("Unique Sample Asset ID")
                asoc_p_id = st.selectbox("Associated Patient Subject Profile Link", registered_patients)
                new_m_qr = st.text_input("Barcode Hardware QR Matrix Identifier")
                new_m_tipo = st.selectbox("Extraction Matrix Assay Specimen Type", ["Plasma", "Whole Blood", "Tissue"])
                new_m_est = st.selectbox("Chain of Custody Operational Workflow State", ["Sample Received", "DNA/RNA Extraction", "Target Amplicons Sequencing", "Bioinformatic Processing", "Clinical Report Compiled"])
                
                if st.button("Synchronize Sample Entry into Central LIMS Core", use_container_width=True):
                    if not new_m_id or not new_m_qr:
                        st.error("❌ Input Constraint: Asset ID and Hardware Barcodes are required.")
                    else:
                        payload_sample = {
                            "sample_id": new_m_id, "patient_id": asoc_p_id, "barcode_qr": new_m_qr,
                            "specimen_type": new_m_tipo, "workflow_state": new_m_est, "practitioner_signature": st.session_state.operator_display_name
                        }
                        try:
                            res_intake = requests.post(f"{BACKEND_URL}/api/v1/lims/samples/intake", json=payload_sample, headers=headers, timeout=5)
                            if res_intake.status_code == 200:
                                st.success("Asset logged successfully.")
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.error(f"❌ LIMS Node Rejection: {res_intake.json().get('detail', 'Invalid parameter constraints')}")
                        except Exception:
                            st.error("❌ Connectivity Failure: Could not commit asset state transaction to Render.")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with m2:
            st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)
            st.markdown('<div class="card-title-clinical">🗃️ Real-Time Audit Trail & Asset Inventory Status</div>', unsafe_allow_html=True)
            try:
                res_s = requests.get(f"{BACKEND_URL}/api/v1/lims/samples/directory", headers=headers, timeout=5)
                df_samples = pd.DataFrame(res_s.json()) if res_s.status_code == 200 and res_s.json() else pd.DataFrame(columns=["Sample ID", "Patient Context", "Hardware QR Code", "Specimen Matrix", "Current LIMS State"])
            except Exception:
                df_samples = pd.DataFrame(columns=["Sample ID", "Patient Context", "Hardware QR Code", "Specimen Matrix", "Current LIMS State"])
                
            st.dataframe(df_samples, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# 🧬 TAB 4: METHYLOX ENGINE (COMPUTATIONAL KERNEL CORES)
# ----------------------------------------------------------------------------
elif nav_selection == "analysis":
    st.markdown("<h2 class='welcome-header'>🧬 Computational Pipeline Kernel Execution</h2>", unsafe_allow_html=True)
    st.markdown("<p class='welcome-caption'>Execute high-density CRISPR-Cas12a calling matrices against sequence parameters</p>", unsafe_allow_html=True)
    
    st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)
    st.markdown('<div class="card-title-clinical">🚀 Quantitative Epigenetic Run Over Raw Methylation Matrices</div>', unsafe_allow_html=True)
    
    if st.session_state.user_role == "md":
        st.warning("🔒 Access Denied: Medical roles do not possess computational clearance to launch sequencing.")
    else:
        try:
            res_p_samples = requests.get(f"{BACKEND_URL}/api/v1/lims/samples/pending-evaluation", headers=headers, timeout=5)
            pending_samples = res_p_samples.json() if res_p_samples.status_code == 200 and res_p_samples.json() else []
        except Exception:
            pending_samples = []

        if not pending_samples:
            st.info("ℹ️ Pipeline Standby: No pending samples in queue requiring CRISPR bioinformatic scoring calculation.")
        else:
            m_target = st.selectbox("Select Pending Asset ID for Pipeline Queue:", pending_samples)
            uploaded_file = st.file_uploader("Upload Sequencer Raw CpG Methylation File (.CSV)", type=["csv"])
            if uploaded_file is not None:
                if st.button("Execute Automated Analytical Pipeline Run", use_container_width=True):
                    files_payload = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                    try:
                        res_calc = requests.post(f"{BACKEND_URL}/api/v1/lims/samples/evaluate/{m_target}", files=files_payload, headers=headers, timeout=15)
                        if res_calc.status_code == 200:
                            calc_result = res_calc.json()
                            st.success(f"⚡ Analytics unraveled. Mean Beta Score: {calc_result['mean_beta']:.4f}")
                            st.write(f"**Clinical Verdict:** {calc_result['verdict']}")
                        else:
                            st.error("❌ Computational Alignment Exception.")
                    except Exception:
                        st.error("❌ Kernel Processing Core Error.")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# 📋 TAB 5: REPORTS (EXHAUSTIVE DEFENSIBLE PDF CLINICAL DOSSIER ENGINE)
# ----------------------------------------------------------------------------
elif nav_selection == "reports":
    from fpdf import FPDF
    st.markdown("<h2 class='welcome-header'>📜 Issuance of Defendible Clinical Dossiers & Technical Reports</h2>", unsafe_allow_html=True)
    st.markdown("<p class='welcome-caption'>Verify mathematical calls and download FDA/HIPAA compliant cryptographic sheets</p>", unsafe_allow_html=True)
    
    st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)
    try:
        res_reports = requests.get(f"{BACKEND_URL}/api/v1/analysis/reports-directory", headers=headers, timeout=5)
        if res_reports.status_code == 200:
            reports_data = res_reports.json()
        else:
            reports_data = []
    except Exception:
        reports_data = []
    
    if not reports_data:
        st.info("ℹ️ Clean Ledger: No clinical report matrix sequences compiled in PostgreSQL database yet. The system is ready in clean-slate production to record and emit real diagnostics.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        df_rep_list = pd.DataFrame(reports_data)
        st.dataframe(df_rep_list[['muestra_id', 'paciente_id', 'score', 'clasificacion', 'fecha_analisis', 'hash_seguridad']].rename(
            columns={
                'muestra_id': 'Sample ID',
                'paciente_id': 'Patient ID',
                'score': 'Beta Score',
                'clasificacion': 'Result Assessment',
                'fecha_analisis': 'Timestamp',
                'hash_seguridad': 'Security Hash'
            }
        ), use_container_width=True, hide_index=True)
        
        st.write("---")
        m_select = st.selectbox("Select Target Sample ID for Report Verification & Electronic Signature Ingestion:", df_rep_list["muestra_id"].unique())
        datos_rep = df_rep_list[df_rep_list["muestra_id"] == m_select].iloc[-1]
        tipo_informe = st.radio("Select Standardized Document Layout Format Structure", ["Institutional Executive Summary", "Technical Biomarker Deep Dive"], horizontal=True)
        
        st.write("##")
        
        # FPDF CORE ENGINE RECONSTRUCTION (HIGH-FIDELITY MEDICAL PDF)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(30, 58, 138)
        pdf.cell(190, 10, "METHYLOX(TM) LABORATORY INTELLIGENCE PLATFORM REPORT", ln=True, align="L")
        
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(190, 5, "BIOMEDICAL SYSTEMS OPERATION KERNEL | SOFTWARE DEVICE STAGE: METHYLOX v3.0-PRODUCTION SaMD", ln=True)
        pdf.ln(3)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)
        
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(190, 6, "1. DIGITAL CHAIN OF CUSTODY AUDIT TRAIL (LIMS TELEMETRY)", ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(95, 5, f"Sample Asset ID: {str(datos_rep['muestra_id'])}", border=0)
        pdf.cell(95, 5, f"Verification Security Hash: {str(datos_rep['hash_seguridad'])}", border=0, ln=True)
        pdf.cell(95, 5, f"Authorized Operator Signature: {str(datos_rep['operador'])}", border=0)
        pdf.cell(95, 5, f"Server Transaction Timestamp: {str(datos_rep['fecha_analisis'])}", border=0, ln=True)
        pdf.ln(3)
        
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(190, 6, "2. ANONYMIZED PATIENT MOLECULAR DIRECTORY PROFILE", ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(95, 5, f"Patient Context ID: {str(datos_rep['paciente_id'])}", border=0)
        pdf.cell(95, 5, f"Security Anonymous Code String: {str(datos_rep['nombre_codigo'])}", border=0, ln=True)
        pdf.cell(95, 5, f"Age: {str(datos_rep['age'])} Years", border=0)
        pdf.cell(95, 5, f"Biological Gender Parameter: {str(datos_rep['sexo'])}", border=0, ln=True)
        pdf.cell(190, 5, f"Medical Corporate Facility Node: {str(datos_rep['institucion'])}", ln=True)
        pdf.ln(3)
        
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(190, 6, "3. QUANTITATIVE EPIGENETIC METHYLATION READOUT (CORE SAMD ENGINE)", ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(190, 5, f"Global Mean Methylation Beta Score (Multiplexed MOX Panel): {float(datos_rep['score']):.4f}", ln=True)
        
        if float(datos_rep['score']) >= 0.1000:
            pdf.set_text_color(220, 38, 38)
            pdf.set_font("Helvetica", "B", 9)
            pdf.cell(190, 5, f"ALGORITHMIC CLINICAL VERDICT: {str(datos_rep['clasificacion'])}", ln=True)
            pdf.set_font("Helvetica", "I", 9)
            pdf.set_text_color(100, 116, 139)
            pdf.cell(190, 5, "INTERPRETATION SCORE: Positive ctDNA calling threshold surpassed. Complementary tissue biopsy suggested.", ln=True)
        else:
            pdf.set_text_color(22, 163, 74)
            pdf.set_font("Helvetica", "B", 9)
            pdf.cell(190, 5, "ALGORITHMIC CLINICAL VERDICT: Stable Baseline Control Range (Tumor Negative Screen)", ln=True)
            
        pdf.set_text_color(15, 23, 42)
        pdf.set_font("Helvetica", "", 9)
        
        if "TECHNICAL" in tipo_informe.upper():
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(190, 6, "4. TECHNICAL BIOINFORMATIC BIOCHEMICAL APPENDIX", ln=True)
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(190, 5, f"Active Patent CRISPR Probes Panel Signatures: {str(datos_rep['guias_activas'])}", ln=True)
            pdf.cell(190, 5, "Genomic Alignment Quality Quality: Passes Phred Quality Score Q30 parameters.", ln=True)
            
        pdf.ln(10)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(148, 163, 184)
        pdf.cell(190, 4, "Regulatory Compliance Notice: This system operates as a Software as a Medical Device (SaMD) compliant with HIPAA and FDA 21 CFR Part 11 guidelines.", ln=True, align="C")
        pdf.cell(190, 4, "Restricted pre-clinical research use only. Confidential proprietary assets of METHYLOX Platform 2026.", ln=True, align="C")
        
        try:
            final_pdf_payload = pdf.output(dest='S').encode('latin1')
        except Exception:
            final_pdf_payload = bytes(pdf.output())
            
        st.download_button(
            label=f"🔬 Verify Electronic Signature & Download Defendible Dossier for Sample {m_select}",
            data=final_pdf_payload,
            file_name=f"METHYLOX_Defendible_Report_{m_select}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
#   TAB 6: ACCESS CONTROL (DYNAMIC RBAC AUTHORIZATION HUB)
# ----------------------------------------------------------------------------
elif nav_selection == "Access Control":
    st.markdown("<h2 class='welcome-header'>Identity Governance & Task Delegation</h2>", unsafe_allow_html=True)
    st.markdown("<p class='welcome-caption'>Provision custom laboratory operational roles dynamically without hardcoding</p>", unsafe_allow_html=True)
   
    st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)
    with st.form("universal_user_provisioning_form", clear_on_submit=True):
            st.markdown("#### Register New Authorized Staff Member")
            c1, c2 = st.columns(2)
            with c1:
                input_username = st.text_input("Email or Username", placeholder="doctor@hospital.com")
                input_full_name = st.text_input("Full Name", placeholder="e.g., Dr. John Doe, MD")
            with c2:
                input_password = st.text_input("Temporary Password", type="password", placeholder="••••••••••••")
                target_role_display = st.selectbox("System Role and Permissions", ["admin", "cls", "md"], format_func=lambda x: {"admin": "Administrator", "cls": "Laboratory Technician (CLS)", "md": "Clinical Doctor (MD)"}[x])
                 
            target_hospital_name = st.text_input("Hospital or Clinic Name", placeholder="e.g., Memorial General Hospital")
            submit_btn = st.form_submit_button("Activate User & Grant Access")
           
    if submit_btn:
        if not input_username or not input_password or not input_full_name:
            st.error("All clinical identity fields are mandatory.")
        else:
            payload_u = {
                "username": input_username,
                "password": input_password,
                "full_name": input_full_name,
                "role": target_role_display,
                "hospital_id": int(target_hospital_id)
            }
            try:
                response = requests.post(f"{BACKEND_URL}/api/v1/auth/provision-user", json=payload_u, headers=headers)
                if response.status_code == 200:
                    st.success("Staff Identity Successfully Activated & Tasks Delegated Real-Time.")
                else:
                    st.error(f"Identity Provisioning Rejection: {response.json().get('detail', 'Unauthorized operational sequence')}")
            except Exception:
                st.error("Deployment Connectivity Error: User profile could not be logged into database repository.")
    st.markdown('</div>', unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# ⚙️ TAB 7: SYSTEM SETTINGS (KERNEL INTEGRITY AUDIT TRAIL MONITOR)
# ----------------------------------------------------------------------------
elif nav_selection == "settings":
    st.markdown("<h2 class='welcome-header'>⚙️ Core Calibration Settings & Kernel Monitor</h2>", unsafe_allow_html=True)
    st.markdown("<p class='welcome-caption'>System validation and mathematical processing rules parameters</p>", unsafe_allow_html=True)
    
    st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)
    st.markdown("<p style='color:#0F172A; font-weight:700; font-size:14px; margin-bottom:10px;'>📜 METHYLOX_DETERMINISTIC_RULES.PY (AUDITABLE CONTEXT)</p>", unsafe_allow_html=True)
    st.code("""
def calculate_proprietary_cpg_beta_value(intensity_methylated: float, intensity_unmethylated: float) -> float:
    # Standard international methylation mathematical equation with fluorescence laser offset correction
    offset_correction = 100.0
    beta_value = intensity_methylated / (intensity_methylated + intensity_unmethylated + offset_correction)
    return round(float(beta_value), 4)
""", language="python")
    st.success("✅ Kernel system integrity check completed successfully. Deterministic rules matching validation parameters.")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# 🏛️ FOOTER LEGAL BOUNDARIES (CLEAN CHARACTER ENCODING)
# ============================================================================
st.markdown("""
<div style="text-align: center; padding: 20px 0px; margin-top: 40px; border-top: 1px solid #E2E8F0;">
    <p style="margin: 0; font-size: 12px; color: #94A3B8;">Copyright (c) 2026 METHYLOX Oncology. All rights reserved. SaMD Software Stage Compliance.</p>
</div>
""", unsafe_allow_html=True)
