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
    page_title="MethyloxTM | Epigenetic AI SaMD Platform",
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
                Methylox™
            </h3>
            <p style="margin:0; color:#38BDF8; font-size:11px; font-weight:600;">
                Epigenetic AI Platform
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # SESSION STATE INITIALIZATION
    if "jwt_access_token" not in st.session_state:
        st.session_state.jwt_access_token = None

    if "operator_display_name" not in st.session_state:
        st.session_state.operator_display_name = "Guest Operator"

    if "user_role" not in st.session_state:
        st.session_state.user_role = None

    if "id_hospital" not in st.session_state:
        st.session_state.id_hospital = 1

    # LOGIN FORM
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
    # RBAC NAVIGATION (PROFESSIONAL ENGLISH LABELS & CORRECTED KEYS)
    # =========================================================================
    menu_options = {}
    if st.session_state.jwt_access_token:
        menu_options = {
            "dashboard": {"label": "General Dashboard", "icon": "📊"},
            "patients": {"label": "Patient Directory", "icon": "👥"},
            "lims": {"label": "Sample Traceability (LIMS)", "icon": "🧪"},
            "analysis": {"label": "Epigenetic Analysis", "icon": "⚙️"},
            "reports": {"label": "Reports & Certificates", "icon": "📄"}
        }

        if st.session_state.user_role == "admin":
            menu_options["settings"] = {"label": "System Settings", "icon": "🛠️"}

        if "nav_selection" not in st.session_state:
            st.session_state.nav_selection = "dashboard"

        current_selection = st.session_state.nav_selection
        if current_selection not in menu_options:
            current_selection = "dashboard"

        selected_key = st.sidebar.radio(
            "Operational Scope Selector",
            options=list(menu_options.keys()),
            format_func=lambda x: f"{menu_options[x]['icon']} {menu_options[x]['label']}",
            key="nav_selection",
            label_visibility="collapsed"
        )
    else:
        selected_key = "restricted"

    st.markdown("---")

    if "page" in st.query_params:
        query_page = st.query_params["page"]
        if query_page == "Patients" and "patients" in menu_options:
            st.session_state.nav_selection = "patients"
        elif query_page == "LIMS-Samples" and "lims" in menu_options:
            st.session_state.nav_selection = "lims"
        elif query_page == "METHYLOX-Engine" and "analysis" in menu_options:
            st.session_state.nav_selection = "analysis"
        elif query_page == "Reports" and "reports" in menu_options:
            st.session_state.nav_selection = "reports"

    st.markdown(
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
# 🏛️ CENTRAL ARCHITECTURE MODULES - TOTAL INTEGRITY
# ============================================================================

if selected_key == "restricted":
    st.markdown('<div class="executive-card-white" style="text-align:center; padding:60px 40px; margin-top:40px;">', unsafe_allow_html=True)
    st.markdown("<h2 style='color:#0F172A; font-weight:800; font-size:24px; margin-bottom:10px;'>Preventative Infrastructure Lockdown Active</h2>", unsafe_allow_html=True)
    st.caption("Methylox™ algorithmic node is encrypted. Enter authorized clinician credentials in the sidebar to allocate active pipelines.")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
#   TAB 1: GENERAL DASHBOARD MATRIX
# ----------------------------------------------------------------------------
elif selected_key == "dashboard":
    st.markdown(f"<h2 class='welcome-header'>Welcome back, {st.session_state.operator_display_name} </h2>", unsafe_allow_html=True)
    st.markdown("<p class='welcome-caption'>Laboratory Activity Summary - Real-time Onco-Genetic Telemetry Engine</p>", unsafe_allow_html=True)
    
    # FETCH LIVE DATA FROM CORRECTED ENDPOINTS
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

    # RENDER TOP TELEMETRY CARDS WITH RECOVERED SVGs
    st.markdown(f"""
    <div class='metric-container-hub'>
        <div class='metric-card-clinical-new'>
            <div class='svg-top-container' style='color: #2563EB;'>
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10 2v8L4.72 17.55a1 1 0 0 0 .83 1.45h12.9a1 1 0 0 0 .83-1.45L14 10V2Z"/><path d="M14 2h-4"/></svg>
            </div>
            <p class='metric-title-sub-new'>Samples Received</p>
            <p class='metric-num-big-new'>{received_today}</p>
            <a class='metric-link-btn-new' href='#'>View all samples →</a>
        </div>
        <div class='metric-card-clinical-new'>
            <div class='svg-top-container' style='color: #D97706;'>
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
            </div>
            <p class='metric-title-sub-new'>In Progress</p>
            <p class='metric-num-big-new'>{in_progress}</p>
            <a class='metric-link-btn-new' href='#'>View details →</a>
        </div>
        <div class='metric-card-clinical-new'>
            <div class='svg-top-container' style='color: #16A34A;'>
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/></svg>
            </div>
            <p class='metric-title-sub-new'>Ready Reports</p>
            <p class='metric-num-big-new'>{ready_analyses}</p>
            <a class='metric-link-btn-new' href='#'>View dossiers →</a>
        </div>
        <div class='metric-card-clinical-new'>
            <div class='svg-top-container' style='color: #6366F1;'>
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            </div>
            <p class='metric-title-sub-new'>Quality Controls</p>
            <p class='metric-num-big-new'>{qc_pass_rate}%</p>
            <a class='metric-link-btn-new' href='#'>View QC matrix →</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("##")

    # PARALLEL COLUMNS WITH SECURE CONTAINERS
    c_left, c_right = st.columns([1.4, 1.0])
    
    with c_left:
        try:
            res_s_dash = requests.get(f"{BACKEND_URL}/lims/samples/directory", headers=headers, timeout=5)
            samples_list = res_s_dash.json() if res_s_dash.status_code == 200 else []
        except Exception:
            samples_list = []
            
        rows_html = ""
        if not samples_list:
            rows_html = "<tr><td colspan='4' style='color: #94A3B8; padding: 60px 10px; font-style: italic; text-align: center; border: none;'>No active samples detected. Dashboard standby node waiting for live data registration...</td></tr>"
        else:
            for s in samples_list[:5]:
                state = s.get("workflow_state", "Sample Received")
                badge_style = "background-color: #EFF6FF; color: #2563EB;" if "Received" in state else "background-color: #FFFBEB; color: #D97706;" if "Extraction" in state or "Sequencing" in state else "background-color: #F0FDF4; color: #16A34A;"
                rows_html += f"""
                <tr style='border-bottom: 1px solid #F1F5F9;'>
                    <td style='font-weight: 700; color: #2563EB; padding: 14px 10px; text-align: center; border: none;'>{s.get('sample_id', '--')}</td>
                    <td style='padding: 14px 10px; text-align: center; border: none;'>{s.get('patient_id', '--')}</td>
                    <td style='padding: 14px 10px; text-align: center; border: none;'>{s.get('specimen_type', 'Plasma')}</td>
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
            res_live_df = requests.get(f"{BACKEND_URL}/lims/samples/directory", headers=headers, timeout=5)
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
            labels_pie = ['Positive Panels', 'Stable Controls', 'In Pipeline']
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
                <p style="font-size: 13px; font-weight: 700; color: #0F172A; margin: 0; line-height: 1.2;">Launch Kernel</p>
                <p style="font-size: 11px; color: #64748B; margin: 2px 0 0 0; line-height: 1.2;">Run Epigenetic Pipeline</p>
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
# 👥 TAB 2: PATIENT DIRECTORY & CLINICAL METADATA REGISTRY
# ============================================================================
if selected_key == "patients":
    st.markdown("<h2 class='welcome-header'>Clinical Subject Directory</h2>", unsafe_allow_html=True)
    st.markdown("<p class='welcome-caption'>Manage cohort entries, demographics, and clinical indication records.</p>", unsafe_allow_html=True)

    tab_p_reg, tab_p_dir = st.tabs(["➕ Enroll Subject", "📋 Cohort Directory & Search"])

    with tab_p_reg:
        st.markdown("""
        <div style='background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.02); margin-bottom: 20px;'>
            <p style='font-size:16px; font-weight:700; color:#0F172A; margin:0 0 5px 0;'>New Subject Intake Form</p>
            <p style='font-size:12px; color:#64748B; margin:0 0 20px 0;'>Register a new patient profile into the encrypted clinical database.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("patient_registration_form"):
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                p_id = st.text_input("Patient ID / Medical Record Number (MRN) *", placeholder="MRN-2026-XXXX")
                p_full_name = st.text_input("Full Subject Name *", placeholder="Doe, John A.")
                p_dob = st.date_input("Date of Birth", value=date(1975, 1, 1))
            with f_col2:
                p_gender = st.selectbox("Biological Sex", ["Female", "Male", "Other / Undisclosed"])
                p_indication = st.text_input("Primary Clinical Indication", placeholder="e.g. Suspected Colorectal Neoplasia")
                p_hospital_id = st.number_input("Hospital / Site ID", min_value=1, value=int(st.session_state.get("id_hospital", 1)))

            submit_patient = st.form_submit_button("💾 Save Patient Record", use_container_width=True)

        if submit_patient:
            if not p_id or not p_full_name:
                st.error("Please fill in all mandatory fields (Patient ID and Name).")
            else:
                payload_patient = {
                    "patient_id": p_id.strip(),
                    "full_name": p_full_name.strip(),
                    "date_of_birth": str(p_dob),
                    "gender": p_gender,
                    "clinical_indication": p_indication.strip(),
                    "hospital_id": int(p_hospital_id)
                }
                try:
                    res_p_post = requests.post(f"{BACKEND_URL}/api/v1/patients/", json=payload_patient, headers=headers, timeout=10)
                    if res_p_post.status_code in [200, 201]:
                        st.success(f"Subject {p_id} successfully registered in the database.")
                    else:
                        err_detail = res_p_post.json().get("detail", "Unknown error")
                        st.error(f"Failed to register patient: {err_detail}")
                except Exception as e:
                    st.error(f"Connection error while communicating with backend: {e}")

    with tab_p_dir:
        st.markdown("<p style='font-size:15px; font-weight:700; color:#0F172A; margin-bottom:15px;'>Active Cohort Records</p>", unsafe_allow_html=True)
        
        try:
            res_p_get = requests.get(f"{BACKEND_URL}/api/v1/patients/", headers=headers, timeout=10)
            patients_list = res_p_get.json() if res_p_get.status_code == 200 else []
        except Exception:
            patients_list = []

        if not patients_list:
            st.info("No patient records found in the system registry.")
        else:
            df_patients = pd.DataFrame(patients_list)
            st.dataframe(df_patients, use_container_width=True, hide_index=True)

# ============================================================================
# 🧪 TAB 3: SAMPLE TRACEABILITY & LIMS
# ============================================================================
elif selected_key == "lims":
    st.markdown("<h2 class='welcome-header'>Sample Traceability & LIMS</h2>", unsafe_allow_html=True)
    st.markdown("<p class='welcome-caption'>Track biological specimen custody, extraction quality metrics, and workflow state transitions.</p>", unsafe_allow_html=True)

    tab_l_reg, tab_l_track = st.tabs(["🧪 Register Sample", "🔍 Custody & Status Tracker"])

    with tab_l_reg:
        st.markdown("""
        <div style='background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.02); margin-bottom: 20px;'>
            <p style='font-size:16px; font-weight:700; color:#0F172A; margin:0 0 5px 0;'>Biological Specimen Intake</p>
            <p style='font-size:12px; color:#64748B; margin:0 0 20px 0;'>Log incoming plasma, tissue, or fluid samples for epigenetic testing.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("sample_registration_form"):
            l_col1, l_col2 = st.columns(2)
            with l_col1:
                s_id = st.text_input("Sample ID *", placeholder="SMP-2026-XXXX")
                s_pid = st.text_input("Associated Patient ID / MRN *", placeholder="MRN-2026-XXXX")
                s_type = st.selectbox("Specimen Matrix Type", ["Plasma (cfDNA)", "FFPE Tissue", "Whole Blood", "Saliva"])
            with l_col2:
                s_state = st.selectbox("Initial Workflow State", ["Sample Received", "DNA Extraction", "Bisulfite Conversion", "Sequencing / Array", "Analysis Ready"])
                s_notes = st.text_area("Handling Notes / Quality Observations", placeholder="e.g., Hemolyzed plasma sample, verified yield via Qubit.")

            submit_sample = st.form_submit_button("📦 Register Sample Custody", use_container_width=True)

        if submit_sample:
            if not s_id or not s_pid:
                st.error("Please fill in all mandatory fields (Sample ID and Patient ID).")
            else:
                payload_sample = {
                    "sample_id": s_id.strip(),
                    "patient_id": s_pid.strip(),
                    "specimen_type": s_type,
                    "workflow_state": s_state,
                    "notes": s_notes.strip()
                }
                try:
                    res_s_post = requests.post(f"{BACKEND_URL}/api/v1/lims/samples", json=payload_sample, headers=headers, timeout=10)
                    if res_s_post.status_code in [200, 201]:
                        st.success(f"Sample {s_id} successfully logged into LIMS.")
                    else:
                        err_detail = res_s_post.json().get("detail", "Unknown error")
                        st.error(f"Failed to log sample: {err_detail}")
                except Exception as e:
                    st.error(f"Connection error while communicating with backend: {e}")

    with tab_l_track:
        st.markdown("<p style='font-size:15px; font-weight:700; color:#0F172A; margin-bottom:15px;'>Active LIMS Specimen Registry</p>", unsafe_allow_html=True)
        
        try:
            res_l_get = requests.get(f"{BACKEND_URL}/api/v1/lims/samples/directory", headers=headers, timeout=10)
            lims_list = res_l_get.json() if res_l_get.status_code == 200 else []
        except Exception:
            lims_list = []

        if not lims_list:
            st.info("No specimens currently registered in the LIMS repository.")
        else:
            df_lims = pd.DataFrame(lims_list)
            st.dataframe(df_lims, use_container_width=True, hide_index=True)

# ============================================================================
# ⚙️ TAB 4: EPIGENETIC ANALYSIS KERNEL
# ============================================================================
elif selected_key == "analysis":
    st.markdown("<h2 class='welcome-header'>Epigenetic Analysis Kernel</h2>", unsafe_allow_html=True)
    st.markdown("<p class='welcome-caption'>Execute computational pipelines for methylation biomarker scoring and classification.</p>", unsafe_allow_html=True)

    with st.form("analysis_pipeline_form"):
        a_col1, a_col2 = st.columns(2)
        with a_col1:
            target_sample_id = st.text_input("Target Sample ID *", value=st.session_state.get("active_live_sample", ""), placeholder="SMP-2026-XXXX")
            model_version = st.selectbox("Diagnostic Model Version", ["Methylox-PanCancer-v3.2", "Methylox-Colorectal-v2.1", "Methylox-Lung-v1.8"])
        with a_col2:
            threshold_val = st.slider("Classification Threshold", min_value=0.01, max_value=0.99, value=0.10, step=0.01)
            include_qc = st.checkbox("Include Deep Quality Control Metrics", value=True)

        run_pipeline_btn = st.form_submit_button("🚀 Run Epigenetic Pipeline", use_container_width=True)

    if run_pipeline_btn:
        if not target_sample_id:
            st.error("Please specify a valid Target Sample ID.")
        else:
            payload_run = {
                "sample_id": target_sample_id.strip(),
                "model_version": model_version,
                "threshold": threshold_val,
                "include_qc": include_qc
            }
            with st.spinner("Executing epigenetic classification kernel... Please wait."):
                try:
                    res_run = requests.post(f"{BACKEND_URL}/api/v1/analysis/run", json=payload_run, headers=headers, timeout=30)
                    if res_run.status_code == 200:
                        res_data = res_run.json()
                        st.success("Analysis pipeline executed successfully.")
                        st.json(res_data)
                    else:
                        err_detail = res_run.json().get("detail", "Pipeline error")
                        st.error(f"Execution failed: {err_detail}")
                except Exception as e:
                    st.error(f"Connection error during pipeline execution: {e}")

# ============================================================================
# 📄 TAB 5: REPORTS & DOSSIERS
# ============================================================================
elif selected_key == "reports":
    st.markdown("<h2 class='welcome-header'>Clinical Reports & Certificates</h2>", unsafe_allow_html=True)
    st.markdown("<p class='welcome-caption'>Review finalized diagnostic dossiers and export verified medical PDF certificates.</p>", unsafe_allow_html=True)

    try:
        res_rep_dir = requests.get(f"{BACKEND_URL}/api/v1/analysis/reports-directory", headers=headers, timeout=10)
        reports_list = res_rep_dir.json() if res_rep_dir.status_code == 200 else []
    except Exception:
        reports_list = []

    if not reports_list:
        st.info("No finalized clinical reports are currently available in the directory.")
    else:
        df_reports = pd.DataFrame(reports_list)
        st.dataframe(df_reports, use_container_width=True, hide_index=True)

        st.markdown("### Export Dossier")
        # Ensure fallback column checking if keys differ
        sample_col = 'sample_id' if 'sample_id' in df_reports.columns else 'muestra_id'
        report_options = df_reports.get(sample_col, pd.Series([''])).tolist()
        
        selected_report_id = st.selectbox("Select Report / Sample ID for PDF Export", options=report_options)
        
        if st.button("📄 Generate & Download PDF Certificate", use_container_width=True):
            if selected_report_id:
                try:
                    res_pdf = requests.get(f"{BACKEND_URL}/api/v1/analysis/report-pdf/{selected_report_id}", headers=headers, timeout=15)
                    if res_pdf.status_code == 200:
                        st.success("PDF Dossier retrieved successfully.")
                        st.download_button(
                            label="📥 Download Verified Medical PDF",
                            data=res_pdf.content,
                            file_name=f"Methylox_Report_{selected_report_id}.pdf",
                            mime="application/pdf"
                        )
                    else:
                        st.error("Failed to generate PDF document from backend.")
                except Exception as e:
                    st.error(f"Connection error: {e}")

# ============================================================================
# 🛠️ TAB 6: SYSTEM SETTINGS (ADMINISTRATOR ONLY)
# ============================================================================
elif selected_key == "settings":
    if st.session_state.get("user_role") != "admin":
        st.error("Access Denied. Administrative privileges required to access system settings.")
    else:
        st.markdown("<h2 class='welcome-header'>System Settings & Administration</h2>", unsafe_allow_html=True)
        st.markdown("<p class='welcome-caption'>Configure platform parameters, user permissions, and node integration endpoints.</p>", unsafe_allow_html=True)

        with st.form("system_settings_form"):
            sys_url = st.text_input("Backend API Gateway URL", value=BACKEND_URL)
            sys_hospital_name = st.text_input("Primary Hospital / Institution Name", value="Global Clinical Oncology Center")
            sys_debug_mode = st.checkbox("Enable Verbose Telemetry Logging", value=False)
            
            save_settings = st.form_submit_button("💾 Save System Configuration", use_container_width=True)

        if save_settings:
            st.success("System configuration parameters updated successfully.")
# ----------------------------------------------------------------------------
# ⚙️ TAB 7: SYSTEM SETTINGS (KERNEL INTEGRITY AUDIT TRAIL MONITOR)
# ----------------------------------------------------------------------------
elif selected_key == "settings" or nav_selection == "⚙️ System Settings":
    if st.session_state.get("user_role") != "admin":
        st.error("Access Denied. Administrative privileges required to access system settings.")
    else:
        st.markdown("<h2 class='welcome-header'>⚙️ Core Calibration Settings & Kernel Monitor</h2>", unsafe_allow_html=True)
        st.markdown("<p class='welcome-caption'>System validation and mathematical processing rules parameters</p>", unsafe_allow_html=True)
       
        st.markdown('<div class="executive-card-white">', unsafe_allow_html=True)
        st.markdown("<p style='color:#0F172A; font-weight:700; font-size:14px; margin-bottom:10px;'>📜 METHYLOX_DETERMINISTIC_RULES.PY (AUDITABLE CONTEXT)</p>", unsafe_allow_html=True)
        st.code("""
def calculate_proprietary_cpg_beta_value(intensity_methylated: float, intensity_unmethylated: float) -> float:
    # Standard international methylation mathematical equation with fluorescence laser offset correction
    offset_correction = 100.0
    beta_value = (intensity_methylated + offset_correction) / (intensity_methylated + intensity_unmethylated + (2 * offset_correction))
    return float(beta_value)
        """, language="python")
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
#   FOOTER LEGAL BOUNDARIES (CLEAN CHARACTER ENCODING)
# ============================================================================
st.markdown("""
<div style="text-align: center; padding: 20px 0px; margin-top: 40px; border-top: 1px solid #E2E8F0;">
    <p style="margin: 0; font-size: 12px; color: #94A3B8;">Copyright &copy; 2026 METHYLOX Oncology. All rights reserved. SaMD Software Stage Compliance.</p>
</div>
""", unsafe_allow_html=True)
