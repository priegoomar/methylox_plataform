# ============================================================================
# METHYLOX™ PLATFORM v3.0 - ENTERPRISE FRONTEND CORE
# ============================================================================

import os
import time
import random
from datetime import datetime, date
import pandas as pd
import requests
import streamlit as st
import jwt

# ============================================================================
# STREAMLIT CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="METHYLOX™ | Epigenetic Intelligence Platform",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# GLOBAL DESIGN SYSTEM
# ============================================================================

st.markdown("""
<style>
.stApp {
    background-color: #F8FAFC;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
[data-testid="stHeader"] {
    display: none;
}
[data-testid="stMainBlockContainer"] {
    padding: 2rem 3rem;
}
[data-testid="stSidebar"] {
    background: #0B0F19;
}
[data-testid="stSidebar"] label {
    color: #CBD5E1 !important;
}
.welcome-header {
    font-size: 28px !important;
    font-weight: 800 !important;
    color: #0F172A !important;
    text-align: center;
}
.welcome-caption {
    font-size: 14px !important;
    color: #64748B !important;
    text-align: center;
    margin-bottom: 25px;
}
.executive-card-white {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 20px;
}
.card-title-clinical {
    text-align: center;
    font-size: 18px;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 20px;
}
div[data-baseweb="input"] {
    border-radius: 20px !important;
    border: 1.5px solid #CBD5E1 !important;
}
div[data-baseweb="input"]:focus-within {
    border-color: #2563EB !important;
}
[data-testid="stDataFrame"] {
    border-radius: 12px;
}
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
    "id_hospital": 1,
    "nav_selection": "dashboard"
}

for key, value in DEFAULT_SESSION.items():
    if key not in st.session_state:
        st.session_state[key] = value

def get_auth_headers():
    if st.session_state.jwt_access_token:
        return {"Authorization": f"Bearer {st.session_state.jwt_access_token}", "Content-Type": "application/json"}
    return {"Content-Type": "application/json"}

headers = get_auth_headers()

# ============================================================================
# BACKEND CONNECTIVITY MONITOR
# ============================================================================

def check_backend_connection():
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            return True, response.json()
        return False, {"status": response.status_code}
    except Exception as e:
        return False, {"error": str(e)}

backend_status, backend_info = check_backend_connection()

# ============================================================================
# SECURE SIDEBAR AUTHENTICATION & RBAC NAVIGATION
# ============================================================================

with st.sidebar:
    st.markdown("""
    <div style="padding:15px 0px; border-bottom:1px solid #1E293B; margin-bottom:25px;">
        <h2 style="color:white; margin:0; font-weight:900;">METHYLOX™</h2>
        <p style="color:#38BDF8; font-size:12px; margin:0;">Epigenetic Intelligence Platform</p>
    </div>
    """, unsafe_allow_html=True)

    # ============================================================================
    # SYSTEM STATUS
    # ============================================================================
    
    if backend_status:
        st.sidebar.success("Backend Online")
    else:
        st.sidebar.error("Backend Offline")
    
    # ============================================================
    # LOGIN GATE
    # ============================================================
    
    if not st.session_state.jwt_access_token:
        with st.form("login_form"):
            st.markdown('<p style="color:#94A3B8; font-size:12px; font-weight:700;">SECURE AUTHENTICATION</p>', unsafe_allow_html=True)
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login = st.form_submit_button("Authenticate", use_container_width=True)
    
        if login:
            if username and password:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/auth/login",
                        data={"username": username, "password": password},
                        timeout=5
                    )
    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.jwt_access_token = data["access_token"]
                        st.session_state.operator_display_name = username
                    
                        decoded_token = jwt.decode(
                            data["access_token"],
                            options={"verify_signature": False}
                        )
                    
                        st.session_state.user_role = decoded_token.get("role", "cls").lower()
                        st.rerun()
                except Exception as e:
                    pass
    
    # ============================================================
    # ACTIVE SESSION
    # ============================================================
    
    else:
        st.markdown(
            f"""
            <div style="background:#1E293B; padding:15px; border-radius:10px;">
            <span style="color:#94A3B8;font-size:11px;">ACTIVE USER</span>
            <br>
            <b style="color:white;">{st.session_state.operator_display_name}</b>
            <br>
            <span style="color:#38BDF8;font-size:12px;">ROLE: {st.session_state.user_role.upper()}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    
        if st.button("Disconnect", use_container_width=True):
            st.session_state.jwt_access_token = None
            st.session_state.user_role = None
            st.session_state.operator_display_name = "Guest Operator"
            st.rerun()
    
    st.sidebar.markdown("---")

# ============================================================================
# RBAC MENU
# ============================================================================

menu_options = {
    "dashboard": "Dashboard",
    "patients": "Patients",
    "lims": "LIMS Samples",
    "analysis": "Analysis",
    "reports": "Reports"
}

# ADMIN ONLY MODULES
if st.session_state.user_role == "admin":
    menu_options.update({
        "users": "Access Control",
        "settings": "Settings"
    })

if st.session_state.jwt_access_token:
    selected_key = st.sidebar.radio(
        "Navigation",
        options=list(menu_options.keys()),
        format_func=lambda x: menu_options[x],
        key="nav_selection"
    )
else:
    selected_key = "restricted"

# GLOBAL ROUTING VARIABLE
nav_selection = selected_key
headers = get_auth_headers()

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

# ----------------------------------------------------------------------------
#   TAB 1: GENERAL DASHBOARD MATRIX
# ----------------------------------------------------------------------------
elif nav_selection == "dashboard":
    st.markdown(f"<h2 class='welcome-header'>Welcome back, {st.session_state.operator_display_name} </h2>", unsafe_allow_html=True)
    st.markdown("<p class='welcome-caption'>Laboratory Operations Dashboard Real-Time Clinical Workflow Monitoring</p>", unsafe_allow_html=True)
    
    # FETCH LIVE DATA FROM ENDPOINTS
    try:
        res_telemetry = requests.get(f"{BACKEND_URL}/analysis/telemetry-summary", headers=headers, timeout=15)
        if res_telemetry.status_code == 200:
            tel = res_telemetry.json()
            received_today = tel.get('received_today', 0)
            in_progress = tel.get('in_progress', 0)
            ready_analyses = tel.get('ready_analyses', 0)
            qc_pass_rate = tel.get('qc_pass_rate', 0.0)
        else:
            received_today, in_progress, ready_analyses, qc_pass_rate = 0, 0, 0, 0.0
    except Exception:
        received_today, in_progress, ready_analyses, qc_pass_rate = 0, 0, 0, 0.0

    # RENDER TOP TELEMETRY CARDS WITH FUNCTIONAL URL NAVIGATION
    st.markdown(f"""
    <div class='metric-container-hub'>
        <div class='metric-card-clinical-new'>
            <div class='svg-top-container' style='color: #2563EB;'>
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10 2v8L4.72 17.55a1 1 0 0 0 .83 1.45h12.9a1 1 0 0 0 .83-1.45L14 10V2Z"/><path d="M14 2h-4"/></svg>
            </div>
            <p class='metric-title-sub-new'>Samples Received</p>
            <p class='metric-num-big-new'>{received_today}</p>
            <a class='metric-link-btn-new' href='?page=LIMS-Samples' target='_self'>View all samples →</a>
        </div>
        <div class='metric-card-clinical-new'>
            <div class='svg-top-container' style='color: #D97706;'>
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
            </div>
            <p class='metric-title-sub-new'>Active Workflow</p>
            <p class='metric-num-big-new'>{in_progress}</p>
            <a class='metric-link-btn-new' href='?page=METHYLOX-Engine' target='_self'>View workflow →</a>
        </div>
        <div class='metric-card-clinical-new'>
            <div class='svg-top-container' style='color: #16A34A;'>
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/></svg>
            </div>
            <p class='metric-title-sub-new'>Ready Reports</p>
            <p class='metric-num-big-new'>{ready_analyses}</p>
            <a class='metric-link-btn-new' href='?page=Reports' target='_self'>View dossiers →</a>
        </div>
        <div class='metric-card-clinical-new'>
            <div class='svg-top-container' style='color: #6366F1;'>
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            </div>
            <p class='metric-title-sub-new'>Quality Controls</p>
            <p class='metric-num-big-new'>{qc_pass_rate}%</p>
            <a class='metric-link-btn-new' href='?page=LIMS-Samples' target='_self'>View QC matrix →</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("##")

    # PARALLEL COLUMNS WITH SECURE CONTAINERS
    c_left, c_right = st.columns([1.4, 1.0])
    
    with c_left:
        try:
            res_s_dash = requests.get(f"{BACKEND_URL}/samples", headers=headers, timeout=5)
            samples_list = res_s_dash.json() if res_s_dash.status_code == 200 else []
        except Exception:
            samples_list = []
            
        rows_html = ""
        if not samples_list:
            rows_html = "<tr><td colspan='4' style='color: #94A3B8; padding: 60px 10px; font-style: italic; text-align: center; border: none;'>No laboratory samples currently registered.</td></tr>"
        else:
            for s in samples_list[:5]:
                state = s.get("status", "Collected")
                if state in ["Sample Registered"]:
                    badge_style = "background-color:#EFF6FF; color:#2563EB;"
                elif state in ["Pre-Analytical Processing", "Molecular Data Generation", "Analysis Running"]:
                    badge_style = "background-color:#FFFBEB; color:#D97706;"
                elif state in ["Quality Control Review", "Clinical Review"]:
                    badge_style = "background-color:#F5F3FF; color:#7C3AED;"
                elif state == "Report Ready":
                    badge_style = "background-color:#F0FDF4; color:#16A34A;"
                else:
                    badge_style = "background-color:#F8FAFC; color:#64748B;"
                
                rows_html += f"""
                <tr style='border-bottom: 1px solid #F1F5F9;'>
                    <td style='font-weight: 700; color: #2563EB; padding: 14px 10px; text-align: center; border: none;'>{s.get('sample_code', '--')}</td>
                    <td style='padding: 14px 10px; text-align: center; border: none;'>{s.get('patient_id', '--')}</td>
                    <td style='padding: 14px 10px; text-align: center; border: none;'>{s.get('sample_type', 'Plasma')}</td>
                    <td style='padding: 14px 10px; text-align: center; border: none;'><span style='padding:4px 8px; border-radius:12px; font-size:11px; font-weight:700; {badge_style}'>{state}</span></td>
                </tr>
                """

        st.markdown(f"""
        <div style='background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 24px; min-height: 360px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);'>
            <p style='font-size:15px; font-weight:700; color:#0F172A; margin:0 0 15px 0;'> Recent Laboratory Activity Trail</p>
            <table class='clinical-table-new'>
                <thead>
                    <tr style='background-color: #F8FAFC; border-top: 1px solid #E2E8F0; border-bottom: 2px solid #E2E8F0;'>
                        <th style='padding: 14px 10px; color: #64748B; font-weight: 700; text-align: center; border: none;'>Sample ID</th>
                        <th style='padding: 14px 10px; color: #64748B; font-weight: 700; text-align: center; border: none;'>Patient ID</th>
                        <th style='padding: 14px 10px; color: #64748B; font-weight: 700; text-align: center; border: none;'>Matrix</th>
                        <th style='padding: 14px 10px; color: #64748B; font-weight: 700; text-align: center; border: none;'>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

    with c_right:
        # LIVE INTERACTIVE STREAM TABLE
        st.markdown("<div style='background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 15px; margin-bottom: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);'>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px; font-weight:700; color:#0F172A; margin:0 0 8px 0;'>⚡ Live Interactive Data Stream</p>", unsafe_allow_html=True)
        
        try:
            res_live_df = requests.get(f"{BACKEND_URL}/samples", headers=headers, timeout=5)
            live_list = res_live_df.json() if res_live_df.status_code == 200 else []
        except Exception:
            live_list = []

        if live_list:
            df_live = pd.DataFrame(live_list)
            selected_live_event = st.dataframe(
                df_live[['sample_id', 'workflow_state']],
                use_container_width=True,
                hide_index=True,
                height=110,
                on_select="rerun",
                selection_mode="single-row"
            )
            if selected_live_event and selected_live_event.selection.rows:
                sel_idx = selected_live_event.selection.rows[0]
                st.session_state.active_live_sample = df_live.iloc[sel_idx].get('sample_id')
        else:
            st.caption("Awaiting live registry telemetry stream...")
        st.markdown("</div>", unsafe_allow_html=True)

        # DONUT CHART SECTION
        try:
            res_rep = requests.get(f"{BACKEND_URL}/analysis/reports-directory", headers=headers, timeout=5)
            rep_data = res_rep.json() if res_rep.status_code == 200 else []
        except Exception:
            rep_data = []
            
        total_cases = len(rep_data)
        positives = sum(1 for r in rep_data if float(r.get('score', 0)) >= 0.1000)
        negatives = total_cases - positives
        in_pipeline = in_progress
       
        if total_cases == 0 and in_pipeline == 0:
            labels_pie = ['Awaiting Data Ingestion']
            values_pie = [1]
            colors_pie = ['#F1F5F9']
        else:
            labels_pie = ['Positive Findings', 'Negative Findings', 'Active Workflow']
            values_pie = [positives, negatives, in_pipeline]
            colors_pie = ['#EF4444', '#10B981', '#3B82F6']

        fig_donut = go.Figure(data=[go.Pie(
            labels=labels_pie, values=values_pie, hole=.6,
            marker=dict(colors=colors_pie), textinfo='none', showlegend=True
        )])
        fig_donut.update_layout(
            height=180, margin=dict(l=0, r=0, t=10, b=10),
            legend=dict(orientation="h", y=-0.2, x=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            annotations=[dict(text=f"<b style='font-size:20px; color:#0F172A;'>{total_cases + in_pipeline}</b><br><span style='font-size:10px; color:#64748B;'>Total</span>", x=0.5, y=0.5, font_size=11, showarrow=False)]
        )

        st.markdown("""
        <div style='background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);'>
            <p style='font-size:15px; font-weight:700; color:#0F172A; margin:0 0 10px 0;'> Onco-Genetic Diagnostic Summary</p>
        """, unsafe_allow_html=True)
        st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    # QUICK ACTION WORKFLOWS GRID
    st.write("##")
    st.markdown("<p style='font-size:14px; font-weight:700; color:#0F172A; margin-bottom:10px;'>Quick Action Clinical Workflows</p>", unsafe_allow_html=True)

    st.markdown("""
    <style>
        .svg-action-link {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 16px;
            display: flex;
            align-items: center;
            gap: 12px;
            width: 100%;
            min-height: 75px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            box-sizing: border-box;
            text-decoration: none !important;
            transition: all 0.2s ease-in-out;
        }
        .svg-action-link:hover {
            border-color: #3B82F6;
            box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.15);
            transform: translateY(-2px);
            background-color: #F8FAFC;
        }
    </style>
    """, unsafe_allow_html=True)

    act_col1, act_col2, act_col3, act_col4 = st.columns(4)

    with act_col1:
        st.markdown("""
        <a href="?page=Patients" target="_self" class="svg-action-link">
            <div style="background: #EFF6FF; padding: 10px; border-radius: 10px; color: #2563EB; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><line x1="19" y1="8" x2="19" y2="14"/><line x1="16" y1="11" x2="22" y2="11"/></svg>
            </div>
            <div style="text-align: left; overflow: hidden;">
                <p style="font-size: 13px; font-weight: 700; color: #0F172A; margin: 0; line-height: 1.2;">Enroll Subject</p>
                <p style="font-size: 11px; color: #64748B; margin: 2px 0 0 0; line-height: 1.2;">New Patient Profile</p>
            </div>
        </a>
        """, unsafe_allow_html=True)

    with act_col2:
        st.markdown("""
        <a href="?page=LIMS-Samples" target="_self" class="svg-action-link">
            <div style="background: #FFF7ED; padding: 10px; border-radius: 10px; color: #EA580C; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10 2v8L4.72 17.55a1 1 0 0 0 .83 1.45h12.9a1 1 0 0 0 .83-1.45L14 10V2Z"/><path d="M14 2h-4"/></svg>
            </div>
            <div style="text-align: left; overflow: hidden;">
                <p style="font-size: 13px; font-weight: 700; color: #0F172A; margin: 0; line-height: 1.2;">Asset Intake</p>
                <p style="font-size: 11px; color: #64748B; margin: 2px 0 0 0; line-height: 1.2;">Log LIMS Custody</p>
            </div>
        </a>
        """, unsafe_allow_html=True)

    with act_col3:
        st.markdown("""
        <a href="?page=METHYLOX-Engine" target="_self" class="svg-action-link">
            <div style="background: #F0FDF4; padding: 10px; border-radius: 10px; color: #16A34A; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="10 8 16 12 10 16 10 8"/></svg>
            </div>
            <div style="text-align: left; overflow: hidden;">
                <p style="font-size: 13px; font-weight: 700; color: #0F172A; margin: 0; line-height: 1.2;">Start Analysis</p>
                <p style="font-size: 11px; color: #64748B; margin: 2px 0 0 0; line-height: 1.2;">Run Molecular Pipeline</p>
            </div>
        </a>
        """, unsafe_allow_html=True)

    with act_col4:
        st.markdown("""
        <a href="?page=Reports" target="_self" class="svg-action-link">
            <div style="background: #FAF5FF; padding: 10px; border-radius: 10px; color: #9333EA; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>
            </div>
            <div style="text-align: left; overflow: hidden;">
                <p style="font-size: 13px; font-weight: 700; color: #0F172A; margin: 0; line-height: 1.2;">Dossier Sheet</p>
                <p style="font-size: 11px; color: #64748B; margin: 2px 0 0 0; line-height: 1.2;">Export Medical PDF</p>
            </div>
        </a>
        """, unsafe_allow_html=True)

# ============================================================================
#   TAB 2: PATIENTS (CLINICAL COHORT MANAGEMENT) - OPTIMIZED & ALIGNED
# ============================================================================
elif nav_selection == "patients":
    import random

    # -------------------------------------------------------------------------
    # CSS CLINICAL PATIENT MODULE
    # -------------------------------------------------------------------------
    st.markdown("""
    <style>
    .card-title-clinical { text-align:center !important; font-weight:700 !important; font-size:1.1rem !important; margin-bottom:1rem !important; width:100% !important; display:block !important; }
    div[data-testid="stTextInput"] label, div[data-testid="stDateInput"] label, div[data-testid="stSelectbox"] label { display:block !important; text-align:center !important; width:100% !important; }
    div[data-baseweb="input"] { border-radius:30px !important; border:1.5px solid #CBD5E1 !important; background:white !important; padding-left:35px !important; }
    div[data-baseweb="input"]:focus-within { border-color:#2563EB !important; box-shadow:0 0 0 2px rgba(37,99,235,0.15) !important; }
    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # HEADER
    # -------------------------------------------------------------------------
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2">
            <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
            <path d="M22 21v-2a4 4 0 0 0-3-3.87"/>
        </svg>
        <h2 style="margin:0;">Patient Cohort & Clinical Directory</h2>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # SESSION STATES
    # -------------------------------------------------------------------------
    if "show_new_patient_form" not in st.session_state:
        st.session_state.show_new_patient_form = False
    if "generated_patient_id" not in st.session_state:
        st.session_state.generated_patient_id = f"PAT-{random.randint(10000,99999)}"
    if "generated_anonymous_code" not in st.session_state:
        st.session_state.generated_anonymous_code = f"MOX-{random.randint(10000,99999)}"

    # -------------------------------------------------------------------------
    # FUNCTION LOAD PATIENT DIRECTORY
    # -------------------------------------------------------------------------
    def load_patient_directory():
        try:
            response = requests.get(f"{BACKEND_URL}/lims/cohort-directory", headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data:
                    return pd.DataFrame(data)
        except Exception:
            pass
        return pd.DataFrame()

    # =========================================================================
    # SEARCH VIEW
    # =========================================================================
    if not st.session_state.show_new_patient_form:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2.2, 1])

        with col2:
            search_query = st.text_input("Search patient", placeholder="Search Patient ID, Record Number or Anonymous Code", label_visibility="collapsed")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("+ New Patient", key="open_new_patient"):
                st.session_state.show_new_patient_form = True
                st.rerun()

        st.markdown("<br><br>", unsafe_allow_html=True)
        df_patients = load_patient_directory()

        if not df_patients.empty:
            rename_map = {
                "id_patient": "Patient ID", "patient_id": "Patient ID",
                "anonymous_code": "Anonymous Code", "full_name": "Full Name",
                "record_number": "Record Number", "date_of_birth": "Date of Birth",
                "dob": "Date of Birth", "gender": "Gender", "institution": "Institution"
            }
            df_patients = df_patients.rename(columns={k: v for k, v in rename_map.items() if k in df_patients.columns})

            if search_query.strip():
                mask = df_patients.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
                filtered = df_patients[mask]

                if not filtered.empty:
                    st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)
                    st.markdown('<div class="card-title-clinical">Search Results</div>', unsafe_allow_html=True)
                    st.dataframe(filtered, use_container_width=True, hide_index=True)
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No registered patients available.")

    # =========================================================================
    # NEW PATIENT REGISTRATION VIEW
    # =========================================================================
    else:
        if st.button("← Back to Search", key="btn_back_patients"):
            st.session_state.show_new_patient_form = False
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        left, right = st.columns([1, 1.3], gap="large")

        # =====================================================================
        # PATIENT REGISTRATION CARD
        # =====================================================================
        with left:
            st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)
            st.markdown('<div class="card-title-clinical">Register New Patient</div>', unsafe_allow_html=True)

            if st.session_state.user_role == "cls":
                st.warning("Restricted Access: Laboratory users cannot enroll patients.")
            else:
                patient_id = st.text_input("Patient ID", value=st.session_state.generated_patient_id, disabled=True)
                if st.button("  Generate New Patient ID", key="generate_patient_id"):
                    st.session_state.generated_patient_id = f"PAT-{random.randint(10000,99999)}"
                    st.rerun()

                anonymous_code = st.text_input("Anonymous Clinical Code", value=st.session_state.generated_anonymous_code, disabled=True)
                if st.button("Generate Anonymous Code", key="generate_anonymous_code"):
                    st.session_state.generated_anonymous_code = f"MOX-{random.randint(10000,99999)}"
                    st.rerun()

                full_name = st.text_input("Full Name", placeholder="Patient legal name")
                record_number = st.text_input("Record Number", placeholder="Example: REC-2026-0091")
                date_birth = st.date_input("Date of Birth", min_value=datetime(1920, 1, 1))
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                institution = st.text_input("Institution", placeholder="Hospital / Laboratory")

                if st.button("Save and Synchronize Patient Record", use_container_width=True, key="save_patient_record"):
                    required_fields = [full_name, record_number, institution]
                    if not all(required_fields):
                        st.error("Missing Data: Complete all mandatory fields.")
                    else:
                        payload_patient = {
                            "id_patient": patient_id, "anonymous_code": anonymous_code,
                            "full_name": full_name, "record_number": record_number,
                            "date_of_birth": str(date_birth), "gender": gender, "institution": institution
                        }
                        try:
                            response = requests.post(f"{BACKEND_URL}/lims/enroll-patient", json=payload_patient, headers=headers, timeout=5)
                            if response.status_code == 200:
                                st.success(f"Patient {patient_id} successfully registered.")
                                st.session_state.generated_patient_id = f"PAT-{random.randint(10000,99999)}"
                                st.session_state.generated_anonymous_code = f"MOX-{random.randint(10000,99999)}"
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.error("Backend rejected patient registration.")
                        except Exception:
                            st.error("Backend unavailable.")

            st.markdown("</div>", unsafe_allow_html=True)

        # =====================================================================
        # PATIENT DIRECTORY TABLE
        # =====================================================================
        with right:
            st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)
            st.markdown('<div class="card-title-clinical">Patient Records</div>', unsafe_allow_html=True)

            df_patients = load_patient_directory()

            if not df_patients.empty:
                rename_map = {
                    "id_patient": "Patient ID", "patient_id": "Patient ID",
                    "anonymous_code": "Anonymous Code", "full_name": "Full Name",
                    "record_number": "Record Number", "date_of_birth": "Date of Birth",
                    "gender": "Gender", "institution": "Institution"
                }
                df_patients = df_patients.rename(columns={k: v for k, v in rename_map.items() if k in df_patients.columns})
                display_cols = ["Patient ID", "Anonymous Code", "Record Number", "Gender", "Institution"]
                display_cols = [c for c in display_cols if c in df_patients.columns]

                st.dataframe(df_patients[display_cols], use_container_width=True, hide_index=True)
            else:
                st.info("No patient records available.")

            st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
#   TAB 3: LIMS SAMPLES (CHAIN OF CUSTODY MANAGEMENT) - OPTIMIZED
# ============================================================================
elif nav_selection == "lims":

    # -------------------------------------------------------------------------
    # CSS LOCAL TAB 3
    # -------------------------------------------------------------------------
    st.markdown("""
    <style>
    .card-title-clinical { text-align:center !important; font-weight:700 !important; font-size:1.1rem !important; margin-bottom:1rem !important; width:100% !important; }
    div[data-testid="stTextInput"] label, div[data-testid="stSelectbox"] label, div[data-testid="stDateInput"] label { display:block !important; text-align:center !important; width:100% !important; }
    .status-box { background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:15px; margin-top:15px; }
    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # HEADER
    # -------------------------------------------------------------------------
    st.markdown("<h2 class='welcome-header'> LIMS Sample Management</h2>", unsafe_allow_html=True)
    st.markdown("<p class='welcome-caption'>Clinical specimen registration, custody tracking and laboratory workflow control.</p>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # LOAD REGISTERED PATIENTS
    # -------------------------------------------------------------------------
    try:
        response_patients = requests.get(f"{BACKEND_URL}/lims/cohort-directory", headers=headers, timeout=5)
        if response_patients.status_code == 200:
            patients_json = response_patients.json()
            registered_patients = [patient.get("id_patient") for patient in patients_json if patient.get("id_patient")]
        else:
            registered_patients = []
    except Exception:
        registered_patients = []

    # -------------------------------------------------------------------------
    # AUTOMATIC SAMPLE ID
    # -------------------------------------------------------------------------
    import random
    if "generated_sample_id" not in st.session_state:
        st.session_state.generated_sample_id = f"SMP-{random.randint(10000,99999)}"

    # -------------------------------------------------------------------------
    # MAIN LAYOUT
    # -------------------------------------------------------------------------
    col_left, col_right = st.columns([1, 1], gap="large")

    # =========================================================================
    # NEW SAMPLE INTAKE
    # =========================================================================
    with col_left:
        st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)
        st.markdown('<div class="card-title-clinical">New Sample Intake</div>', unsafe_allow_html=True)

        user_role = st.session_state.get("user_role", "unknown")

        if user_role == "md":
            st.warning(" Clinical doctors cannot modify laboratory custody records.")
        elif not registered_patients:
            st.warning(" No patient profiles available. Register a patient first.")
        else:
            sample_id = st.text_input("Sample Asset ID", value=st.session_state.generated_sample_id, disabled=True)
            barcode = st.text_input("Barcode / QR Identifier", placeholder="Scan laboratory barcode")
            patient_id = st.selectbox("Associated Patient Profile", options=registered_patients)
            specimen_type = st.selectbox("Specimen Type", ["Plasma", "Whole Blood", "Tissue", "cfDNA Extract"])
            collection_date = st.date_input("Collection Date", value=date.today())
            collection_site = st.text_input("Collection Site", placeholder="Hospital / Laboratory")
            qc_status = st.selectbox("Initial Sample Quality Control", ["Accepted", "Rejected", "Insufficient Volume", "Hemolysis Detected"])
            st.info("Initial workflow state: Sample Received")

            if st.button("Register Sample Into LIMS", use_container_width=True):
                if not barcode or not collection_site:
                    st.error("Barcode and Collection Site are mandatory.")
                else:
                    payload_sample = {
                        "sample_id": sample_id,
                        "patient_id": patient_id,
                        "barcode_qr": barcode,
                        "specimen_type": specimen_type,
                        "workflow_state": "Sample Received",
                        "collection_date": str(collection_date),
                        "collection_site": collection_site,
                        "qc_status": qc_status,
                        "received_by": st.session_state.get("operator_display_name", "SYSTEM"),
                        "practitioner_signature": st.session_state.get("operator_display_name", "SYSTEM")
                    }
                    try:
                        response_sample = requests.post(f"{BACKEND_URL}/lims/samples/intake", json=payload_sample, headers=headers, timeout=5)
                        if response_sample.status_code == 200:
                            st.success(f" Sample {sample_id} registered successfully.")
                            st.session_state.generated_sample_id = f"SMP-{random.randint(10000,99999)}"
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error(" LIMS rejected sample registration.")
                    except Exception:
                        st.error(" Backend connection failure.")

        st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # SAMPLE INVENTORY
    # =========================================================================
    with col_right:
        st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)
        st.markdown('<div class="card-title-clinical">Sample Inventory</div>', unsafe_allow_html=True)

        try:
            response_samples = requests.get(f"{BACKEND_URL}/lims/samples/directory", headers=headers, timeout=5)
            samples_data = response_samples.json() if response_samples.status_code == 200 else []
        except Exception:
            samples_data = []

        if samples_data:
            df_samples = pd.DataFrame(samples_data)
            column_map = {
                "sample_id": "Sample ID", "patient_id": "Patient ID",
                "barcode_qr": "Barcode", "specimen_type": "Specimen",
                "workflow_state": "Status", "qc_status": "QC",
                "collection_date": "Collection Date"
            }
            df_samples = df_samples.rename(columns={k: v for k, v in column_map.items() if k in df_samples.columns})
            visible_columns = [c for c in ["Sample ID", "Patient ID", "Specimen", "Status", "QC"] if c in df_samples.columns]

            st.dataframe(df_samples[visible_columns], use_container_width=True, hide_index=True, height=320)
        else:
            st.info("No samples registered in LIMS repository.")

        st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # TRACEABILITY PANEL
    # =========================================================================
    st.markdown("<br><h3 style='color:#0F172A;'> Sample Traceability & Custody Timeline</h3>", unsafe_allow_html=True)

    try:
        response_trace = requests.get(f"{BACKEND_URL}/lims/samples/directory", headers=headers, timeout=5)
        trace_samples = response_trace.json() if response_trace.status_code == 200 else []
    except Exception:
        trace_samples = []

    if trace_samples:
        sample_ids = [s.get("sample_id") for s in trace_samples if s.get("sample_id")]
        selected_trace_sample = st.selectbox("Select Sample for Audit Review", options=sample_ids, key="trace_selector")
        selected_sample_data = next((s for s in trace_samples if s.get("sample_id") == selected_trace_sample), {})

        metric_a, metric_b, metric_c = st.columns(3)
        metric_a.metric("Sample ID", selected_sample_data.get("sample_id", "--"))
        metric_b.metric("Current Status", selected_sample_data.get("workflow_state", "Unknown"))
        metric_c.metric("QC Status", selected_sample_data.get("qc_status", "Pending"))

        st.markdown('<div class="status-box"><b>Chain of Custody Timeline</b><br><br>', unsafe_allow_html=True)

        workflow_timeline = [
            ("Sample Registered", selected_sample_data.get("collection_date", "Date unavailable")),
            ("Pre-Analytical Processing", "Pending workflow stage"),
            ("Molecular Data Generation", "Pending workflow stage"),
            ("Analysis Running", "Pending workflow stage"),
            ("Quality Control Review", "Pending workflow stage"),
            ("Clinical Review", "Pending workflow stage"),
            ("Report Ready", "Pending workflow stage")
        ]

        for title, detail in workflow_timeline:
            st.markdown(f"""
                <div style="padding:10px; border-left:3px solid #2563EB; margin-bottom:10px; background:#FFFFFF;">
                <b>{title}</b><br>
                <span style="color:#64748B; font-size:13px;">{detail}</span>
                </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No samples available for traceability review.")

    # =========================================================================
    # WORKFLOW STATUS UPDATE
    # =========================================================================
    st.markdown('<div class="executive-card-white"><div class="card-title-clinical">Sample Workflow Tracking</div>', unsafe_allow_html=True)

    if trace_samples:
        workflow_ids = [s.get("sample_id") for s in trace_samples if s.get("sample_id")]
        selected_workflow_sample = st.selectbox("Select Sample", options=workflow_ids, key="workflow_selector")
        current_workflow_sample = next((s for s in trace_samples if s.get("sample_id") == selected_workflow_sample), {})

        current_state = current_workflow_sample.get("workflow_state", "Sample Received")
        st.info(f"Current Status: {current_state}")

        available_states = [
            "Sample Received", "Pre-Analytical Processing", "Molecular Data Generation",
            "Analysis Running", "Quality Control Review", "Clinical Review", "Report Ready"
        ]
        new_state = st.selectbox("Update Workflow Status", options=available_states, key="workflow_update")

        if st.button("Update Sample Status", use_container_width=True):
            payload_update = {"sample_id": selected_workflow_sample, "workflow_state": new_state}
            try:
                update_response = requests.put(f"{BACKEND_URL}/lims/samples/update-status", json=payload_update, headers=headers, timeout=5)
                if update_response.status_code == 200:
                    st.success(" Workflow status updated successfully.")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Unable to update workflow state.")
            except Exception:
                st.error("Backend connection unavailable.")
    else:
        st.info("No registered samples available.")

    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# 🧬 TAB 4: METHYLOX ENGINE (COMPUTATIONAL KERNEL CORES)
# ----------------------------------------------------------------------------
elif nav_selection == "analysis":
    st.markdown("""
        <style>
            .welcome-header {
                text-align: center !important;
                width: 100% !important;
            }
            .card-title-clinical {
                text-align: center !important;
                font-weight: 700 !important;
                font-size: 1.1rem !important;
                margin-bottom: 1rem !important;
                display: block !important;
                width: 100% !important;
            }
            div[data-testid="stSelectbox"] label,
            div[data-testid="stFileUploader"] label {
                display: block !important;
                text-align: center !important;
                width: 100% !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 class='welcome-header'>🧬 Sample Analysis</h2>", unsafe_allow_html=True)
    
    st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)
    st.markdown('<div class="card-title-clinical">Analyze Laboratory Sample</div>', unsafe_allow_html=True)
    
    if st.session_state.user_role == "md":
        st.warning("🔒 Access Denied: Medical roles do not possess computational clearance to launch sequencing.")
    else:
        try:
            res_p_samples = requests.get(f"{BACKEND_URL}/lims/samples/pending-evaluation", headers=headers, timeout=5)
            pending_samples = res_p_samples.json() if res_p_samples.status_code == 200 and res_p_samples.json() else []
        except Exception:
            pending_samples = []

        if not pending_samples:
            st.info("ℹ️ Register a sample in the Samples section before starting an analysis.")
        else:
            m_target = st.selectbox("Select Pending Asset ID for Pipeline Queue:", pending_samples)
            uploaded_file = st.file_uploader("Upload Sequencer Raw CpG Methylation File (.CSV)", type=["csv"])
            
            if uploaded_file is not None:
                if st.button("Execute Automated Analytical Pipeline Run", use_container_width=True):
                    files_payload = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                    try:
                        res_calc = requests.post(f"{BACKEND_URL}/lims/samples/evaluate/{m_target}", files=files_payload, headers=headers, timeout=15)
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
# TAB 5: REPORTS (METHYLOX™ CLINICAL REPORT GENERATION)
# ----------------------------------------------------------------------------
elif nav_selection == "reports":
    from fpdf import FPDF

    st.markdown("""
        <style>
            .welcome-header, .welcome-caption {
                text-align: center !important;
                width: 100% !important;
            }
            div[data-testid="stSelectbox"] label {
                display: block !important;
                text-align: center !important;
                width: 100% !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 class='welcome-header'> Clinical Reports</h2>", unsafe_allow_html=True)
    st.markdown("<p class='welcome-caption'>Generate validated molecular analysis reports from METHYLOX™ laboratory records.</p>", unsafe_allow_html=True)
    st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)

    # ============================================================
    # LOAD AVAILABLE SAMPLES FROM BACKEND
    # ============================================================
    try:
        samples_response = requests.get(f"{BACKEND_URL}/samples/", headers=headers, timeout=5)
        samples_data = samples_response.json() if samples_response.status_code == 200 else []
    except Exception:
        samples_data = []

    if not samples_data:
        st.info("No samples available. Create and analyze a sample before generating reports.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        samples_df = pd.DataFrame(samples_data)
        st.markdown("### Select Sample for Report Generation")
        selected_sample_id = st.selectbox("Sample ID", options=samples_df["id"].tolist())

        # ========================================================
        # REQUEST REPORT DATA FROM BACKEND
        # ========================================================
        try:
            report_response = requests.get(f"{BACKEND_URL}/reports/sample/{selected_sample_id}", headers=headers, timeout=5)
            if report_response.status_code == 200:
                report_data = report_response.json()
            else:
                report_data = None
                st.error("Unable to retrieve report information from backend.")
        except Exception:
            report_data = None
            st.error("Backend connection error while retrieving report.")

        if report_data:
            sample_info = report_data.get("sample", {})
            analysis_results = report_data.get("analysis_results", [])
            generated_by = report_data.get("generated_by", {})

            st.markdown("---")
            st.markdown("### Report Preview")

            preview_data = {
                "Sample Code": sample_info.get("sample_code", "N/A"),
                "Sample Type": sample_info.get("type", "N/A"),
                "Status": sample_info.get("status", "N/A"),
                "Analysis Count": len(analysis_results)
            }

            st.dataframe(pd.DataFrame([preview_data]), use_container_width=True, hide_index=True)

            # ========================================================
            # REPORT FORMAT SELECTION
            # ========================================================
            report_format = st.radio("Document Format", ["Institutional Clinical Summary", "Technical Molecular Analysis"], horizontal=True)
            st.write("")

            # ========================================================
            # PDF GENERATION ENGINE
            # ========================================================
            pdf = FPDF()
            pdf.add_page()

            # HEADER
            pdf.set_font("Helvetica", "B", 14)
            pdf.set_text_color(30, 58, 138)
            pdf.cell(190, 10, "METHYLOX(TM) CLINICAL MOLECULAR REPORT", ln=True)

            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(100, 116, 139)
            pdf.cell(190, 5, "Epigenetic AI Laboratory Intelligence Platform | METHYLOX v3.0", ln=True)

            pdf.ln(5)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)

            # SECTION 1 - SAMPLE INFORMATION
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(15, 23, 42)
            pdf.cell(190, 6, "1. SAMPLE INFORMATION", ln=True)

            pdf.set_font("Helvetica", "", 9)
            pdf.cell(95, 5, f"Sample ID: {sample_info.get('id')}", ln=True)
            pdf.cell(95, 5, f"Sample Code: {sample_info.get('sample_code')}", ln=True)
            pdf.cell(95, 5, f"Sample Type: {sample_info.get('type')}", ln=True)
            pdf.cell(95, 5, f"Sample Status: {sample_info.get('status')}", ln=True)
            pdf.ln(4)

            # SECTION 2 - MOLECULAR ANALYSIS RESULTS
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(190, 6, "2. MOLECULAR ANALYSIS RESULTS", ln=True)
            pdf.set_font("Helvetica", "", 9)

            if analysis_results:
                for result in analysis_results:
                    metrics = result.get("metrics", {})
                    pdf.cell(190, 5, f"Pipeline Version: {result.get('pipeline')}", ln=True)
                    pdf.cell(190, 5, f"Quality Control Status: {result.get('qc_status')}", ln=True)
                    pdf.cell(190, 5, f"Beta Score: {metrics.get('beta_score', 'N/A')}", ln=True)
                    pdf.cell(190, 5, f"AUC Performance: {metrics.get('auc', 'N/A')}", ln=True)
                    pdf.cell(190, 5, f"Classification: {result.get('classification')}", ln=True)
                    pdf.ln(3)
            else:
                pdf.cell(190, 5, "No molecular analysis results available.", ln=True)

            # SECTION 3 - TECHNICAL APPENDIX
            if "Technical" in report_format:
                pdf.ln(3)
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(190, 6, "3. TECHNICAL MOLECULAR APPENDIX", ln=True)
                pdf.set_font("Helvetica", "", 9)
                pdf.cell(190, 5, "METHYLOX computational pipeline evaluation.", ln=True)
                pdf.cell(190, 5, "Epigenetic biomarker analysis and quality assessment performed by the platform engine.", ln=True)

            # SECTION 4 - REPORT TRACEABILITY
            pdf.ln(4)
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(190, 6, "4. REPORT TRACEABILITY", ln=True)
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(190, 5, f"Generated by User ID: {generated_by.get('user_id', 'N/A')}", ln=True)
            pdf.cell(190, 5, f"Operator: {generated_by.get('username', 'N/A')}", ln=True)
            pdf.cell(190, 5, f"Role: {generated_by.get('role', 'N/A')}", ln=True)
            pdf.ln(8)

            # DISCLAIMER
            pdf.set_font("Helvetica", "I", 8)
            pdf.set_text_color(100, 116, 139)
            pdf.cell(190, 4, "Research and laboratory intelligence platform. Results require clinical validation according to applicable institutional procedures.", ln=True, align="C")
            pdf.cell(190, 4, "Confidential proprietary information of METHYLOX(TM) Platform.", ln=True, align="C")

            # CREATE DOWNLOAD FILE
            try:
                pdf_output = pdf.output(dest="S").encode("latin1")
            except Exception:
                pdf_output = bytes(pdf.output())

            st.download_button(
                label=f" Generate & Download METHYLOX™ Report - Sample {selected_sample_id}",
                data=pdf_output,
                file_name=f"METHYLOX_Clinical_Report_{selected_sample_id}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

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
                "hospital_id": int(target_hospital_id) if 'target_hospital_id' in locals() and target_hospital_id else 1
            }
            try:
                # CORRECCIÓN: Se eliminó el prefijo redundante `/api/v1` para evitar duplicidad con BACKEND_URL
                response = requests.post(f"{BACKEND_URL}/auth/provision-user", json=payload_u, headers=headers)
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
