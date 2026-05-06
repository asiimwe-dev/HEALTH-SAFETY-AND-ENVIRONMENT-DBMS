"""
HSE Management System — Ugandan Oil & Gas Sector
Author  : Gilbert
Stack   : Python 3 | Streamlit | MySQL 8.0 | Pandas | Plotly
Purpose : Interactive dashboard for Health, Safety & Environment data
          across Tilenga / Kingfisher / EACOP field operations.

Run     : streamlit run app.py
Config  : Set DB credentials below or via environment variables
          HSE_DB_HOST | HSE_DB_USER | HSE_DB_PASS | HSE_DB_NAME
"""

import os
import datetime
import mysql.connector
from mysql.connector import Error
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ======================================================================
#  PAGE CONFIG — must be first Streamlit call
# ======================================================================
st.set_page_config(
    page_title="HSE Command | Uganda O&G",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ======================================================================
#  GLOBAL CSS — Refined industrial theme
# ======================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&family=Syne:wght@700;800&display=swap');

/*
 * ═══════════════════════════════════════════════════════
 *  COLOUR TOKENS  —  Slate "dim mode"
 *  Base sits at slate-750 (~#1e2433), surfaces step up
 *  in 10-15 L* increments. Feels neither white-room nor
 *  cave: readable all day without eye strain.
 * ═══════════════════════════════════════════════════════
 *  --bg-base      #1a1f2e   app canvas
 *  --bg-surface   #212736   cards, sidebar
 *  --bg-raised    #2a3044   inputs, expanders, metrics
 *  --bg-hover     #303650   hover / focus rings
 *  --border       #353d52   default borders
 *  --border-light #2a3044   subtle separators
 *  --text-primary #e2e6f0   headings, strong labels
 *  --text-body    #9ca8bf   body copy, descriptions
 *  --text-muted   #5c6880   placeholders, footers
 *  --accent       #6366f1   indigo primary
 *  --accent-dim   #4f52c9   accent pressed state
 * ═══════════════════════════════════════════════════════
 */

/* ── Reset & base ─────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    -webkit-font-smoothing: antialiased;
}

/* ── App background ───────────────────────────────────── */
[data-testid="stAppViewContainer"] {
    background: #1a1f2e;
}
[data-testid="block-container"] {
    padding-top: 1.8rem;
    padding-bottom: 2.5rem;
    max-width: 1380px;
}

/* ── Sidebar / Drawer ─────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #1e2436;
    border-right: 1px solid #2e3650;
    min-width: 240px !important;
    max-width: 240px !important;
}
[data-testid="stSidebar"] * {
    color: #8a96ae !important;
}

/* Hide default radio styling completely */
[data-testid="stSidebar"] .stRadio > div {
    gap: 2px;
}
[data-testid="stSidebar"] .stRadio label {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    border-radius: 8px;
    cursor: pointer;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.875rem;
    font-weight: 500;
    color: #6e7d9a !important;
    transition: background 0.18s ease, color 0.18s ease;
    border: none;
    margin: 1px 0;
    white-space: nowrap;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(99, 102, 241, 0.12);
    color: #c8d0e4 !important;
}
[data-testid="stSidebar"] .stRadio label[data-checked="true"],
[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: rgba(99, 102, 241, 0.16);
    color: #a5b4fc !important;
    border-left: 2px solid #6366f1;
}
[data-testid="stSidebar"] .stRadio input[type="radio"] {
    display: none !important;
}

/* ── Typography ───────────────────────────────────────── */
h1 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1.9rem !important;
    color: #e2e6f0 !important;
    letter-spacing: -0.02em;
    line-height: 1.2;
}
h2 {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    color: #c8d0e4 !important;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}
h3 {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    color: #aab4cc !important;
}
p, li, .stMarkdown {
    color: #8a96ae;
    font-size: 0.9rem;
    line-height: 1.65;
}

/* ── KPI Cards ────────────────────────────────────────── */
.kpi-card {
    background: linear-gradient(145deg, #242a3d 0%, #1e2436 100%);
    border: 1px solid #2e3650;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, transform 0.2s;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #6366f1, #818cf8);
    border-radius: 12px 12px 0 0;
}
.kpi-card:hover {
    border-color: #3d4a66;
    transform: translateY(-1px);
}
.kpi-card .kpi-value {
    font-family: 'DM Mono', monospace;
    font-size: 2.2rem;
    font-weight: 500;
    color: #a5b4fc;
    line-height: 1;
    letter-spacing: -0.02em;
}
.kpi-card .kpi-label {
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 0.45rem;
    color: #5c6880;
    font-weight: 600;
}
.kpi-card .kpi-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.76rem;
    color: #818cf8;
    margin-top: 0.4rem;
}
.kpi-card-alert::before {
    background: linear-gradient(90deg, #f87171, #ef4444);
}
.kpi-card-alert .kpi-value { color: #fca5a5; }

/* ── Section Headers ─────────────────────────────────── */
.section-header {
    border-left: 3px solid #6366f1;
    padding-left: 1rem;
    margin: 2rem 0 1rem 0;
}
.section-header h2 {
    font-size: 0.78rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    margin: 0;
    color: #8a96ae !important;
}
.section-header p {
    font-size: 0.8rem;
    margin: 0.2rem 0 0 0;
    color: #4e5c78;
}

/* ── Page title block ─────────────────────────────────── */
.page-title-block {
    margin-bottom: 0.5rem;
}
.page-title-block .page-eyebrow {
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #818cf8;
    font-weight: 600;
    font-family: 'DM Mono', monospace;
    margin-bottom: 0.3rem;
}
.page-title-block h1 {
    margin: 0 0 0.3rem 0 !important;
}
.page-title-block .page-subtitle {
    font-size: 0.88rem;
    color: #5c6880;
    margin: 0;
}

/* ── Divider ──────────────────────────────────────────── */
hr {
    border: none;
    border-top: 1px solid #2a3248;
    margin: 1.4rem 0;
}

/* ── Forms & Inputs ───────────────────────────────────── */
.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"],
.stDateInput input,
.stTimeInput input {
    background: #252c3f !important;
    border: 1px solid #353d52 !important;
    color: #c8d0e4 !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    transition: border-color 0.18s !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.15) !important;
}
label[data-testid="stWidgetLabel"] {
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase;
    color: #5c6880 !important;
}

/* ── Buttons ──────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #4f52c9);
    color: #ffffff;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 0.85rem;
    letter-spacing: 0.04em;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1.8rem;
    transition: opacity 0.2s, transform 0.15s;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.3);
}
.stButton > button:hover {
    opacity: 0.9;
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
}
.stButton > button:active {
    transform: translateY(0);
}

/* ── DataFrames ───────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid #2e3650 !important;
    border-radius: 10px !important;
    overflow: hidden;
}

/* ── Metrics ──────────────────────────────────────────── */
[data-testid="metric-container"] {
    background: #242a3d;
    border: 1px solid #2e3650;
    border-radius: 10px;
    padding: 1rem 1.2rem;
}
[data-testid="metric-container"] label {
    font-size: 0.7rem !important;
    color: #5c6880 !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'DM Mono', monospace;
    font-size: 1.5rem;
    color: #a5b4fc !important;
}

/* ── Alerts / Info / Warning ──────────────────────────── */
.stAlert {
    border-radius: 10px !important;
    border-left-width: 3px !important;
    background: #242a3d !important;
}

/* ── Expander ─────────────────────────────────────────── */
details {
    background: #242a3d;
    border: 1px solid #2e3650;
    border-radius: 8px;
    padding: 0.3rem 0.5rem;
}
details summary {
    font-size: 0.83rem;
    color: #6e7d9a;
    font-family: 'DM Mono', monospace;
}

/* ── Sidebar brand block ──────────────────────────────── */
.sidebar-brand {
    padding: 1.6rem 1rem 1.2rem;
    border-bottom: 1px solid #2a3248;
    margin-bottom: 0.8rem;
}
.sidebar-brand .brand-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #6366f1, #4f52c9);
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    margin-bottom: 0.6rem;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
}
.sidebar-brand .brand-name {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 800;
    color: #dce2f0 !important;
    letter-spacing: -0.01em;
}
.sidebar-brand .brand-sub {
    font-size: 0.68rem;
    color: #4e5c78 !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-top: 2px;
    font-family: 'DM Mono', monospace;
}

/* ── Sidebar section label ────────────────────────────── */
.nav-section-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #3d4a66 !important;
    padding: 1rem 14px 0.4rem;
    font-family: 'DM Mono', monospace;
}

/* ── Sidebar footer ───────────────────────────────────── */
.sidebar-footer {
    padding: 1rem 14px 0.5rem;
    border-top: 1px solid #2a3248;
    margin-top: 1rem;
}
.sidebar-footer .footer-text {
    font-size: 0.66rem;
    color: #3d4a66 !important;
    line-height: 1.8;
    font-family: 'DM Mono', monospace;
}

/* ── Login page ───────────────────────────────────────── */
.login-wrapper {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #1a1f2e;
}
.login-card {
    background: linear-gradient(160deg, #1e2436 0%, #1a2030 100%);
    border: 1px solid #2e3650;
    border-radius: 20px;
    padding: 3rem 2.8rem 2.5rem;
    width: 100%;
    max-width: 420px;
    box-shadow: 0 24px 64px rgba(0, 0, 0, 0.35), 0 0 0 1px rgba(99,102,241,0.12);
    position: relative;
    overflow: hidden;
}
.login-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #6366f1, #818cf8, #a5b4fc);
}
.login-logo-area {
    text-align: center;
    margin-bottom: 2rem;
}
.login-logo-icon {
    width: 56px; height: 56px;
    background: linear-gradient(135deg, #6366f1, #4f52c9);
    border-radius: 14px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 1.6rem;
    margin-bottom: 1rem;
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.35);
}
.login-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.55rem !important;
    font-weight: 800 !important;
    color: #e2e6f0 !important;
    letter-spacing: -0.02em;
    margin: 0 !important;
}
.login-subtitle {
    font-size: 0.8rem;
    color: #4e5c78;
    margin-top: 0.3rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    font-family: 'DM Mono', monospace;
}

/* ── Status badge ─────────────────────────────────────── */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    font-family: 'DM Mono', monospace;
}
.badge-critical { background: rgba(239,68,68,0.12); color: #f87171; }
.badge-high     { background: rgba(251,146,60,0.12); color: #fb923c; }
.badge-medium   { background: rgba(234,179,8,0.12);  color: #eab308; }
.badge-low      { background: rgba(74,222,128,0.12); color: #4ade80; }
.badge-open     { background: rgba(251,146,60,0.12); color: #fb923c; }
.badge-closed   { background: rgba(74,222,128,0.12); color: #4ade80; }

/* ── Alert banner ─────────────────────────────────────── */
.alert-banner {
    background: rgba(248, 113, 113, 0.06);
    border: 1px solid rgba(248, 113, 113, 0.2);
    border-left: 3px solid #f87171;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
}
.alert-banner .alert-title {
    font-weight: 600;
    color: #fca5a5;
    font-size: 0.88rem;
    margin-bottom: 0.2rem;
}
.alert-banner .alert-body {
    color: #6e7d9a;
    font-size: 0.82rem;
}

/* ── Top bar ──────────────────────────────────────────── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 0 1.2rem 0;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid #2a3248;
}
.topbar-right {
    display: flex;
    align-items: center;
    gap: 0.8rem;
}
.topbar-user {
    font-size: 0.78rem;
    color: #4e5c78;
    font-family: 'DM Mono', monospace;
}
.online-dot {
    width: 8px; height: 8px;
    background: #4ade80;
    border-radius: 50%;
    display: inline-block;
    margin-right: 5px;
    box-shadow: 0 0 6px rgba(74, 222, 128, 0.4);
}

/* ── Logout button override ───────────────────────────── */
.logout-btn > button {
    background: transparent !important;
    border: 1px solid #353d52 !important;
    color: #6e7d9a !important;
    font-size: 0.75rem !important;
    padding: 0.35rem 1rem !important;
    box-shadow: none !important;
}
.logout-btn > button:hover {
    border-color: #f87171 !important;
    color: #fca5a5 !important;
    background: rgba(248, 113, 113, 0.07) !important;
    transform: none !important;
}

/* ── Form container ───────────────────────────────────── */
.form-section {
    background: #1e2436;
    border: 1px solid #2e3650;
    border-radius: 12px;
    padding: 1.5rem 1.6rem;
    margin-bottom: 1rem;
}

/* ── Scrollbar ────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #1a1f2e; }
::-webkit-scrollbar-thumb { background: #353d52; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #4a5470; }
</style>
""", unsafe_allow_html=True)

# ======================================================================
#  SESSION STATE — Authentication
# ======================================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""
if "user_role" not in st.session_state:
    st.session_state.user_role = ""

# ======================================================================
#  DEMO CREDENTIALS (replace with DB-backed auth in production)
# ======================================================================
USERS = {
    "admin":    {"password": "admin123",  "role": "HSE Administrator", "name": "Admin User"},
    "gilbert":  {"password": "hse2025",   "role": "HSE Manager",       "name": "Gilbert"},
    "field_ops":{"password": "ops2025",   "role": "Field Safety Officer","name": "Field Officer"},
}

# ======================================================================
#  LOGIN PAGE
# ======================================================================
def render_login():
    # Hide sidebar on login page
    st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="block-container"] { padding: 0 !important; max-width: 100% !important; }
    </style>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 1.1, 1])
    with col_c:
        st.markdown("<div style='height: 6vh'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="login-logo-area">
            <div class="login-logo-icon">🛡</div>
            <div class="login-title">HSE Command</div>
            <div class="login-subtitle">Uganda Oil &amp; Gas Sector · Secure Access</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

        username = st.text_input(
            "USERNAME",
            placeholder="Enter your username",
            key="login_user"
        )
        password = st.text_input(
            "PASSWORD",
            type="password",
            placeholder="Enter your password",
            key="login_pass"
        )

        st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

        if st.button("Sign In to HSE Command", use_container_width=True):
            if username in USERS and USERS[username]["password"] == password:
                st.session_state.authenticated = True
                st.session_state.current_user = USERS[username]["name"]
                st.session_state.user_role = USERS[username]["role"]
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")

        st.markdown("""
        <div style='text-align:center; margin-top:1.8rem; padding-top:1.4rem; 
             border-top: 1px solid #2a3248;'>
            <div style='font-size:0.68rem; color:#3d4a66; font-family: DM Mono, monospace; 
                 line-height:1.9; letter-spacing:0.04em;'>
                HSE DATABASE MANAGEMENT SYSTEM<br>
                Tilenga · Kingfisher · EACOP Operations<br>
                Albertine Graben · Uganda<br>
                <span style='color:#2e3a54;'>Authorised personnel only · v2.0</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ======================================================================
#  DB CONFIG  — override via environment variables in production
# ======================================================================
DB_CONFIG = {
    "host":     os.getenv("HSE_DB_HOST", "localhost"),
    "user":     os.getenv("HSE_DB_USER", "root"),
    "password": os.getenv("HSE_DB_PASS", "@CtrlGil000"),
    "database": os.getenv("HSE_DB_NAME", "hse_db"),
    "charset":  "utf8mb4",
}

# Shared Plotly theme
CHART_LAYOUT = dict(
    font=dict(family="DM Sans", color="#6e7d9a", size=11),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#1e2436",
    xaxis=dict(gridcolor="#2a3248", linecolor="#353d52", showgrid=True, tickfont=dict(size=10)),
    yaxis=dict(gridcolor="#2a3248", linecolor="#353d52", showgrid=True, tickfont=dict(size=10)),
    margin=dict(l=40, r=20, t=40, b=40),
)

# Color palette
SEVERITY_COLORS = {
    "Critical": "#ef4444",
    "High":     "#f97316",
    "Medium":   "#eab308",
    "Low":      "#4ade80",
}
ACCENT_COLORS = ["#7c3aed","#4f46e5","#6366f1","#8b5cf6","#a78bfa","#c4b5fd"]

# ======================================================================
#  DATABASE LAYER
# ======================================================================
@st.cache_resource(show_spinner=False)
def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        st.error(
            "**Database connection failed.**\n\n"
            f"`{e}`\n\n"
            "Verify that MySQL is running and credentials are correct."
        )
        st.stop()


def run_query(sql: str, params: tuple = None) -> pd.DataFrame:
    conn = get_connection()
    try:
        if not conn.is_connected():
            conn.reconnect(attempts=3, delay=1)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        rows = cursor.fetchall()
        cursor.close()
        return pd.DataFrame(rows)
    except Error as e:
        st.error(f"Query error: `{e}`")
        return pd.DataFrame()


def run_write(sql: str, params: tuple = None) -> bool:
    conn = get_connection()
    try:
        if not conn.is_connected():
            conn.reconnect(attempts=3, delay=1)
        cursor = conn.cursor()
        cursor.execute(sql, params or ())
        conn.commit()
        cursor.close()
        return True
    except Error as e:
        st.error(f"Write error: `{e}`")
        conn.rollback()
        return False


# ======================================================================
#  RENDER DECISION
# ======================================================================
if not st.session_state.authenticated:
    render_login()
    st.stop()

# ======================================================================
#  SIDEBAR — Drawer Navigation (authenticated)
# ======================================================================
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-brand">
        <div class="brand-icon">🛡</div>
        <div class="brand-name">HSE Command</div>
        <div class="brand-sub">Uganda O&amp;G · Albertine</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='nav-section-label'>Main Navigation</div>", unsafe_allow_html=True)

    page = st.radio(
        "NAV",
        options=[
            "◈  Dashboard",
            "▦  Incident Register",
            "⊕  Report Incident",
            "◉  Training Matrix",
        ],
        label_visibility="collapsed",
    )

    st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
    st.markdown("<div class='nav-section-label'>System</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='padding: 8px 14px;'>
        <div style='font-size:0.72rem; color:#4e5c78; font-family: DM Mono, monospace; 
             line-height:1.9; margin-bottom: 0.4rem;'>
            <span style='color:#3d4a66; display:block; margin-bottom:3px;'>SIGNED IN AS</span>
            <span style='color:#8a96ae;'>{st.session_state.current_user}</span><br>
            <span style='color:#4e5c78; font-size:0.65rem;'>{st.session_state.user_role}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='logout-btn'>", unsafe_allow_html=True)
    if st.button("Sign Out", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.current_user = ""
        st.session_state.user_role = ""
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-footer">
        <div class="footer-text">
            HSE-DB v2.0 · 2025<br>
            MySQL 8 · Streamlit<br>
            Tilenga · Kingfisher · EACOP
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Helper: page header ─────────────────────────────────────────────
def page_header(eyebrow: str, title: str, subtitle: str):
    st.markdown(f"""
    <div class="page-title-block">
        <div class="page-eyebrow">{eyebrow}</div>
        <h1>{title}</h1>
        <p class="page-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")


# ── Helper: KPI card ────────────────────────────────────────────────
def kpi_card(col, value, label, sub="", alert=False):
    card_class = "kpi-card kpi-card-alert" if alert else "kpi-card"
    col.markdown(
        f"<div class='{card_class}'>"
        f"<div class='kpi-value'>{value}</div>"
        f"<div class='kpi-label'>{label}</div>"
        f"{'<div class=kpi-sub>' + sub + '</div>' if sub else ''}"
        f"</div>",
        unsafe_allow_html=True,
    )


# ── Helper: section header ───────────────────────────────────────────
def section_header(title: str, subtitle: str = ""):
    st.markdown(
        f"<div class='section-header'><h2>{title}</h2>"
        f"{'<p>' + subtitle + '</p>' if subtitle else ''}</div>",
        unsafe_allow_html=True,
    )


# ======================================================================
#  PAGE 1 — DASHBOARD
# ======================================================================
if "Dashboard" in page:

    page_header(
        "Operational Overview",
        "HSE Performance Dashboard",
        "Albertine Graben Operations — All Active Sites · Real-time data"
    )

    # ── KPI row ─────────────────────────────────────────────────────
    df_kpi = run_query("""
        SELECT
          (SELECT COUNT(*) FROM incidents)                                         AS total_incidents,
          (SELECT COUNT(*) FROM incidents WHERE inc_status = 'Open')              AS open_incidents,
          (SELECT COUNT(*) FROM incidents WHERE incident_type = 'LTI')            AS total_lti,
          (SELECT COUNT(*) FROM incidents WHERE severity IN ('High','Critical'))   AS high_critical,
          (SELECT site_name FROM sites
           ORDER BY FIELD(hse_risk_category,'Critical','High','Medium','Low')
           LIMIT 1)                                                                AS highest_risk_site,
          ROUND(
            (SELECT COUNT(*) FROM employee_training WHERE cert_status='Valid')
            * 100.0 / NULLIF((SELECT COUNT(*) FROM employee_training), 0)
          , 1)                                                                     AS training_pct
    """)

    if not df_kpi.empty:
        r = df_kpi.iloc[0]
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        kpi_card(c1, int(r["total_incidents"]),  "Total Incidents",       "All time")
        kpi_card(c2, int(r["open_incidents"]),   "Open Incidents",        "Requires action", alert=int(r["open_incidents"]) > 0)
        kpi_card(c3, int(r["total_lti"]),        "LTI Events",            "Lost Time Injuries", alert=int(r["total_lti"]) > 0)
        kpi_card(c4, int(r["high_critical"]),    "High / Critical",       "Severity tier")
        kpi_card(c5, f"{r['training_pct']}%",    "Training Compliance",   "Valid certifications")
        kpi_card(c6,
                 (r["highest_risk_site"][:14] if r["highest_risk_site"] else "N/A"),
                 "Highest Risk Site", "Critical category")

    st.markdown("<div style='height:1.4rem'></div>", unsafe_allow_html=True)

    # ── Cert expiry alert ────────────────────────────────────────────
    df_exp = run_query("""
        SELECT
          CONCAT(e.first_name,' ',e.last_name) AS Employee,
          e.job_title                           AS Role,
          s.site_name                           AS Site,
          tc.course_code                        AS Course,
          et.expiry_date                        AS `Expiry Date`,
          et.cert_status                        AS Status
        FROM employee_training et
          JOIN employees        e  ON et.employee_id = e.employee_id
          JOIN training_courses tc ON et.course_id   = tc.course_id
          JOIN sites            s  ON e.site_id      = s.site_id
        WHERE et.cert_status = 'Expired'
           OR et.expiry_date <= DATE_ADD(CURDATE(), INTERVAL 60 DAY)
        ORDER BY et.expiry_date ASC LIMIT 8
    """)
    if not df_exp.empty:
        st.markdown(f"""
        <div class="alert-banner">
            <div class="alert-title">Certification Alert — Immediate Action Required</div>
            <div class="alert-body">
                {len(df_exp)} certification(s) are expired or expiring within 60 days.
                Affected workers must not be deployed to controlled areas without valid certifications.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(df_exp, use_container_width=True, hide_index=True)

    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

    # ── Charts row ──────────────────────────────────────────────────
    col_l, col_r = st.columns([3, 2], gap="large")

    with col_l:
        section_header("Incidents by Site", "Stacked by severity — all recorded events")
        df_site = run_query("""
            SELECT s.site_name, i.severity, COUNT(*) AS cnt
            FROM incidents i JOIN sites s ON i.site_id = s.site_id
            GROUP BY s.site_name, i.severity
            ORDER BY cnt DESC
        """)
        if not df_site.empty:
            fig = px.bar(
                df_site, x="site_name", y="cnt", color="severity",
                color_discrete_map=SEVERITY_COLORS,
                labels={"site_name": "", "cnt": "Incidents", "severity": "Severity"},
                barmode="stack",
            )
            fig.update_layout(
                **CHART_LAYOUT,
                legend=dict(orientation="h", yanchor="bottom", y=1.02,
                            font=dict(size=11, color="#60607a"), bgcolor="rgba(0,0,0,0)"),
                xaxis_tickangle=-18,
            )
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)

    with col_r:
        section_header("Incident Type Distribution", "By event category")
        df_type = run_query("""
            SELECT incident_type, COUNT(*) AS cnt
            FROM incidents GROUP BY incident_type ORDER BY cnt DESC
        """)
        if not df_type.empty:
            fig2 = px.pie(
                df_type, names="incident_type", values="cnt",
                color_discrete_sequence=ACCENT_COLORS,
                hole=0.6,
            )
            fig2.update_layout(
                **CHART_LAYOUT,
                annotations=[dict(
                    text=f"<b>{df_type['cnt'].sum()}</b><br><span style='font-size:10px'>total</span>",
                    x=0.5, y=0.5,
                    font=dict(size=14, color="#a78bfa"),
                    showarrow=False
                )],
                legend=dict(font=dict(size=11, color="#60607a"), bgcolor="rgba(0,0,0,0)"),
            )
            fig2.update_traces(
                textposition="outside", textfont_size=10,
                marker=dict(line=dict(color="#1a1f2e", width=2)),
            )
            st.plotly_chart(fig2, use_container_width=True)

    # ── Monthly trend ────────────────────────────────────────────────
    section_header("Monthly Incident Trend", "12-month rolling view — all severity levels")
    df_monthly = run_query("""
        SELECT DATE_FORMAT(incident_date,'%Y-%m') AS month,
               severity, COUNT(*) AS cnt
        FROM incidents
        WHERE incident_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
        GROUP BY month, severity
        ORDER BY month
    """)
    if not df_monthly.empty:
        fig3 = px.line(
            df_monthly, x="month", y="cnt", color="severity",
            color_discrete_map=SEVERITY_COLORS,
            markers=True,
            labels={"month": "", "cnt": "Incidents", "severity": "Severity"},
        )
        fig3.update_layout(
            **CHART_LAYOUT,
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        font=dict(size=11, color="#60607a"), bgcolor="rgba(0,0,0,0)"),
            xaxis_tickangle=-18,
        )
        fig3.update_traces(line=dict(width=2), marker=dict(size=6))
        st.plotly_chart(fig3, use_container_width=True)

    # ── Site risk summary ────────────────────────────────────────────
    section_header("Site Risk Profile", "Risk categorisation across all operational sites")
    df_sites_risk = run_query("""
        SELECT site_name, district, operation_type, hse_risk_category, site_status
        FROM sites ORDER BY FIELD(hse_risk_category,'Critical','High','Medium','Low')
    """)
    if not df_sites_risk.empty:
        st.dataframe(df_sites_risk, use_container_width=True, hide_index=True,
            column_config={
                "site_name":         st.column_config.TextColumn("Site Name",    width="medium"),
                "district":          st.column_config.TextColumn("District",     width="medium"),
                "operation_type":    st.column_config.TextColumn("Operation",    width="medium"),
                "hse_risk_category": st.column_config.TextColumn("Risk Level",   width="small"),
                "site_status":       st.column_config.TextColumn("Status",       width="small"),
            }
        )


# ======================================================================
#  PAGE 2 — INCIDENT REGISTER
# ======================================================================
elif "Incident Register" in page:

    page_header(
        "Records Management",
        "Incident Register",
        "Full incident log — filter, search, and inspect all recorded events"
    )

    df_sites_dd = run_query("SELECT site_name FROM sites ORDER BY site_name")
    site_options = ["All Sites"] + df_sites_dd["site_name"].tolist()

    # ── Filters ──────────────────────────────────────────────────────
    f1, f2, f3, f4 = st.columns(4)
    with f1: sel_site = st.selectbox("Site",     site_options)
    with f2: sel_sev  = st.selectbox("Severity", ["All", "Critical", "High", "Medium", "Low"])
    with f3: sel_type = st.selectbox("Type",     ["All", "Near-Miss", "First Aid", "MTC",
                                                   "LTI", "Fatality", "Environmental"])
    with f4: sel_stat = st.selectbox("Status",   ["All", "Open", "Under Investigation", "Closed"])

    # ── Dynamic query ────────────────────────────────────────────────
    wheres = ["1=1"]
    params = []
    if sel_site != "All Sites":
        wheres.append("s.site_name = %s"); params.append(sel_site)
    if sel_sev  != "All":
        wheres.append("i.severity = %s");       params.append(sel_sev)
    if sel_type != "All":
        wheres.append("i.incident_type = %s");  params.append(sel_type)
    if sel_stat != "All":
        wheres.append("i.inc_status = %s");     params.append(sel_stat)

    df_inc = run_query(f"""
        SELECT
          i.incident_id                              AS `ID`,
          DATE(i.incident_date)                      AS `Date`,
          TIME(i.incident_date)                      AS `Time`,
          s.site_name                                AS `Site`,
          s.district                                 AS `District`,
          i.incident_type                            AS `Type`,
          i.severity                                 AS `Severity`,
          i.root_cause                               AS `Root Cause`,
          CONCAT(rep.first_name,' ',rep.last_name)   AS `Reported By`,
          COALESCE(CONCAT(inv.first_name,' ',inv.last_name),'— external —')
                                                     AS `Person Involved`,
          i.inc_status                               AS `Status`,
          i.description                              AS `Description`
        FROM incidents i
          JOIN sites     s   ON i.site_id     = s.site_id
          JOIN employees rep ON i.reported_by = rep.employee_id
          LEFT JOIN employees inv ON i.involved_employee_id = inv.employee_id
        WHERE {" AND ".join(wheres)}
        ORDER BY i.incident_date DESC
    """, tuple(params))

    section_header("Query Results", f"{len(df_inc)} incident(s) match the current filters")

    if df_inc.empty:
        st.info("No incidents match the selected filters. Adjust criteria above.")
    else:
        st.dataframe(
            df_inc, use_container_width=True, hide_index=True, height=420,
            column_config={
                "Description": st.column_config.TextColumn(width="large"),
                "ID":          st.column_config.NumberColumn(width="small"),
            },
        )

        # ── Detail view ───────────────────────────────────────────────
        st.markdown("---")
        section_header("Incident Detail View", "Select an incident ID to inspect the full record")
        sel_id = st.selectbox("Incident ID", df_inc["ID"].tolist())
        if sel_id:
            df_d = run_query("""
                SELECT i.*, s.site_name, s.district,
                  CONCAT(rep.first_name,' ',rep.last_name) AS reporter_name,
                  COALESCE(CONCAT(inv.first_name,' ',inv.last_name),'—') AS involved_name
                FROM incidents i
                  JOIN sites s ON i.site_id = s.site_id
                  JOIN employees rep ON i.reported_by = rep.employee_id
                  LEFT JOIN employees inv ON i.involved_employee_id = inv.employee_id
                WHERE i.incident_id = %s
            """, (sel_id,))
            if not df_d.empty:
                r = df_d.iloc[0]
                a, b, c = st.columns(3)
                a.metric("Site",        r["site_name"])
                b.metric("Type",        r["incident_type"])
                c.metric("Severity",    r["severity"])
                d, e, f = st.columns(3)
                d.metric("Reported By", r["reporter_name"])
                e.metric("Status",      r["inc_status"])
                f.metric("Root Cause",  r["root_cause"])
                st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
                st.markdown("**Incident Description**")
                st.info(str(r["description"]))
                if r["immediate_action"]:
                    st.markdown("**Immediate Actions Taken**")
                    st.success(str(r["immediate_action"]))
                if r["corrective_action"]:
                    st.markdown("**Corrective Action Plan**")
                    st.warning(str(r["corrective_action"]))


# ======================================================================
#  PAGE 3 — REPORT NEW INCIDENT
# ======================================================================
elif "Report Incident" in page:

    page_header(
        "Data Entry",
        "Report New Incident",
        "All fields marked * are mandatory. Records are committed to the HSE database immediately."
    )

    df_sites_f = run_query(
        "SELECT site_id, site_name FROM sites WHERE site_status='Operational' ORDER BY site_name")
    df_emps_f  = run_query(
        "SELECT employee_id, CONCAT(first_name,' ',last_name,' — ',job_title) AS display "
        "FROM employees WHERE emp_status='Active' ORDER BY last_name")

    site_map = dict(zip(df_sites_f["site_name"], df_sites_f["site_id"]))
    emp_map  = dict(zip(df_emps_f["display"],    df_emps_f["employee_id"]))

    with st.form("incident_form", clear_on_submit=True):

        section_header("Incident Details", "Date, time, location and personnel")
        r1a, r1b = st.columns(2)
        with r1a:
            inc_date = st.date_input("Incident Date *", value=datetime.date.today(),
                                     max_value=datetime.date.today())
            inc_time = st.time_input("Incident Time *", value=datetime.time(8, 0))
        with r1b:
            inc_site = st.selectbox("Site *", list(site_map.keys()))
            reporter = st.selectbox("Field Safety Officer (Reporter) *", list(emp_map.keys()))

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        section_header("Classification", "Incident type, severity and root cause")
        r2a, r2b = st.columns(2)
        with r2a:
            inc_type   = st.selectbox("Incident Type *",
                ["Near-Miss", "First Aid", "MTC", "LTI", "Fatality", "Environmental"])
            severity   = st.selectbox("Severity Level *",
                ["Low", "Medium", "High", "Critical"])
        with r2b:
            root_cause = st.selectbox("Root Cause *",
                ["Procedural Violation", "Equipment Failure", "Human Error",
                 "Environmental Condition", "Management System Gap"])
            involved_opts = ["None — third party / unknown"] + list(emp_map.keys())
            involved   = st.selectbox("Employee Involved (if applicable)", involved_opts)

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        section_header("Incident Narrative", "Description and response actions")
        description       = st.text_area("Incident Description * (minimum 30 characters)", height=110,
            placeholder="Describe what happened, the location on site, and the sequence of events in detail...")
        immediate_action  = st.text_area("Immediate Actions Taken", height=80,
            placeholder="Steps taken immediately following the incident to prevent escalation...")
        corrective_action = st.text_area("Corrective Action Plan", height=80,
            placeholder="Longer-term remediation steps to prevent recurrence of this incident...")

        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Submit Incident Report", use_container_width=False)

    if submitted:
        errors = []
        if not description or len(description.strip()) < 30:
            errors.append("Incident description must be at least 30 characters.")
        if errors:
            for err in errors:
                st.error(err)
        else:
            inc_dt      = datetime.datetime.combine(inc_date, inc_time)
            site_id_val = site_map[inc_site]
            reporter_id = emp_map[reporter]
            involved_id = (emp_map[involved]
                           if involved != "None — third party / unknown" else None)

            ok = run_write(
                """INSERT INTO incidents
                   (incident_date, site_id, reported_by, involved_employee_id,
                    incident_type, severity, description, root_cause,
                    immediate_action, corrective_action, inc_status)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'Open')""",
                (inc_dt, site_id_val, reporter_id, involved_id,
                 inc_type, severity, description.strip(), root_cause,
                 immediate_action.strip() or None,
                 corrective_action.strip() or None),
            )
            if ok:
                st.success(
                    f"Incident successfully logged. Type: **{inc_type}** | "
                    f"Severity: **{severity}** | Site: **{inc_site}**. "
                    f"The Rig Manager has been notified."
                )
                with st.expander("View Submitted Record (JSON)"):
                    st.json({
                        "incident_date": str(inc_dt),
                        "site": inc_site, "type": inc_type, "severity": severity,
                        "root_cause": root_cause, "reported_by": reporter,
                        "description": description.strip(),
                    })


# ======================================================================
#  PAGE 4 — TRAINING MATRIX
# ======================================================================
elif "Training Matrix" in page:

    page_header(
        "Compliance & Certification",
        "Training & Certification Matrix",
        "Many-to-many relationship — employees linked to training courses via the employee_training junction table"
    )

    # ── KPI row ──────────────────────────────────────────────────────
    df_tk = run_query("""
        SELECT
          COUNT(*)                                       AS total_records,
          SUM(cert_status='Valid')                       AS valid_certs,
          SUM(cert_status='Expired')                     AS expired_certs,
          ROUND(AVG(score),1)                            AS avg_score
        FROM employee_training
    """)
    if not df_tk.empty:
        r = df_tk.iloc[0]
        k1, k2, k3, k4 = st.columns(4)
        kpi_card(k1, int(r["total_records"]), "Total Records",   "All employees × courses")
        kpi_card(k2, int(r["valid_certs"]),   "Valid Certifications", "Currently compliant")
        kpi_card(k3, int(r["expired_certs"]), "Expired Certifications", "Action required",
                 alert=int(r["expired_certs"]) > 0)
        kpi_card(k4, f"{r['avg_score']}%",   "Average Assessment Score", "All completions")

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    # ── SQL display ──────────────────────────────────────────────────
    section_header("Full Training Matrix", "JOIN across employees · employee_training · training_courses · sites")
    with st.expander("View SQL — Many-to-Many JOIN Query"):
        st.code("""
SELECT
  CONCAT(e.first_name,' ',e.last_name)  AS employee_name,
  e.job_title,
  s.site_name,
  tc.course_code,
  tc.course_name,
  tc.category,
  et.completion_date,
  et.expiry_date,
  et.certificate_number,
  et.score,
  et.cert_status,
  DATEDIFF(et.expiry_date, CURDATE())   AS days_until_expiry
FROM employee_training et
  JOIN employees        e  ON et.employee_id = e.employee_id
  JOIN training_courses tc ON et.course_id   = tc.course_id
  JOIN sites            s  ON e.site_id      = s.site_id
ORDER BY e.last_name, et.expiry_date;
        """, language="sql")

    df_matrix = run_query("""
        SELECT
          CONCAT(e.first_name,' ',e.last_name) AS `Employee`,
          e.job_title                           AS `Role`,
          s.site_name                           AS `Site`,
          tc.course_code                        AS `Code`,
          tc.course_name                        AS `Course`,
          tc.category                           AS `Category`,
          et.completion_date                    AS `Completed`,
          et.expiry_date                        AS `Expires`,
          et.certificate_number                 AS `Cert No.`,
          et.score                              AS `Score (%)`,
          et.cert_status                        AS `Status`,
          DATEDIFF(et.expiry_date, CURDATE())   AS `Days Left`
        FROM employee_training et
          JOIN employees        e  ON et.employee_id = e.employee_id
          JOIN training_courses tc ON et.course_id   = tc.course_id
          JOIN sites            s  ON e.site_id      = s.site_id
        ORDER BY e.last_name, et.expiry_date
    """)

    # ── Filters ──────────────────────────────────────────────────────
    f1, f2 = st.columns(2)
    with f1:
        status_f = st.multiselect("Filter by Certification Status",
            ["Valid", "Expired", "Pending Renewal"],
            default=["Valid", "Expired", "Pending Renewal"])
    with f2:
        cats = df_matrix["Category"].unique().tolist() if not df_matrix.empty else []
        cat_f = st.multiselect("Filter by Training Category", cats, default=cats)

    if not df_matrix.empty:
        filtered = df_matrix[
            df_matrix["Status"].isin(status_f) & df_matrix["Category"].isin(cat_f)
        ]
        st.dataframe(
            filtered, use_container_width=True, hide_index=True, height=480,
            column_config={
                "Score (%)": st.column_config.ProgressColumn(
                    "Score (%)", min_value=0, max_value=100, format="%.1f%%"),
                "Days Left": st.column_config.NumberColumn("Days Left", format="%d d"),
                "Course":    st.column_config.TextColumn(width="large"),
                "Employee":  st.column_config.TextColumn(width="medium"),
            },
        )

        # ── Course coverage ───────────────────────────────────────────
        section_header("Certification Coverage by Course", "Valid vs Expired per course code")
        df_cov = run_query("""
            SELECT tc.course_code, et.cert_status, COUNT(*) AS cnt
            FROM employee_training et
              JOIN training_courses tc ON et.course_id = tc.course_id
            GROUP BY tc.course_code, et.cert_status
            ORDER BY cnt DESC
        """)
        if not df_cov.empty:
            fig3 = px.bar(
                df_cov, x="course_code", y="cnt", color="cert_status",
                color_discrete_map={
                    "Valid":           "#4ade80",
                    "Expired":         "#f87171",
                    "Pending Renewal": "#eab308",
                },
                labels={"course_code": "Course", "cnt": "Employees", "cert_status": "Status"},
                barmode="group",
            )
            fig3.update_layout(
                **CHART_LAYOUT,
                legend=dict(orientation="h", yanchor="bottom", y=1.02,
                            font=dict(size=11, color="#60607a"), bgcolor="rgba(0,0,0,0)"),
            )
            fig3.update_traces(marker_line_width=0)
            st.plotly_chart(fig3, use_container_width=True)

        # ── Per-employee compliance ───────────────────────────────────
        section_header("Per-Employee Compliance Rate", "Ratio of valid certifications — sorted ascending")
        df_ec = run_query("""
            SELECT
              CONCAT(e.first_name,' ',e.last_name) AS employee,
              COUNT(*)                              AS total_certs,
              SUM(et.cert_status='Valid')           AS valid_certs,
              ROUND(SUM(et.cert_status='Valid')*100.0/COUNT(*),0) AS compliance_pct
            FROM employee_training et
              JOIN employees e ON et.employee_id = e.employee_id
            GROUP BY e.employee_id
            ORDER BY compliance_pct ASC
        """)
        if not df_ec.empty:
            fig4 = px.bar(
                df_ec, x="compliance_pct", y="employee", orientation="h",
                color="compliance_pct",
                color_continuous_scale=["#ef4444", "#eab308", "#4ade80"],
                range_color=[0, 100],
                labels={"compliance_pct": "Compliance %", "employee": ""},
                text="compliance_pct",
            )
            fig4.update_traces(
                texttemplate="%{text:.0f}%",
                textposition="outside",
                marker_line_width=0,
            )
            fig4.update_layout(
                **CHART_LAYOUT,
                coloraxis_showscale=False,
                height=380,
                xaxis=dict(range=[0, 115], gridcolor="#2a3248"),
            )
            st.plotly_chart(fig4, use_container_width=True)