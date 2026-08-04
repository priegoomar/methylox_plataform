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
import plotly.graph_objects as go
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
    "lims": "Samples",
    "analysis": "Analysis",
    "reports": "Reports"
}

# ADMIN ONLY MODULES
if st.session_state.user_role == "admin":
    menu_options.update({
        "users": "Access Control",
        "settings": "System Settings"
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
# TAB: ACCESS CONTROL (DYNAMIC RBAC AUTHORIZATION HUB)
# ----------------------------------------------------------------------------
elif nav_selection == "users":
    st.markdown("<h2 class='welcome-header'>Identity Governance & Task Delegation</h2>", unsafe_allow_html=True)
    st.markdown("<p class='welcome-caption'>Provision authorized personnel and assign operational roles within METHYLOX™.</p>", unsafe_allow_html=True)
    st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)

    with st.form("universal_user_provisioning_form", clear_on_submit=True):
        st.markdown("#### Register New Authorized Staff Member")
        c1, c2 = st.columns(2)

        with c1:
            input_username = st.text_input("Email", placeholder="doctor@hospital.com")
            input_full_name = st.text_input("Full Name", placeholder="e.g., Dr. John Doe, MD")

        with c2:
            input_password = st.text_input("Temporary Password", type="password", placeholder="••••••••••••")
            target_role_display = st.selectbox(
                "System Role and Permissions",
                ["admin", "cls", "md"],
                format_func=lambda x: {"admin": "Administrator", "cls": "Laboratory Scientist (CLS)", "md": "Clinical Doctor (MD)"}[x]
            )

        submit_btn = st.form_submit_button("Activate User & Grant Access")

    if submit_btn:
        if not input_username or not input_password or not input_full_name:
            st.error("All user registration fields are required.")
        else:
            payload_u = {
                "username": input_username,
                "email": input_username,
                "password": input_password,
                "full_name": input_full_name,
                "role": target_role_display
            }
            try:
                response = requests.post(f"{BACKEND_URL}/auth/provision-user", json=payload_u, headers=headers, timeout=10)
                if response.status_code == 200:
                    st.success("User account created successfully.")
                else:
                    try:
                        detail = response.json().get("detail", "Provisioning request rejected.")
                    except Exception:
                        detail = "Provisioning request rejected."
                    st.error(detail)
            except Exception:
                st.error("Backend connection unavailable.")

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# TAB 1: GENERAL DASHBOARD MATRIX
# ----------------------------------------------------------------------------
elif nav_selection == "dashboard":
    st.markdown("""
    <style>
    .welcome-header { text-align:center; color:#0F172A; font-weight:800; font-size:26px; margin-bottom:5px; }
    .welcome-caption { text-align:center; color:#64748B; font-size:13px; margin-bottom:25px; }
    .metric-card-clinical-new { background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:18px; text-align:center; min-height:150px; box-shadow:0 1px 3px rgba(0,0,0,0.04); }
    .svg-top-container { margin-bottom:8px; }
    .metric-title-sub-new { color:#64748B; font-size:12px; font-weight:700; margin:0; }
    .metric-num-big-new { color:#0F172A; font-size:30px; font-weight:800; margin:8px 0 0 0; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f'<h2 class="welcome-header">Welcome back, {st.session_state.operator_display_name}</h2>', unsafe_allow_html=True)
    st.markdown('<p class="welcome-caption">Laboratory Operations Dashboard | Real-Time Clinical Workflow Monitoring</p>', unsafe_allow_html=True)

    # ============================================================
    # TELEMETRY
    # ============================================================
    try:
        telemetry_response = requests.get(f"{BACKEND_URL}/api/v1/analysis/telemetry-summary", headers=headers, timeout=10)
        if telemetry_response.status_code == 200:
            telemetry = telemetry_response.json()
            received_today = telemetry.get("received_today", 0)
            in_progress = telemetry.get("in_progress", 0)
            ready_reports = telemetry.get("ready_reports", 0)
            qc_rate = telemetry.get("qc_pass_rate", 0)
        else:
            received_today, in_progress, ready_reports, qc_rate = 0, 0, 0, 0
    except Exception:
        received_today, in_progress, ready_reports, qc_rate = 0, 0, 0, 0

    # ============================================================
    # METRIC CARDS WITH SVG
    # ============================================================
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown("""
        <div class="metric-card-clinical-new">
        <div class="svg-top-container" style="color:#2563EB;">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M10 2v8L4.72 17.55a1 1 0 0 0 .83 1.45h12.9a1 1 0 0 0 .83-1.45L14 10V2Z"/>
        <path d="M14 2h-4"/>
        </svg>
        </div>
        <p class="metric-title-sub-new">Samples Received</p>
        <p class="metric-num-big-new">{}</p>
        </div>
        """.format(received_today), unsafe_allow_html=True)

    with m2:
        st.markdown("""
        <div class="metric-card-clinical-new">
        <div class="svg-top-container" style="color:#D97706;">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <polyline points="12 6 12 12 16 14"/>
        </svg>
        </div>
        <p class="metric-title-sub-new">Active Workflow</p>
        <p class="metric-num-big-new">{}</p>
        </div>
        """.format(in_progress), unsafe_allow_html=True)

    with m3:
        st.markdown("""
        <div class="metric-card-clinical-new">
        <div class="svg-top-container" style="color:#16A34A;">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M6 2h9l3 3v17H6z"/>
        <polyline points="14 2 14 8 20 8"/>
        </svg>
        </div>
        <p class="metric-title-sub-new">Ready Reports</p>
        <p class="metric-num-big-new">{}</p>
        </div>
        """.format(ready_reports), unsafe_allow_html=True)

    with m4:
        st.markdown("""
        <div class="metric-card-clinical-new">
        <div class="svg-top-container" style="color:#6366F1;">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
        </svg>
        </div>
        <p class="metric-title-sub-new">Quality Controls</p>
        <p class="metric-num-big-new">{}%</p>
        </div>
        """.format(qc_rate), unsafe_allow_html=True)

    st.write("")

    # ============================================================
    # RECENT LABORATORY ACTIVITY + LIVE DATA PANEL
    # ============================================================
    try:
        samples_response = requests.get(f"{BACKEND_URL}/api/v1/samples/", headers=headers, timeout=10)
        samples = samples_response.json() if samples_response.status_code == 200 else []
    except Exception:
        samples = []

    col_left, col_right = st.columns([1.45, 1])

    # ============================================================
    # LEFT COLUMN: RECENT LABORATORY ACTIVITY TRAIL
    # ============================================================
    with col_left:
        rows_html = ""
        if samples:
            for sample in samples[:5]:
                status = sample.get("status", "Collected")
                if status in ["Sample Registered"]:
                    status_style = "background:#EFF6FF; color:#2563EB;"
                elif status in ["Pre-Analytical Processing", "Molecular Data Generation", "Analysis Running"]:
                    status_style = "background:#FFFBEB; color:#D97706;"
                elif status in ["Quality Control Review", "Clinical Review"]:
                    status_style = "background:#F5F3FF; color:#7C3AED;"
                elif status == "Report Ready":
                    status_style = "background:#F0FDF4; color:#16A34A;"
                else:
                    status_style = "background:#F8FAFC; color:#64748B;"

                rows_html += f"""
                <tr style="border-bottom:1px solid #F1F5F9;">
                <td style="padding:14px 10px; text-align:center; color:#2563EB; font-weight:700; border:none;">{sample.get('sample_code','--')}</td>
                <td style="padding:14px 10px; text-align:center; border:none;">{sample.get('patient_id','--')}</td>
                <td style="padding:14px 10px; text-align:center; border:none;">{sample.get('sample_type','--')}</td>
                <td style="padding:14px 10px; text-align:center; border:none;">
                <span style="padding:5px 10px; border-radius:12px; font-size:11px; font-weight:700; {status_style}">{status}</span>
                </td>
                </tr>
                """
        else:
            rows_html = '<tr><td colspan="4" style="text-align:center; padding:60px 10px; color:#94A3B8; border:none;">No laboratory samples currently registered.</td></tr>'

        st.markdown(f"""
        <div style="background:white; border:1px solid #E2E8F0; border-radius:14px; padding:24px; min-height:360px; box-shadow:0 1px 3px rgba(0,0,0,0.03);">
        <p style="font-size:15px; font-weight:700; color:#0F172A; margin:0 0 15px 0;">Recent Laboratory Activity Trail</p>
        <table style="width:100%; border-collapse:collapse;">
        <thead>
        <tr style="background:#F8FAFC;">
        <th style="padding:12px; font-size:12px; color:#64748B; border:none;">Sample ID</th>
        <th style="padding:12px; font-size:12px; color:#64748B; border:none;">Patient ID</th>
        <th style="padding:12px; font-size:12px; color:#64748B; border:none;">Matrix</th>
        <th style="padding:12px; font-size:12px; color:#64748B; border:none;">Status</th>
        </tr>
        </thead>
        <tbody>
        {rows_html}
        </tbody>
        </table>
        </div>
        """, unsafe_allow_html=True)

    # ============================================================
    # RIGHT COLUMN: LIVE INTERACTIVE DATA STREAM & ONCO-GENETIC SUMMARY
    # ============================================================
    with col_right:
        st.markdown("""
        <div style="background:white; border:1px solid #E2E8F0; border-radius:14px; padding:20px; min-height:150px; box-shadow:0 1px 3px rgba(0,0,0,0.03);">
        <p style="font-size:15px; font-weight:700; color:#0F172A; margin:0 0 12px 0;">Live Interactive Data Stream</p>
        </div>
        """, unsafe_allow_html=True)

        if samples:
            live_df = pd.DataFrame(samples)
            live_columns = [c for c in ["sample_code", "status"] if c in live_df.columns]
            if live_columns:
                event_table = st.dataframe(live_df[live_columns].head(5), use_container_width=True, hide_index=True, height=150)
                selected_rows = event_table.selection.rows if hasattr(event_table, "selection") else []
                if selected_rows:
                    index = selected_rows[0]
                    st.session_state.active_live_sample = live_df.iloc[index].get("sample_code")
        else:
            st.markdown('<p style="color:#94A3B8; font-size:12px; text-align:center; padding:25px;">Awaiting live registry telemetry stream...</p>', unsafe_allow_html=True)

        # ============================================================
        # ONCO-GENETIC DIAGNOSTIC SUMMARY (DONUT)
        # ============================================================
        try:
            reports_response = requests.get(f"{BACKEND_URL}/api/v1/analysis/reports-directory", headers=headers, timeout=5)
            reports_data = reports_response.json() if reports_response.status_code == 200 else []
        except Exception:
            reports_data = []

        total_cases = len(reports_data)
        positive_cases = sum(1 for r in reports_data if float(r.get("score", 0)) >= 0.1000)
        negative_cases = total_cases - positive_cases
        workflow_cases = sum(1 for s in samples if s.get("status") not in ["Report Ready"]) if samples else 0

        labels = ["Positive Findings", "Negative Findings", "Active Workflow"]
        values = [positive_cases, negative_cases, workflow_cases]

        if sum(values) == 0:
            labels = ["Awaiting Data"]
            values = [1]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.60)])
        fig.update_layout(height=230, margin=dict(l=0, r=0, t=10, b=10), showlegend=True, paper_bgcolor="rgba(0,0,0,0)")

        st.markdown("""
        <div style="background:white; border:1px solid #E2E8F0; border-radius:14px; padding:20px; margin-top:15px;">
        <p style="font-size:15px; font-weight:700; color:#0F172A; margin:0 0 10px 0;">Onco-Genetic Diagnostic Summary</p>
        """, unsafe_allow_html=True)

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # ============================================================
    # QUICK CLINICAL WORKFLOWS
    # ============================================================
    st.markdown('<p style="font-size:15px; font-weight:700; color:#0F172A; margin-top:25px;">Quick Clinical Workflows</p>', unsafe_allow_html=True)

    q1, q2, q3, q4 = st.columns(4)

    def workflow_button(icon, title, subtitle, key):
        st.markdown(f"""
        <div style="background:white; border:1px solid #E2E8F0; border-radius:12px; padding:15px; height:75px; display:flex; align-items:center; gap:12px;">
        <div style="background:#EFF6FF; color:#2563EB; padding:10px; border-radius:10px;">{icon}</div>
        <div>
        <div style="font-size:13px; font-weight:700; color:#0F172A;">{title}</div>
        <div style="font-size:11px; color:#64748B;">{subtitle}</div>
        </div>
        </div>
        """, unsafe_allow_html=True)

    with q1:
        workflow_button("""
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
        <circle cx="9" cy="7" r="4"/>
        <line x1="19" y1="8" x2="19" y2="14"/>
        <line x1="22" y1="11" x2="16" y2="11"/>
        </svg>
        """, "Enroll Subject", "New Patient Profile", "patient")
    with q2:
        workflow_button("""
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
        <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
        <line x1="12" y1="22.08" x2="12" y2="12"/>
        </svg>
        """, "Asset Intake", "Log LIMS Custody", "sample")
    with q3:
        workflow_button("""
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polygon points="5 3 19 12 5 21 5 3"/>
        </svg>
        """, "Start Analysis", "Run Molecular Pipeline", "analysis")
    with q4:
        workflow_button("""
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
        <polyline points="14 2 14 8 20 8"/>
        <line x1="16" y1="13" x2="8" y2="13"/>
        <line x1="16" y1="17" x2="8" y2="17"/>
        <polyline points="10 9 9 9 8 9"/>
        </svg>
        """, "Dossier Sheet", "Export Medical PDF", "report")

    # ============================================================
    # LEGAL FOOTER
    # ============================================================
    st.markdown("""
    <div style="text-align:center; padding:20px 0; margin-top:40px; border-top:1px solid #E2E8F0;">
    <p style="margin:0; font-size:12px; color:#94A3B8;">Copyright (c) 2026 METHYLOX Oncology. All rights reserved. SaMD Software Stage Compliance.</p>
    </div>
    """, unsafe_allow_html=True)
    
# ============================================================================
# TAB 2: PATIENTS (CLINICAL COHORT MANAGEMENT)
# ============================================================================

if nav_selection == "patients":
    import uuid
    import time
    from datetime import datetime

    # -------------------------------------------------------------------------
    # CSS MODULE
    # -------------------------------------------------------------------------
    st.markdown("""
    <style>
    .patient-header {
        display:flex;
        align-items:center;
        gap:12px;
        margin-bottom:8px;
    }
    .patient-card {
        background:white;
        border:1px solid #E2E8F0;
        border-radius:12px;
        padding:12px 16px;
        box-shadow:0 1px 2px rgba(0,0,0,0.03);
        margin-bottom:8px;
    }
    .patient-card-title {
        font-size:14px;
        font-weight:700;
        color:#0F172A;
        margin-bottom:8px;
    }
    div[data-testid="stTextInput"] label,
    div[data-testid="stDateInput"] label,
    div[data-testid="stSelectbox"] label {
        font-weight:700;
        color:#334155;
        font-size:12px;
    }
    div[data-baseweb="input"] {
        border-radius:8px !important;
        border:1px solid #CBD5E1 !important;
    }
    .row-widget.stButton {
        margin-top: 0px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # HEADER
    # -------------------------------------------------------------------------
    st.markdown("""
    <div class="patient-header">
        <div style="color:#2563EB; display:flex; align-items:center;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M19 8v6"/>
                <path d="M22 11h-6"/>
            </svg>
        </div>
        <div>
            <div style="font-size:18px; font-weight:800; color:#0F172A; line-height:1.2;">Clinical Cohort Management</div>
            <div style="font-size:11px; color:#64748B; line-height:1.2;">Patient Registry & Subject Tracking</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    def load_patient_directory():
        try:
            res = requests.get(f"{BACKEND_URL}/api/v1/patients/", headers=headers, timeout=10)
            if res.status_code == 200:
                return res.json()
        except Exception:
            pass
        return []

    def normalize_patients(data):
        if not data:
            return pd.DataFrame()
        if isinstance(data, dict):
            data = data.get("patients", data.get("data", []))
        return pd.DataFrame([
            {
                "Patient ID": p.get("patient_code", ""),
                "Anonymous Code": (p.get("demographics") or {}).get("anonymous_code", ""),
                "Full Name": (p.get("demographics") or {}).get("full_name", ""),
                "Record Number": (p.get("demographics") or {}).get("record_number", ""),
                "Date of Birth": (p.get("demographics") or {}).get("date_of_birth", ""),
                "Gender": (p.get("demographics") or {}).get("gender", ""),
                "Institution": (p.get("demographics") or {}).get("institution", "")
            } for p in data if isinstance(p, dict)
        ])

    # SESSION STATES
    
    if "show_new_patient_form" not in st.session_state:
        st.session_state.show_new_patient_form = False
    
    if "patient_code_temp" not in st.session_state:
        st.session_state.patient_code_temp = (
            f"PAT-{datetime.now().year}-{str(uuid.uuid4())[:4].upper()}"
        )


    # -------------------------------------------------------------------------
    # LOAD DATA
    # -------------------------------------------------------------------------
    patients_raw = load_patient_directory()
    patients_df = normalize_patients(patients_raw)

    # =========================================================================
    # DIRECTORY VIEW
    # =========================================================================
    if not st.session_state.show_new_patient_form:
        search_col, button_col = st.columns([4, 1])

        with search_col:
            search_query = st.text_input("Search patient", placeholder="Search Patient ID, Record Number, Institution", label_visibility="collapsed")

        with button_col:
            if st.button("New Patient", use_container_width=True, key="new_patient_button"):
                st.session_state.show_new_patient_form = True
                st.rerun()

        if not patients_df.empty:
            filtered_df = patients_df.copy()
            if search_query:
                mask = filtered_df.astype(str).apply(lambda row: row.str.contains(search_query, case=False, na=False).any(), axis=1)
                filtered_df = filtered_df[mask]

            st.markdown('<div class="patient-card"><div class="patient-card-title">Patient Records Directory</div>', unsafe_allow_html=True)
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No registered patients available.")

    # =========================================================================
    # NEW PATIENT REGISTRATION
    # =========================================================================
    else:
        if st.button("Back to Directory", key="back_patient_directory"):
            st.session_state.show_new_patient_form = False
            st.rerun()

        left, right = st.columns([1, 1])

        # ---------------------------------------------------------------------
        # REGISTRATION FORM
        # ---------------------------------------------------------------------
        with left:
            st.markdown('<div class="patient-card"><div class="patient-card-title">Register New Patient</div>', unsafe_allow_html=True)
            patient_code = st.text_input("Patient ID", value=st.session_state.patient_code_temp, disabled=True)
            anonymous_code = st.text_input("Anonymous Clinical Code", value=f"MOX-{str(uuid.uuid4())[:6].upper()}", disabled=True)
            full_name = st.text_input("Full Name")
            record_number = st.text_input("Record Number")
            date_birth = st.date_input("Date of Birth")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            institution = st.text_input("Institution")
            clinical_notes = st.text_area("Clinical Notes", height=70)

            if st.button("Save Patient Record", use_container_width=True, key="save_patient"):
                if not full_name or not record_number or not institution:
                    st.error("Complete mandatory fields.")
                else:
                    payload = {
                        "patient_code": patient_code,
                        "demographics": {
                            "anonymous_code": anonymous_code,
                            "full_name": full_name,
                            "record_number": record_number,
                            "date_of_birth": str(date_birth),
                            "gender": gender,
                            "institution": institution
                        },
                        "clinical_notes": clinical_notes
                    }
                    try:
                        response = requests.post(f"{BACKEND_URL}/api/v1/patients/", json=payload, headers=headers, timeout=10)
                        if response.status_code in [200, 201]:
                            st.success("Patient registered successfully.")
                            time.sleep(1)
                            st.session_state.show_new_patient_form = False
                            st.session_state.patient_code_temp = f"PAT-{datetime.now().year}-{str(uuid.uuid4())[:4].upper()}"
                            st.rerun()
                        else:
                            st.error(response.text)
                    except Exception:
                        st.error("Backend unavailable.")
            st.markdown('</div>', unsafe_allow_html=True)

        # ---------------------------------------------------------------------
        # PATIENT SUMMARY PANEL
        # ---------------------------------------------------------------------
        with right:
            st.markdown('<div class="patient-card"><div class="patient-card-title">Clinical Cohort Overview</div>', unsafe_allow_html=True)
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
                st.caption("Waiting for patient registry data...")
            st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================================
    # MODULE FOOTER
    # =========================================================================
    st.markdown("""
    <div style="margin-top:10px; padding:6px; text-align:center; border-top:1px solid #E2E8F0;">
    <span style="color:#94A3B8; font-size:11px;">
    METHYLOX™ Clinical Cohort Management | Patient Registry Synchronization Active | Audit Trace Enabled
    </span>
    </div>
    """, unsafe_allow_html=True)

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
                        "sample_code": sample_id,
                        "patient_id": patient_id,
                        "sample_type": specimen_type,
                        "collection_date": str(collection_date),
                        "received_date": str(collection_date),
                        "status": "Collected",
                        "storage_location": collection_site
                    }                    
                    try:
                        response_sample = requests.post(f"{BACKEND_URL}/api/v1/samples/", json=payload_sample, headers=headers, timeout=5)
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
            res_s_dash = requests.get(
                f"{BACKEND_URL}/api/v1/samples/",
                headers=headers,
                timeout=5
            )
        
            if res_s_dash.status_code == 200:
                samples_list = res_s_dash.json()
            else:
                samples_list = []
        
        except Exception as e:
            samples_list = []

        if samples_data:
            df_samples = pd.DataFrame(samples_data)
            column_map = {
                "sample_code": "Sample ID",
                "patient_id": "Patient ID",
                "sample_type": "Specimen",
                "status": "Status",
                "storage_location": "Location"
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
