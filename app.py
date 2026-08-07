import os
import time
import uuid
from datetime import datetime, date

import pandas as pd
import requests
import streamlit as st
import plotly.graph_objects as go
import jwt
from fpdf import FPDF

# ============================================================================
# STREAMLIT CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="METHYLOX™ | Epigenetic Intelligence Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# GLOBAL DESIGN SYSTEM
# ============================================================================
st.markdown("""
<style>
.stApp { background-color: #F8FAFC; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
[data-testid="stHeader"] { display: none; }
[data-testid="stMainBlockContainer"] { padding: 2rem 3rem; }
[data-testid="stSidebar"] { background: #0B0F19; }
[data-testid="stSidebar"] label { color: #CBD5E1 !important; }
.welcome-header { font-size: 26px !important; font-weight: 800 !important; color: #0F172A !important; text-align: center; margin-bottom: 5px; }
.welcome-caption { font-size: 13px !important; color: #64748B !important; text-align: center; margin-bottom: 25px; }
.executive-card-white { background: white; border: 1px solid #E2E8F0; border-radius: 14px; padding: 24px; margin-bottom: 20px; }
.card-title-clinical { text-align: center; font-size: 18px; font-weight: 700; color: #0F172A; margin-bottom: 20px; }
.metric-card-clinical-new { background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:18px; text-align:center; min-height:150px; box-shadow:0 1px 3px rgba(0,0,0,0.04); }
.svg-top-container { margin-bottom:8px; }
.metric-title-sub-new { color:#64748B; font-size:12px; font-weight:700; margin:0; }
.metric-num-big-new { color:#0F172A; font-size:30px; font-weight:800; margin:8px 0 0 0; }
.section-card { background:white; border:1px solid #E2E8F0; border-radius:14px; padding:20px; margin-bottom:15px; }
.section-card-title { font-size:15px; font-weight:700; color:#0F172A; margin:0 0 12px 0; }
div[data-baseweb="input"] { border-radius:10px !important; border:1px solid #CBD5E1 !important; }
div[data-baseweb="input"]:focus-within { border-color: #2563EB !important; }
[data-testid="stDataFrame"] { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# BACKEND CONNECTION & SESSION STATE
# ============================================================================
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api/v1")

DEFAULT_SESSION = {
    "jwt_access_token": None, "operator_display_name": "Guest Operator",
    "user_role": None, "user_id": None, "permissions": [],
    "hospital_id": None, "hospital_name": None, "nav_selection": "dashboard",
    "show_new_patient_form": False, "show_sample_form": False,
    "patient_code_temp": None, "patient_anon_code_temp": None,
    "sample_code_temp": None, "login_error": None,
}

for key, value in DEFAULT_SESSION.items():
    if key not in st.session_state:
        st.session_state[key] = value


def get_auth_headers():
    return {"Authorization": f"Bearer {st.session_state.jwt_access_token}"} if st.session_state.jwt_access_token else {}

# ============================================================================
# API HELPERS
# ============================================================================

class ApiResult:
    def __init__(self, ok, data=None, error=None, status_code=None):
        self.ok = ok
        self.data = data if data is not None else []
        self.error = error
        self.status_code = status_code


def api_get(path, params=None, timeout=10):
    try:
        r = requests.get(
            f"{BACKEND_URL}{path}",
            headers=get_auth_headers(),
            params=params,
            timeout=timeout
        )
        if r.status_code == 200:
            return ApiResult(True, data=r.json() if r.text else {}, status_code=r.status_code)
        try:
            detail = r.json().get("detail", r.text)
        except:
            detail = r.text
        return ApiResult(False, error=detail, status_code=r.status_code)
    except requests.exceptions.RequestException as e:
        return ApiResult(False, error=str(e), status_code=None)


def api_post(path, json=None, files=None, timeout=10):
    try:
        r = requests.post(
            f"{BACKEND_URL}{path}",
            json=json,
            files=files,
            headers=get_auth_headers(),
            timeout=timeout
        )
        if r.status_code in (200, 201):
            return ApiResult(True, data=r.json() if r.text else {}, status_code=r.status_code)
        return ApiResult(False, error=r.text, status_code=r.status_code)
    except requests.exceptions.RequestException as e:
        return ApiResult(False, error=str(e), status_code=None)


@st.cache_data(ttl=20, show_spinner=False)
def cached_get(path, _headers_token):
    return api_get(path)

# ============================================================================
# LOAD PERMISSIONS & BACKEND STATUS
# ============================================================================
def load_user_permissions():
    if not st.session_state.user_id:
        return []
    result = api_get(f"/access/user/{st.session_state.user_id}")
    return [p["name"] for p in result.data] if result.ok else []


def check_backend_connection():
    try:
        r = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return True, r.json()
    except Exception as e:
        return False, {"error": str(e)}


backend_status, backend_info = check_backend_connection()

# ============================================================================
# SIDEBAR AUTHENTICATION
# ============================================================================
with st.sidebar:
    st.markdown("""
        <div style="padding:15px 0px; border-bottom:1px solid #1E293B; margin-bottom:25px;">
            <h2 style="color:white;">METHYLOX™</h2>
            <p style="color:#38BDF8;">Epigenetic Intelligence Platform</p>
        </div>
    """, unsafe_allow_html=True)

    if backend_status: st.success("Backend Online")
    else: st.error("Backend Offline")

    if not st.session_state.jwt_access_token:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login = st.form_submit_button("Authenticate", use_container_width=True)

        if login:
            response = requests.post(f"{BACKEND_URL}/auth/login", data={"username": username, "password": password})
            if response.status_code == 200:
                data = response.json()
                token = data["access_token"]
                st.session_state.jwt_access_token = token
                decoded = jwt.decode(token, options={"verify_signature": False})
                st.session_state.user_role = decoded.get("role", "viewer")
                st.session_state.user_id = decoded.get("id_user")
                st.session_state.operator_display_name = decoded.get("sub", username)
                st.session_state.hospital_id = decoded.get("id_hospital")
                st.session_state.permissions = load_user_permissions()
                st.rerun()
    else:
        st.markdown(f"""
            <div style="background:#1E293B; padding:15px; border-radius:10px;">
                <span style="color:#94A3B8;">USER</span><br>
                <b style="color:white;">{st.session_state.operator_display_name}</b><br>
                <span style="color:#38BDF8;">ROLE: {st.session_state.user_role}</span>
            </div>
        """, unsafe_allow_html=True)

    # ======================================================
    # NAVIGATION BY PERMISSIONS
    # ======================================================
    menu_options = {"dashboard": "Dashboard"}
    permissions = st.session_state.permissions

    if "patient_read" in permissions: menu_options["patients"] = "Patients"
    if "sample_read" in permissions: menu_options["lims"] = "Samples"
    if "analysis_read" in permissions: menu_options["analysis"] = "Analysis"
    if "report_read" in permissions: menu_options["reports"] = "Reports"

    if st.session_state.user_role == "admin":
        menu_options.update({"users": "Access Control", "settings": "Audit Trail"})

    nav_selection = st.radio(
        "Navigation", options=list(menu_options.keys()),
        format_func=lambda x: menu_options[x], key="nav_selection"
    ) if st.session_state.jwt_access_token else "restricted"

headers = get_auth_headers()

# ============================================================================
# PANTALLA SIN SESIÓN
# ============================================================================
if nav_selection == "restricted":
    st.markdown('<div class="executive-card-white" style="text-align:center; padding:60px 40px; margin-top:40px;">', unsafe_allow_html=True)
    st.markdown("<h2 style='color:#0F172A; font-weight:800; font-size:24px; margin-bottom:10px;'>Acceso restringido</h2>", unsafe_allow_html=True)
    st.caption("Ingresa credenciales de clínico autorizado en la barra lateral para continuar.")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# TAB: DASHBOARD
# ============================================================================
elif nav_selection == "dashboard":
    st.markdown(f'<h2 class="welcome-header">Welcome back, {st.session_state.operator_display_name}</h2>', unsafe_allow_html=True)
    st.markdown('<p class="welcome-caption">Laboratory Operations Dashboard | Real-Time Clinical Workflow Monitoring</p>', unsafe_allow_html=True)

    samples_result = cached_get("/samples/", st.session_state.jwt_access_token)
    samples = samples_result.data if samples_result.ok else []

    if not samples_result.ok:
        st.warning(f"No se pudieron cargar los datos del laboratorio: {samples_result.error}")

    today_str = date.today().isoformat()
    received_today = sum(1 for s in samples if str(s.get("collection_date", "")).startswith(today_str))
    in_progress = sum(1 for s in samples if s.get("status") not in ("Report Ready", None))
    ready_reports = sum(1 for s in samples if s.get("status") == "Report Ready")
    total_samples = len(samples)

    m1, m2, m3, m4 = st.columns(4)
    metric_defs = [
        (m1, "#2563EB", "Samples Received Today", received_today, '<path d="M10 2v8L4.72 17.55a1 1 0 0 0 .83 1.45h12.9a1 1 0 0 0 .83-1.45L14 10V2Z"/><path d="M14 2h-4"/>'),
        (m2, "#D97706", "Active Workflow", in_progress, '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>'),
        (m3, "#16A34A", "Ready Reports", ready_reports, '<path d="M6 2h9l3 3v17H6z"/><polyline points="14 2 14 8 20 8"/>'),
        (m4, "#6366F1", "Total Samples", total_samples, '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'),
    ]
    for col, color, title, value, svg_path in metric_defs:
        with col:
            st.markdown(f"""
            <div class="metric-card-clinical-new">
            <div class="svg-top-container" style="color:{color};">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">{svg_path}</svg>
            </div>
            <p class="metric-title-sub-new">{title}</p>
            <p class="metric-num-big-new">{value}</p>
            </div>
            """, unsafe_allow_html=True)

    st.caption("Nota: el indicador de tasa de control de calidad (QC) se retiró temporalmente — dependía de un endpoint del backend que todavía no existe (`/analysis/telemetry-summary`). Se puede reincorporar en cuanto ese endpoint se defina.")
    st.write("")

    col_left, col_right = st.columns([1.45, 1])

    with col_left:
        st.markdown('<div class="section-card"><p class="section-card-title">Recent Laboratory Activity Trail</p>', unsafe_allow_html=True)
        if samples:
            activity_df = pd.DataFrame(samples)
            cols = [c for c in ["sample_code", "patient_id", "sample_type", "status"] if c in activity_df.columns]
            activity_df = activity_df[cols].rename(columns={
                "sample_code": "Sample ID", "patient_id": "Patient ID",
                "sample_type": "Matrix", "status": "Status"
            })
            st.dataframe(activity_df.head(8), use_container_width=True, hide_index=True, height=280)
        else:
            st.info("No hay muestras registradas todavía." if samples_result.ok else "Sin datos disponibles (ver aviso arriba).")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-card"><p class="section-card-title">Distribución por Estado de Flujo</p>', unsafe_allow_html=True)
        if samples:
            status_counts = pd.DataFrame(samples)["status"].value_counts()
            fig = go.Figure(data=[go.Pie(labels=status_counts.index.tolist(), values=status_counts.values.tolist(), hole=0.60)])
            fig.update_layout(height=260, margin=dict(l=0, r=0, t=10, b=10), showlegend=True, paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown('<p style="color:#94A3B8; font-size:12px; text-align:center; padding:25px;">Sin datos de muestras todavía.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<p class="section-card-title" style="margin-top:10px;">Quick Clinical Workflows</p>', unsafe_allow_html=True)
    q1, q2, q3, q4 = st.columns(4)
    workflow_targets = [
        (q1, "Enroll Subject", "New Patient Profile", "patients"),
        (q2, "Asset Intake", "Log LIMS Custody", "lims"),
        (q3, "Start Analysis", "Register Analysis Result", "analysis"),
        (q4, "Dossier Sheet", "Export Medical PDF", "reports"),
    ]
    for col, title, subtitle, target_nav in workflow_targets:
        with col:
            if st.button(f"{title}\n{subtitle}", key=f"quickbtn_{target_nav}", use_container_width=True):
                st.session_state.nav_selection = target_nav
                st.rerun()

    st.markdown("""
    <div style="text-align:center; padding:20px 0; margin-top:30px; border-top:1px solid #E2E8F0;">
    <p style="margin:0; font-size:12px; color:#94A3B8;">Copyright (c) 2026 METHYLOX Oncology. All rights reserved. SaMD Software Stage Compliance.</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# TAB: PATIENTS
# ============================================================================
elif nav_selection == "patients":
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:15px;">
        <div style="color:#2563EB;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>
                <path d="M19 8v6"/><path d="M22 11h-6"/>
            </svg>
        </div>
        <div>
            <div style="font-size:18px; font-weight:800; color:#0F172A;">Clinical Cohort Management</div>
            <div style="font-size:11px; color:#64748B;">Patient Registry &amp; Subject Tracking</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    def normalize_patients(data):
        if not data:
            return pd.DataFrame()
        rows = []
        for p in data:
            demo = p.get("demographics") or {}
            rows.append({
                "Patient ID": p.get("patient_code", ""),
                "_row_id": p.get("id"),
                "Anonymous Code": demo.get("anonymous_code", ""),
                "Full Name": demo.get("full_name", ""),
                "Record Number": demo.get("record_number", ""),
                "Date of Birth": demo.get("date_of_birth", ""),
                "Gender": demo.get("gender", ""),
                "Institution": demo.get("institution", ""),
            })
        return pd.DataFrame(rows)

    if st.session_state.patient_code_temp is None:
        st.session_state.patient_code_temp = f"PAT-{datetime.now().year}-{str(uuid.uuid4())[:4].upper()}"
    if st.session_state.patient_anon_code_temp is None:
        st.session_state.patient_anon_code_temp = f"MOX-{str(uuid.uuid4())[:6].upper()}"

    patients_result = cached_get("/patients/", st.session_state.jwt_access_token)
    patients_df = normalize_patients(patients_result.data if patients_result.ok else [])

    if not patients_result.ok:
        st.warning(f"Failed to load patient directory: {patients_result.error}")

    if not st.session_state.show_new_patient_form:
        search_col, button_col = st.columns([4, 1])
        with search_col:
            search_query = st.text_input("Search patient", placeholder="Search by ID, record number or institution", label_visibility="collapsed")
        with button_col:
            if st.button("New Patient", use_container_width=True, key="new_patient_button"):
                st.session_state.show_new_patient_form = True
                st.rerun()

        if not patients_df.empty:
            filtered_df = patients_df.copy()
            if search_query:
                mask = filtered_df.astype(str).apply(lambda row: row.str.contains(search_query, case=False, na=False).any(), axis=1)
                filtered_df = filtered_df[mask]
            st.markdown('<div class="section-card"><p class="section-card-title">Patient Records Directory</p>', unsafe_allow_html=True)
            st.dataframe(filtered_df.drop(columns=["_row_id"]), use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No registered patients found." if patients_result.ok else "No data available (see warning above).")

    else:
        if st.button("← Back to Directory", key="back_patient_directory"):
            st.session_state.show_new_patient_form = False
            st.rerun()

        left, right = st.columns([1, 1])

        with left:
            st.markdown('<div class="section-card"><p class="section-card-title">Register New Patient</p>', unsafe_allow_html=True)
            patient_code = st.text_input("Patient ID", value=st.session_state.patient_code_temp, disabled=True)
            anonymous_code = st.text_input("Anonymous Clinical Code", value=st.session_state.patient_anon_code_temp, disabled=True)
            full_name = st.text_input("Full Name")
            record_number = st.text_input("Record Number")
            date_birth = st.date_input("Date of Birth")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            institution = st.text_input("Institution")
            clinical_notes = st.text_area("Clinical Notes", height=70)

            if st.button("Save Patient Record", use_container_width=True, key="save_patient"):
                if not full_name or not record_number or not institution:
                    st.error("Please complete required fields (Full Name, Record Number, Institution).")
                else:
                    payload = {
                        "patient_code": patient_code,
                        "demographics": {
                            "anonymous_code": anonymous_code,
                            "full_name": full_name,
                            "record_number": record_number,
                            "date_of_birth": str(date_birth),
                            "gender": gender,
                            "institution": institution,
                        },
                        "clinical_notes": clinical_notes,
                    }
                    result = api_post("/patients/", json=payload)
                    if result.ok:
                        st.success("Patient registered successfully.")
                        st.cache_data.clear()
                        st.session_state.show_new_patient_form = False
                        st.session_state.patient_code_temp = None
                        st.session_state.patient_anon_code_temp = None
                        time.sleep(0.8)
                        st.rerun()
                    elif result.status_code == 403:
                        st.error("You do not have permission to register patients (missing 'patient_create' permission).")
                    elif result.status_code == 400:
                        st.error(f"Failed to register: {result.error}")
                    else:
                        st.error(f"Error registering patient: {result.error}")
            st.markdown('</div>', unsafe_allow_html=True)

        with right:
            st.markdown('<div class="section-card"><p class="section-card-title">Clinical Cohort Overview</p>', unsafe_allow_html=True)
            if not patients_df.empty:
                selected_patient = st.selectbox("Select Patient", patients_df["Patient ID"].tolist())
                patient_detail = patients_df[patients_df["Patient ID"] == selected_patient].iloc[0]
                st.markdown(f"""
                <div style="background:#F8FAFC; border-radius:10px; padding:12px; border:1px solid #E2E8F0;">
                <p style="margin:0 0 6px 0; font-size:12px;"><b>Patient ID:</b> {patient_detail['Patient ID']}</p>
                <p style="margin:0 0 6px 0; font-size:12px;"><b>Anonymous Code:</b> {patient_detail['Anonymous Code']}</p>
                <p style="margin:0 0 6px 0; font-size:12px;"><b>Full Name:</b> {patient_detail['Full Name']}</p>
                <p style="margin:0 0 6px 0; font-size:12px;"><b>Record Number:</b> {patient_detail['Record Number']}</p>
                <p style="margin:0 0 6px 0; font-size:12px;"><b>Institution:</b> {patient_detail['Institution']}</p>
                <p style="margin:0; font-size:12px;"><b>Gender:</b> {patient_detail['Gender']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.caption("No patient data yet.")
            st.markdown('</div>', unsafe_allow_html=True)

    st.caption("Pending privacy note: currently `full_name` and `anonymous_code` reside in the same record — any role with `patient_read` permission sees both. If true de-identification is required against certain roles, this needs to be separated in the backend.")

# ============================================================================
# TAB: REPORTS & CLINICAL DOSSIERS
# ============================================================================
elif nav_selection == "reports":
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:15px;">
        <div style="color:#2563EB;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>
            </svg>
        </div>
        <div>
            <div style="font-size:18px; font-weight:800; color:#0F172A;">Clinical Reports &amp; Dossiers</div>
            <div style="font-size:11px; color:#64748B;">PDF Generation • SaMD Official Clinical Output</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    samples_result = cached_get("/samples/", st.session_state.jwt_access_token)
    samples_data = samples_result.data if samples_result.ok else []

    patients_result = cached_get("/patients/", st.session_state.jwt_access_token)
    patients_data = patients_result.data if patients_result.ok else []
    patient_dict = {p.get("id"): p for p in patients_data if p.get("id")}

    if not samples_result.ok:
        st.warning(f"No se pudieron cargar las muestras: {samples_result.error}")
    elif not samples_data:
        st.info("No hay muestras disponibles para generar reportes.")
    else:
        sample_codes = [s.get("sample_code") for s in samples_data if s.get("sample_code")]
        selected_report_code = st.selectbox("Seleccionar Muestra para Reporte PDF", sample_codes, key="report_sample_selector")

        selected_sample = next((s for s in samples_data if s.get("sample_code") == selected_report_code), None)

        if selected_sample:
            patient_id = selected_sample.get("patient_id")
            patient_obj = patient_dict.get(patient_id, {})
            demographics = patient_obj.get("demographics") or {}

            sample_db_id = selected_sample.get("id")
            analysis_result = api_get(f"/analysis/sample/{sample_db_id}")
            analysis_list = analysis_result.data if analysis_result.ok and isinstance(analysis_result.data, list) else []
            latest_analysis = analysis_list[0] if analysis_list else {}
            metrics = latest_analysis.get("metrics") or {}

            st.markdown('<div class="section-card"><p class="section-card-title">Vista Previa del Reporte Clínico</p>', unsafe_allow_html=True)

            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.markdown(f"""
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px; padding:15px; font-size:12px;">
                <p style="margin:0 0 8px 0; font-weight:700; color:#0F172A;">INFORMACIÓN DEL PACIENTE</p>
                <p style="margin:0 0 4px 0;"><b>Nombre:</b> {demographics.get('full_name', '—')}</p>
                <p style="margin:0 0 4px 0;"><b>Código Anónimo:</b> {demographics.get('anonymous_code', '—')}</p>
                <p style="margin:0 0 4px 0;"><b>HC / Registro:</b> {demographics.get('record_number', '—')}</p>
                <p style="margin:0;"><b>Institución:</b> {demographics.get('institution', '—')}</p>
                </div>
                """, unsafe_allow_html=True)
            with col_p2:
                st.markdown(f"""
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px; padding:15px; font-size:12px;">
                <p style="margin:0 0 8px 0; font-weight:700; color:#0F172A;">DATOS DE LA MUESTRA Y ANÁLISIS</p>
                <p style="margin:0 0 4px 0;"><b>Sample ID:</b> {selected_sample.get('sample_code', '—')}</p>
                <p style="margin:0 0 4px 0;"><b>Tipo de Espécimen:</b> {selected_sample.get('sample_type', '—')}</p>
                <p style="margin:0 0 4px 0;"><b>Beta Score:</b> {metrics.get('beta_score', 'Pendiente / No registrado')}</p>
                <p style="margin:0;"><b>Clasificación:</b> {latest_analysis.get('classification', 'Pendiente')}</p>
                </div>
                """, unsafe_allow_html=True)

            st.write("")

            class PDFReport(FPDF):
                def header(self):
                    self.set_font("helvetica", "B", 16)
                    self.set_text_color(15, 23, 42)
                    self.cell(0, 10, "METHYLOX(TM) - DOSSIER CLÍNICO EPIGENÉTICO", 0, 1, "L")
                    self.set_font("helvetica", "", 9)
                    self.set_text_color(100, 116, 139)
                    self.cell(0, 5, "Plataforma de Inteligencia Epigenética en Oncología | SaMD Compliance", 0, 1, "L")
                    self.ln(5)

                def footer(self):
                    self.set_y(-15)
                    self.set_font("helvetica", "I", 8)
                    self.set_text_color(150, 150, 150)
                    self.cell(0, 10, f"Página {self.page_no()} | Documento Confidencial de Uso Médico", 0, 0, "C")

            def generate_pdf_bytes():
                pdf = PDFReport()
                pdf.add_page()
                pdf.set_auto_page_break(auto=True, margin=15)

                pdf.set_font("helvetica", "B", 11)
                pdf.set_text_color(37, 99, 235)
                pdf.cell(0, 8, "1. DATOS DE IDENTIFICACIÓN DEL PACIENTE", 0, 1, "L")
                pdf.set_font("helvetica", "", 10)
                pdf.set_text_color(0, 0, 0)
                pdf.cell(0, 6, f"Paciente: {demographics.get('full_name', 'N/A')}", 0, 1, "L")
                pdf.cell(0, 6, f"Código Anónimo: {demographics.get('anonymous_code', 'N/A')}", 0, 1, "L")
                pdf.cell(0, 6, f"No. Registro / HC: {demographics.get('record_number', 'N/A')}", 0, 1, "L")
                pdf.cell(0, 6, f"Institución: {demographics.get('institution', 'N/A')}", 0, 1, "L")
                pdf.ln(4)

                pdf.set_font("helvetica", "B", 11)
                pdf.set_text_color(37, 99, 235)
                pdf.cell(0, 8, "2. TRAZABILIDAD DE LA MUESTRA (LIMS)", 0, 1, "L")
                pdf.set_font("helvetica", "", 10)
                pdf.set_text_color(0, 0, 0)
                pdf.cell(0, 6, f"Sample ID: {selected_sample.get('sample_code', 'N/A')}", 0, 1, "L")
                pdf.cell(0, 6, f"Espécimen: {selected_sample.get('sample_type', 'N/A')}", 0, 1, "L")
                pdf.cell(0, 6, f"Fecha de Colección: {selected_sample.get('collection_date', 'N/A')}", 0, 1, "L")
                pdf.cell(0, 6, f"Ubicación de Almacenamiento: {selected_sample.get('storage_location', 'N/A')}", 0, 1, "L")
                pdf.ln(4)

                pdf.set_font("helvetica", "B", 11)
                pdf.set_text_color(37, 99, 235)
                pdf.cell(0, 8, "3. RESULTADO DEL ANÁLISIS MOLECULAR", 0, 1, "L")
                pdf.set_font("helvetica", "", 10)
                pdf.set_text_color(0, 0, 0)
                pdf.cell(0, 6, f"Pipeline Version: {latest_analysis.get('pipeline_version', 'N/A')}", 0, 1, "L")
                pdf.cell(0, 6, f"QC Status: {latest_analysis.get('qc_status', 'N/A')}", 0, 1, "L")
                pdf.cell(0, 6, f"Beta Score: {metrics.get('beta_score', 'N/A')}", 0, 1, "L")
                pdf.cell(0, 6, f"Clasificación Clínico-Molecular: {latest_analysis.get('classification', 'N/A')}", 0, 1, "L")
                pdf.ln(10)

                pdf.set_font("helvetica", "I", 9)
                pdf.set_text_color(100, 100, 100)
                pdf.multi_cell(0, 5, "Nota legal: Este informe ha sido generado automáticamente por la plataforma METHYLOX(TM) bajo supervisión de control de calidad de laboratorio clínico. Su interpretación debe ser valorada por el médico tratante en conjunto con el cuadro clínico del paciente.")

                return pdf.output()

            if st.button("Generar y Descargar Reporte PDF Oficial", use_container_width=True, key="download_pdf_button"):
                pdf_data = generate_pdf_bytes()
                st.download_label = "Descargar Archivo PDF"
                st.download_button(
                    label="📥 Haga clic aquí para descargar el PDF",
                    data=bytes(pdf_data),
                    file_name=f"Reporte_Clinico_{selected_report_code}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

            st.markdown('</div>', unsafe_allow_html=True)
# ============================================================================
# TAB: REPORTS
# ============================================================================
elif nav_selection == "reports":
    st.markdown("<h2 class='welcome-header'>Clinical Reports</h2>", unsafe_allow_html=True)
    st.markdown("<p class='welcome-caption'>Generate validated molecular analysis reports from METHYLOX™ laboratory records.</p>", unsafe_allow_html=True)
    st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)

    samples_result = cached_get("/samples/", st.session_state.jwt_access_token)
    samples_data = samples_result.data if samples_result.ok else []

    if not samples_data:
        st.info("No hay muestras disponibles." if samples_result.ok else f"No se pudieron cargar muestras: {samples_result.error}")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        samples_df = pd.DataFrame(samples_data)
        label_map = {s["id"]: s.get("sample_code", str(s["id"])) for s in samples_data}
        st.markdown("### Select Sample for Report Generation")
        selected_sample_id = st.selectbox("Sample", options=list(label_map.keys()), format_func=lambda x: label_map[x])

        generate_clicked = st.button("Cargar vista previa del reporte", use_container_width=True)

        if generate_clicked:
            report_result = api_get(f"/reports/sample/{selected_sample_id}")
            st.session_state["_report_preview"] = report_result

        report_result = st.session_state.get("_report_preview")

        if report_result and report_result.ok:
            report_data = report_result.data
            sample_info = report_data.get("sample", {})
            analysis_results = report_data.get("analysis_results", [])
            generated_by = report_data.get("generated_by", {})

            st.markdown("---")
            st.markdown("### Report Preview")
            preview_data = {
                "Sample Code": sample_info.get("sample_code", "N/A"),
                "Sample Type": sample_info.get("type", "N/A"),
                "Status": sample_info.get("status", "N/A"),
                "Analysis Count": len(analysis_results),
            }
            st.dataframe(pd.DataFrame([preview_data]), use_container_width=True, hide_index=True)

            report_format = st.radio("Document Format", ["Institutional Clinical Summary", "Technical Molecular Analysis"], horizontal=True)

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 14)
            pdf.set_text_color(30, 58, 138)
            pdf.cell(190, 10, "METHYLOX(TM) CLINICAL MOLECULAR REPORT", ln=True)
            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(100, 116, 139)
            pdf.cell(190, 5, "Epigenetic AI Laboratory Intelligence Platform | METHYLOX v3.0", ln=True)
            pdf.ln(5)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)

            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(15, 23, 42)
            pdf.cell(190, 6, "1. SAMPLE INFORMATION", ln=True)
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(95, 5, f"Sample ID: {sample_info.get('id')}", ln=True)
            pdf.cell(95, 5, f"Sample Code: {sample_info.get('sample_code')}", ln=True)
            pdf.cell(95, 5, f"Sample Type: {sample_info.get('type')}", ln=True)
            pdf.cell(95, 5, f"Sample Status: {sample_info.get('status')}", ln=True)
            pdf.ln(4)

            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(190, 6, "2. MOLECULAR ANALYSIS RESULTS", ln=True)
            pdf.set_font("Helvetica", "", 9)
            if analysis_results:
                for result in analysis_results:
                    metrics = result.get("metrics", {})
                    pdf.cell(190, 5, f"Pipeline Version: {result.get('pipeline')}", ln=True)
                    pdf.cell(190, 5, f"Quality Control Status: {result.get('qc_status')}", ln=True)
                    pdf.cell(190, 5, f"Beta Score: {metrics.get('beta_score', 'N/A')}", ln=True)
                    pdf.cell(190, 5, f"Classification: {result.get('classification')}", ln=True)
                    pdf.ln(3)
            else:
                pdf.cell(190, 5, "No molecular analysis results available.", ln=True)

            if "Technical" in report_format:
                pdf.ln(3)
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(190, 6, "3. TECHNICAL MOLECULAR APPENDIX", ln=True)
                pdf.set_font("Helvetica", "", 9)
                pdf.cell(190, 5, "METHYLOX computational pipeline evaluation.", ln=True)
                pdf.cell(190, 5, "Epigenetic biomarker analysis and quality assessment performed by the platform engine.", ln=True)

            pdf.ln(4)
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(190, 6, "4. REPORT TRACEABILITY", ln=True)
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(190, 5, f"Generated by User ID: {generated_by.get('user_id', 'N/A')}", ln=True)
            pdf.cell(190, 5, f"Operator: {generated_by.get('username', 'N/A')}", ln=True)
            pdf.cell(190, 5, f"Role: {generated_by.get('role', 'N/A')}", ln=True)
            pdf.ln(8)

            pdf.set_font("Helvetica", "I", 8)
            pdf.set_text_color(100, 116, 139)
            pdf.cell(190, 4, "Research and laboratory intelligence platform. Results require clinical validation according to applicable institutional procedures.", ln=True, align="C")
            pdf.cell(190, 4, "Confidential proprietary information of METHYLOX(TM) Platform.", ln=True, align="C")

            try:
                pdf_output = pdf.output(dest="S").encode("latin1")
            except Exception:
                pdf_output = bytes(pdf.output())

            st.download_button(
                label=f"Generate & Download METHYLOX™ Report - Sample {label_map[selected_sample_id]}",
                data=pdf_output,
                file_name=f"METHYLOX_Clinical_Report_{label_map[selected_sample_id]}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
            st.caption(
                "Nota: cada vista previa (`GET /reports/sample/{id}`) queda registrada en el log de "
                "auditoría del backend como 'GENERATE_REPORT' — no solo la descarga final. Vale la pena "
                "separar ambos eventos en el backend si el log de auditoría necesita reflejar solo "
                "descargas reales."
            )
        elif report_result and not report_result.ok:
            if report_result.status_code == 403:
                st.error("No tienes permiso para consultar este reporte.")
            elif report_result.status_code == 404:
                st.error("No se encontró información para esta muestra.")
            else:
                st.error(f"Error al cargar el reporte: {report_result.error}")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# TAB: ACCESS CONTROL
# ============================================================================
elif nav_selection == "users":
    st.markdown("<h2 class='welcome-header'>Identity Governance</h2>", unsafe_allow_html=True)
    st.markdown("<p class='welcome-caption'>Provisiona personal autorizado y asigna roles operativos dentro de METHYLOX™.</p>", unsafe_allow_html=True)

    st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)
    with st.form("user_provisioning_form", clear_on_submit=True):
        st.markdown("#### Registrar nuevo miembro del personal")
        c1, c2 = st.columns(2)
        with c1:
            input_username = st.text_input("Username", placeholder="jdoe")
            input_email = st.text_input("Email", placeholder="doctor@hospital.com")
            input_full_name = st.text_input("Full Name", placeholder="e.g., Dr. John Doe, MD")
        with c2:
            input_password = st.text_input("Temporary Password", type="password", placeholder="••••••••••••")
            target_role = st.selectbox(
                "System Role and Permissions",
                ["admin", "cls", "md"],
                format_func=lambda x: {"admin": "Administrator", "cls": "Laboratory Scientist (CLS)", "md": "Clinical Doctor (MD)"}[x],
            )
        submit_btn = st.form_submit_button("Activate User & Grant Access")

    if submit_btn:
        if not input_username or not input_email or not input_password or not input_full_name:
            st.error("Todos los campos de registro son obligatorios.")
        else:
            payload_u = {
                "username": input_username,
                "email": input_email,
                "password": input_password,
                "full_name": input_full_name,
                "role": target_role,
            }
            result = api_post("/users/", json=payload_u)
            if result.ok:
                st.success("Cuenta de usuario activada correctamente.")
                st.cache_data.clear()
            elif result.status_code == 403:
                st.error("No tienes permisos de administrador para crear usuarios.")
            elif result.status_code == 400:
                st.error(f"No se pudo crear el usuario: {result.error}")
            else:
                st.error(f"Error al crear usuario: {result.error}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)
    st.markdown('<p class="section-card-title">Personal registrado</p>', unsafe_allow_html=True)
    users_result = cached_get("/users/", st.session_state.jwt_access_token)
    if users_result.ok and users_result.data:
        users_df = pd.DataFrame(users_result.data)
        cols = [c for c in ["username", "email", "full_name", "role", "active", "last_login"] if c in users_df.columns]
        st.dataframe(users_df[cols], use_container_width=True, hide_index=True)
    elif users_result.ok:
        st.info("No hay usuarios registrados todavía.")
    else:
        st.warning(f"No se pudo cargar la lista de usuarios: {users_result.error}")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# TAB: AUDIT TRAIL
# ============================================================================
elif nav_selection == "settings":
    st.markdown("<h2 class='welcome-header'>Audit Trail</h2>", unsafe_allow_html=True)
    st.markdown("<p class='welcome-caption'>Registro de acciones del sistema para trazabilidad clínica.</p>", unsafe_allow_html=True)

    st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)
    audit_result = cached_get("/audit/", st.session_state.jwt_access_token)
    if audit_result.ok and audit_result.data:
        audit_df = pd.DataFrame(audit_result.data)
        cols = [c for c in ["created_at", "user_id", "action", "module", "entity"] if c in audit_df.columns]
        display_df = audit_df[cols].sort_values("created_at", ascending=False) if "created_at" in cols else audit_df[cols]
        st.dataframe(display_df, use_container_width=True, hide_index=True, height=500)
    elif audit_result.ok:
        st.info("Sin eventos de auditoría todavía.")
    else:
        st.warning(f"No se pudo cargar el log de auditoría: {audit_result.error}")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# FOOTER LEGAL
# ============================================================================
if st.session_state.jwt_access_token:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0px; margin-top: 40px; border-top: 1px solid #E2E8F0;">
        <p style="margin: 0; font-size: 12px; color: #94A3B8;">Copyright (c) 2026 METHYLOX Oncology. All rights reserved. SaMD Software Stage Compliance.</p>
    </div>
    """, unsafe_allow_html=True)
