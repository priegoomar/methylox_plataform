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
# GLOBAL DESIGN SYSTEM (consolidado en un solo bloque)
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
    "jwt_access_token": None,
    "operator_display_name": "Guest Operator",
    "user_role": None,
    "nav_selection": "dashboard",
    "show_new_patient_form": False,
    "show_sample_form": False,
    "patient_code_temp": None,
    "patient_anon_code_temp": None,
    "sample_code_temp": None,
    "login_error": None,
}

for key, value in DEFAULT_SESSION.items():
    if key not in st.session_state:
        st.session_state[key] = value


def get_auth_headers():
    if st.session_state.jwt_access_token:
        return {"Authorization": f"Bearer {st.session_state.jwt_access_token}"}
    return {}


headers = get_auth_headers()


# ============================================================================
# HELPERS DE RED — separan error de conexión de "sin datos"
# ============================================================================

class ApiResult:
    """Encapsula el resultado de una llamada para no confundir '0 registros'
    con 'no se pudo conectar' (bug que arrastraba la versión anterior)."""
    def __init__(self, ok, data=None, error=None, status_code=None):
        self.ok = ok
        self.data = data if data is not None else []
        self.error = error
        self.status_code = status_code


def api_get(path, params=None, timeout=10):
    try:
        r = requests.get(f"{BACKEND_URL}{path}", headers=get_auth_headers(), params=params, timeout=timeout)
        if r.status_code == 200:
            return ApiResult(True, data=r.json(), status_code=200)
        try:
            detail = r.json().get("detail", r.text)
        except Exception:
            detail = r.text
        return ApiResult(False, error=detail, status_code=r.status_code)
    except requests.exceptions.RequestException as e:
        return ApiResult(False, error=f"Sin conexión con el backend ({e.__class__.__name__})", status_code=None)


def api_post(path, json=None, files=None, timeout=10):
    try:
        r = requests.post(f"{BACKEND_URL}{path}", json=json, files=files, headers=get_auth_headers(), timeout=timeout)
        if r.status_code in (200, 201):
            return ApiResult(True, data=r.json() if r.text else {}, status_code=r.status_code)
        try:
            detail = r.json().get("detail", r.text)
        except Exception:
            detail = r.text
        return ApiResult(False, error=detail, status_code=r.status_code)
    except requests.exceptions.RequestException as e:
        return ApiResult(False, error=f"Sin conexión con el backend ({e.__class__.__name__})", status_code=None)


def api_patch(path, json=None, timeout=10):
    try:
        r = requests.patch(f"{BACKEND_URL}{path}", json=json, headers=get_auth_headers(), timeout=timeout)
        if r.status_code == 200:
            return ApiResult(True, data=r.json() if r.text else {}, status_code=200)
        try:
            detail = r.json().get("detail", r.text)
        except Exception:
            detail = r.text
        return ApiResult(False, error=detail, status_code=r.status_code)
    except requests.exceptions.RequestException as e:
        return ApiResult(False, error=f"Sin conexión con el backend ({e.__class__.__name__})", status_code=None)


@st.cache_data(ttl=20, show_spinner=False)
def cached_get(path, _headers_token):
    """Cachea lecturas frecuentes 20s para no martillar el backend en cada
    rerun. _headers_token solo se usa para invalidar caché si cambia el token."""
    return api_get(path)


# ============================================================================
# BACKEND CONNECTIVITY MONITOR
# ============================================================================

def check_backend_connection():
    try:
        r = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return (True, r.json()) if r.status_code == 200 else (False, {"status": r.status_code})
    except Exception as e:
        return False, {"error": str(e)}


backend_status, backend_info = check_backend_connection()

# ============================================================================
# SIDEBAR: AUTENTICACIÓN Y NAVEGACIÓN
# ============================================================================

with st.sidebar:
    st.markdown("""
    <div style="padding:15px 0px; border-bottom:1px solid #1E293B; margin-bottom:25px;">
        <h2 style="color:white; margin:0; font-weight:900;">METHYLOX™</h2>
        <p style="color:#38BDF8; font-size:12px; margin:0;">Epigenetic Intelligence Platform</p>
    </div>
    """, unsafe_allow_html=True)

    if backend_status:
        st.sidebar.success("Backend Online")
    else:
        st.sidebar.error("Backend Offline")
        st.sidebar.caption("No se puede iniciar sesión ni cargar datos hasta reestablecer la conexión.")

    # ------------------------------------------------------------------
    # LOGIN
    # ------------------------------------------------------------------
    if not st.session_state.jwt_access_token:
        with st.form("login_form"):
            st.markdown('<p style="color:#94A3B8; font-size:12px; font-weight:700;">SECURE AUTHENTICATION</p>', unsafe_allow_html=True)
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login = st.form_submit_button("Authenticate", use_container_width=True, disabled=not backend_status)

        if login:
            if not username or not password:
                st.session_state.login_error = "Ingresa usuario y contraseña."
            else:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/auth/login",
                        data={"username": username, "password": password},
                        timeout=8
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.jwt_access_token = data["access_token"]
                        decoded = jwt.decode(data["access_token"], options={"verify_signature": False})
                        st.session_state.user_role = decoded.get("role", "cls").lower()
                        st.session_state.operator_display_name = decoded.get("sub", username)
                        st.session_state.login_error = None
                        st.rerun()
                    elif response.status_code == 401:
                        st.session_state.login_error = "Usuario o contraseña incorrectos."
                    elif response.status_code == 403:
                        st.session_state.login_error = "Usuario inactivo. Contacta a un administrador."
                    else:
                        st.session_state.login_error = f"Error inesperado del servidor ({response.status_code})."
                except requests.exceptions.RequestException:
                    st.session_state.login_error = "No se pudo conectar con el backend."

        if st.session_state.login_error:
            st.sidebar.error(st.session_state.login_error)

    # ------------------------------------------------------------------
    # SESIÓN ACTIVA
    # ------------------------------------------------------------------
    else:
        st.markdown(
            f"""
            <div style="background:#1E293B; padding:15px; border-radius:10px;">
            <span style="color:#94A3B8;font-size:11px;">ACTIVE USER</span><br>
            <b style="color:white;">{st.session_state.operator_display_name}</b><br>
            <span style="color:#38BDF8;font-size:12px;">ROLE: {(st.session_state.user_role or "").upper()}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Disconnect", use_container_width=True):
            for key, value in DEFAULT_SESSION.items():
                st.session_state[key] = value
            st.cache_data.clear()
            st.rerun()

    st.sidebar.markdown("---")

    # ------------------------------------------------------------------
    # MENÚ RBAC — única fuente de verdad para nav_selection
    # ------------------------------------------------------------------
    menu_options = {
        "dashboard": "Dashboard",
        "patients": "Patients",
        "lims": "Samples",
        "analysis": "Analysis",
        "reports": "Reports",
    }
    if st.session_state.user_role == "admin":
        menu_options.update({
            "users": "Access Control",
            "settings": "Audit Trail",
        })

    if st.session_state.jwt_access_token:
        nav_selection = st.sidebar.radio(
            "Navigation",
            options=list(menu_options.keys()),
            format_func=lambda x: menu_options[x],
            key="nav_selection",
        )
    else:
        nav_selection = "restricted"

headers = get_auth_headers()
# (fin de la sección de sidebar / inicio de las vistas)

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
            st.dataframe(activity_df.tail(8), use_container_width=True, hide_index=True, height=280)
        else:
            st.info("No hay muestras registradas todavía." if samples_result.ok else "Sin datos disponibles (ver aviso arriba).")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-card"><p class="section-card-title">Live Interactive Data Stream</p>', unsafe_allow_html=True)
        if samples:
            live_df = pd.DataFrame(samples)
            live_cols = [c for c in ["sample_code", "sample_type", "status"] if c in live_df.columns]
            st.dataframe(live_df[live_cols].tail(5), use_container_width=True, hide_index=True, height=180)
        else:
            st.caption("Awaiting laboratory telemetry stream...")
        st.markdown('</div>', unsafe_allow_html=True)        
        st.markdown('<div class="section-card"><p class="section-card-title">Workflow Status Distribution</p>', unsafe_allow_html=True)
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
        st.warning(f"No se pudo cargar el directorio de pacientes: {patients_result.error}")

    if not st.session_state.show_new_patient_form:
        search_col, button_col = st.columns([4, 1])
        with search_col:
            search_query = st.text_input("Buscar paciente", placeholder="Buscar por ID, expediente o institución", label_visibility="collapsed")
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
            st.info("No hay pacientes registrados." if patients_result.ok else "Sin datos disponibles (ver aviso arriba).")

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
                    st.error("Completa los campos obligatorios (Full Name, Record Number, Institution).")
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
                        st.success("Paciente registrado correctamente.")
                        st.cache_data.clear()
                        st.session_state.show_new_patient_form = False
                        st.session_state.patient_code_temp = None
                        st.session_state.patient_anon_code_temp = None
                        time.sleep(0.8)
                        st.rerun()
                    elif result.status_code == 403:
                        st.error("No tienes permiso para registrar pacientes (falta el permiso 'patient_create').")
                    elif result.status_code == 400:
                        st.error(f"No se pudo registrar: {result.error}")
                    else:
                        st.error(f"Error al registrar paciente: {result.error}")
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
                st.caption("Sin datos de pacientes todavía.")
            st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# TAB: LIMS SAMPLE MANAGEMENT
# ============================================================================
elif nav_selection == "lims":

    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:15px;">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2">
            <path d="M9 2h6"/><path d="M10 2v6l-5 9a3 3 0 0 0 3 5h8a3 3 0 0 0 3-5l-5-9V2"/><path d="M8 14h8"/>
        </svg>
        <div>
            <div style="font-size:18px; font-weight:800; color:#0F172A;">LIMS Sample Management</div>
            <div style="font-size:11px; color:#64748B;">Clinical Specimen Registry • Chain of Custody • Laboratory Workflow</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_btn1, _ = st.columns([1, 5])
    with col_btn1:
        if st.button("+ Register New Sample", use_container_width=True):
            st.session_state.show_sample_form = True
            st.session_state.sample_code_temp = None
            st.rerun()

    patients_result = cached_get("/patients/", st.session_state.jwt_access_token)
    patients_data = patients_result.data if patients_result.ok else []
    patient_label_by_id = {
        p.get("id"): f"{p.get('patient_code', '?')} — {(p.get('demographics') or {}).get('full_name', 'sin nombre')}"
        for p in patients_data if p.get("id")
    }

    samples_result = cached_get("/samples/", st.session_state.jwt_access_token)
    samples_data = samples_result.data if samples_result.ok else []
    if not samples_result.ok:
        st.warning(f"No se pudieron cargar las muestras: {samples_result.error}")

    left_panel, right_panel = st.columns([2, 1], gap="medium")

    with left_panel:
        st.markdown('<div class="section-card"><p class="section-card-title">Laboratory Sample Directory</p>', unsafe_allow_html=True)
        if samples_data:
            df_samples = pd.DataFrame(samples_data)
            rename_columns = {
                "sample_code": "Sample ID", "patient_id": "Patient ID", "sample_type": "Specimen",
                "collection_date": "Collection Date", "status": "Status", "storage_location": "Storage Location",
            }
            df_samples = df_samples.rename(columns={k: v for k, v in rename_columns.items() if k in df_samples.columns})
            visible_columns = [c for c in ["Sample ID", "Patient ID", "Specimen", "Collection Date", "Status", "Storage Location"] if c in df_samples.columns]

            search_sample = st.text_input("Search Sample", placeholder="Buscar por Sample ID, Patient ID o estado", key="sample_search_box")
            if search_sample:
                mask = df_samples.astype(str).apply(lambda row: row.str.contains(search_sample, case=False, na=False).any(), axis=1)
                df_display = df_samples[mask]
            else:
                df_display = df_samples

            st.dataframe(df_display[visible_columns], use_container_width=True, hide_index=True)

            if "Sample ID" in df_display.columns:
                available_samples = df_display["Sample ID"].tolist()
                if available_samples:
                    selected_sample = st.selectbox("Selected Sample", available_samples, key="lims_sample_selector")
                    st.session_state["selected_sample_code"] = selected_sample
        else:
            st.info("No hay muestras registradas." if samples_result.ok else "Sin datos disponibles (ver aviso arriba).")
        st.markdown('</div>', unsafe_allow_html=True)

    with right_panel:
        st.markdown('<div class="section-card"><p class="section-card-title">Sample Intelligence Panel</p>', unsafe_allow_html=True)
        selected_code = st.session_state.get("selected_sample_code")
        selected_sample = next((s for s in samples_data if s.get("sample_code") == selected_code), None) if selected_code else None

        if selected_sample:
            detail_data = {
                "Sample ID": selected_sample.get("sample_code", "--"),
                "Patient": patient_label_by_id.get(selected_sample.get("patient_id"), selected_sample.get("patient_id", "--")),
                "Specimen": selected_sample.get("sample_type", "--"),
                "Collection": selected_sample.get("collection_date", "--"),
                "Status": selected_sample.get("status", "--"),
                "Storage": selected_sample.get("storage_location", "--"),
            }
            for label, value in detail_data.items():
                st.markdown(f"""
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:9px; margin-bottom:8px; font-size:12px;">
                    <b>{label}</b><br>{value}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("Selecciona una muestra para ver el detalle.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # REGISTRAR NUEVA MUESTRA
    # ------------------------------------------------------------------
    if st.session_state.get("show_sample_form", False):
        st.markdown('<div class="section-card"><p class="section-card-title">Register New Laboratory Sample</p>', unsafe_allow_html=True)

        if st.session_state.sample_code_temp is None:
            st.session_state.sample_code_temp = f"SMP-{int(time.time())}"

        col_a, col_b = st.columns(2)
        with col_a:
            sample_code = st.text_input("Sample ID", value=st.session_state.sample_code_temp, disabled=True)
            if patient_label_by_id:
                selected_patient_label = st.selectbox("Patient", list(patient_label_by_id.values()))
                patient_id = next(pid for pid, label in patient_label_by_id.items() if label == selected_patient_label)
            else:
                st.selectbox("Patient", ["No hay pacientes registrados"], disabled=True)
                patient_id = None
            sample_type = st.selectbox("Specimen Type", ["Whole Blood", "Plasma", "Tissue", "cfDNA Extract"])
        with col_b:
            collection_date = st.date_input("Collection Date", value=date.today())
            storage_location = st.text_input("Storage Location", placeholder="Freezer A1")
            initial_status = st.selectbox("Initial Status", ["Collected", "Received"])

        save_col, cancel_col = st.columns(2)
        with save_col:
            if st.button("Save Sample", use_container_width=True, key="save_new_sample", disabled=patient_id is None):
                payload = {
                    "sample_code": sample_code,
                    "patient_id": patient_id,
                    "sample_type": sample_type,
                    "collection_date": str(collection_date),
                    "received_date": str(collection_date),
                    "status": initial_status,
                    "storage_location": storage_location,
                }
                result = api_post("/samples/", json=payload)
                if result.ok:
                    st.success("Muestra registrada correctamente.")
                    st.cache_data.clear()
                    st.session_state.show_sample_form = False
                    st.session_state.sample_code_temp = None
                    time.sleep(0.8)
                    st.rerun()
                elif result.status_code == 403:
                    st.error("No tienes permiso para registrar muestras (falta el permiso 'sample_create').")
                else:
                    st.error(f"Error al registrar muestra: {result.error}")
        with cancel_col:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_sample_form = False
                st.session_state.sample_code_temp = None
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # ACTUALIZAR ESTADO DE MUESTRA
    # ------------------------------------------------------------------
    st.markdown('<div class="section-card"><p class="section-card-title">Update Sample Workflow Status</p>', unsafe_allow_html=True)
    if samples_data:
        status_samples = {s.get("sample_code"): s.get("id") for s in samples_data if s.get("sample_code")}
        selected_update_code = st.selectbox("Sample", list(status_samples.keys()), key="update_sample_selector")
        new_status = st.selectbox("New Status", ["Collected", "Received", "Processing", "Analysis Running", "Quality Control Review", "Clinical Review", "Report Ready"])

        if st.button("Update Status", use_container_width=True, key="update_sample_status"):
            sample_id = status_samples[selected_update_code]
            result = api_patch(f"/samples/{sample_id}", json={"status": new_status})
            if result.ok:
                st.success("Estado de flujo actualizado.")
                st.cache_data.clear()
                time.sleep(0.8)
                st.rerun()
            elif result.status_code == 403:
                st.error("No tienes permiso para actualizar muestras (falta el permiso 'sample_update').")
            else:
                st.error(f"Error al actualizar estado: {result.error}")
    else:
        st.info("No hay muestras disponibles para actualizar.")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# TAB: ANALYSIS
# ============================================================================
elif nav_selection == "analysis":
    st.markdown("<h2 class='welcome-header'>🧬 Sample Analysis</h2>", unsafe_allow_html=True)
    st.markdown('<p class="welcome-caption">Registro y consulta de resultados de análisis molecular.</p>', unsafe_allow_html=True)

    if st.session_state.user_role == "md":
        st.warning("Acceso restringido: el rol clínico (MD) no tiene autorización para registrar análisis computacionales.")
    else:
        samples_result = cached_get("/samples/", st.session_state.jwt_access_token)
        samples_data = samples_result.data if samples_result.ok else []

        if not samples_result.ok:
            st.warning(f"No se pudieron cargar las muestras: {samples_result.error}")
        elif not samples_data:
            st.info("Registra una muestra en la sección Samples antes de iniciar un análisis.")
        else:
            sample_options = {s["sample_code"]: s["id"] for s in samples_data if s.get("sample_code")}
            selected_code = st.selectbox("Muestra", list(sample_options.keys()))
            selected_id = sample_options[selected_code]

            st.markdown('<div class="section-card"><p class="section-card-title">Registrar nuevo resultado</p>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                pipeline_version = st.text_input("Pipeline Version", value="METHYLOX Analysis v1.0")
                qc_status = st.selectbox("QC Status", ["Pass", "Fail", "Review"])
            with c2:
                beta_score = st.number_input("Beta Score", min_value=0.0, max_value=1.0, step=0.0001, format="%.4f")
                classification = st.selectbox("Classification", ["Positive", "Negative", "Inconclusive"])

            if st.button("Guardar resultado de análisis", use_container_width=True):
                payload = {
                    "sample_id": selected_id,
                    "pipeline_version": pipeline_version,
                    "qc_status": qc_status,
                    "metrics": {"beta_score": beta_score},
                    "classification": classification,
                }
                result = api_post("/analysis/", json=payload)
                if result.ok:
                    st.success("Resultado de análisis registrado.")
                    st.cache_data.clear()
                    time.sleep(0.8)
                    st.rerun()
                elif result.status_code == 403:
                    st.error("No tienes permiso para registrar análisis (falta el permiso 'analysis_create').")
                else:
                    st.error(f"Error al registrar análisis: {result.error}")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-card"><p class="section-card-title">Resultados existentes para esta muestra</p>', unsafe_allow_html=True)
            existing_result = api_get(f"/analysis/sample/{selected_id}")
            if existing_result.ok and existing_result.data:
                for r in existing_result.data:
                    metrics = r.get("metrics") or {}
                    st.markdown(f"""
                    <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:10px; margin-bottom:8px; font-size:12px;">
                    <b>Pipeline:</b> {r.get('pipeline_version', '--')} &nbsp;|&nbsp;
                    <b>QC:</b> {r.get('qc_status', '--')} &nbsp;|&nbsp;
                    <b>Beta Score:</b> {metrics.get('beta_score', '--')} &nbsp;|&nbsp;
                    <b>Clasificación:</b> {r.get('classification', '--')}
                    </div>
                    """, unsafe_allow_html=True)
            elif existing_result.ok:
                st.caption("Sin resultados registrados todavía para esta muestra.")
            else:
                st.warning(f"No se pudieron cargar resultados previos: {existing_result.error}")

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
    st.markdown("<p class='welcome-caption'>Provisiona personal autorizado y administra permisos operativos dentro de METHYLOX™.</p>", unsafe_allow_html=True)

    # USER CREATION
    st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)
    with st.form("user_provisioning_form", clear_on_submit=True):
        st.markdown("#### Registrar nuevo miembro del personal")
        c1, c2 = st.columns(2)
        with c1:
            input_username = st.text_input("Username")
            input_email = st.text_input("Email")
            input_full_name = st.text_input("Full Name")
        with c2:
            input_password = st.text_input("Temporary Password", type="password")
            target_role = st.selectbox("System Role", ["admin", "cls", "md"], format_func=lambda x: {"admin": "Administrator", "cls": "Laboratory Scientist", "md": "Clinical Doctor"}[x])
        submit_btn = st.form_submit_button("Activate User & Grant Access")

    if submit_btn:
        payload_u = {
            "username": input_username,
            "email": input_email,
            "password": input_password,
            "full_name": input_full_name,
            "role": target_role
        }
        result = api_post("/users/", json=payload_u)
        if result.ok:
            st.success("Usuario creado correctamente.")
            st.cache_data.clear()
            st.rerun()
        else:
            st.error(result.error)
    st.markdown('</div>', unsafe_allow_html=True)

    # USER DIRECTORY
    st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)
    st.markdown('<p class="section-card-title">Registered Personnel</p>', unsafe_allow_html=True)
    users_result = cached_get("/users/", st.session_state.jwt_access_token)

    if users_result.ok and users_result.data:
        users_df = pd.DataFrame(users_result.data)
        cols = [c for c in ["username", "email", "full_name", "role", "active"] if c in users_df.columns]
        st.dataframe(users_df[cols], use_container_width=True, hide_index=True)
    elif users_result.ok:
        st.info("No users found.")
    else:
        st.warning(users_result.error)
    st.markdown('</div>', unsafe_allow_html=True)

    # PERMISSION MANAGEMENT
    st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)
    st.markdown('<p class="section-card-title">Permission Management</p>', unsafe_allow_html=True)

    if users_result.ok and users_result.data:
        user_options = {f"{u['username']} ({u['role']})": u["id"] for u in users_result.data}
        selected_user_label = st.selectbox("Select Employee", list(user_options.keys()))
        selected_user_id = user_options[selected_user_label]

        permissions_result = api_get("/access/permissions")
        current_permissions_result = api_get(f"/access/user/{selected_user_id}")
        current_permissions = []

        if current_permissions_result.ok:
            current_permissions = [p["name"] for p in current_permissions_result.data]

        if permissions_result.ok:
            permission_catalog = permissions_result.data
            st.markdown("#### Assigned Permissions")
            st.caption("Selecciona los permisos que deseas otorgar.")

            selected_permissions = []
            for permission in permission_catalog:
                checked = st.checkbox(
                    permission["name"],
                    value=permission["name"] in current_permissions,
                    key=f"user_{selected_user_id}_perm_{permission['id']}"
                )
                if checked:
                    selected_permissions.append(permission)

            if st.button("Save Permission Changes", use_container_width=True):
                desired_names = {p["name"] for p in selected_permissions}
                current_names = set(current_permissions)

                for permission in permission_catalog:
                    if permission["name"] in desired_names and permission["name"] not in current_names:
                        api_post("/access/assign", json={
                            "user_id": selected_user_id,
                            "permission_id": permission["id"]
                        })

                st.success("Permisos actualizados correctamente.")
                st.cache_data.clear()
                st.rerun()

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
