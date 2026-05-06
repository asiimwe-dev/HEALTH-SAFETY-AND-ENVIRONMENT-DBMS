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
    page_title="HSE-DB | Uganda O&G",
    page_icon="⛽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ======================================================================
#  GLOBAL CSS — Industrial dark theme, amber accent
# ======================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}
[data-testid="stSidebar"] {
    background: #0d1117;
    border-right: 1px solid #30363d;
}
[data-testid="stSidebar"] * { color: #c9d1d9 !important; }
[data-testid="stSidebar"] .stRadio label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    letter-spacing: 0.04em;
}
[data-testid="stAppViewContainer"] { background: #0d1117; }
[data-testid="block-container"] { padding-top: 1.5rem; padding-bottom: 2rem; }
h1, h2, h3 {
    font-family: 'IBM Plex Sans', sans-serif;
    font-weight: 700;
    color: #f0f6fc;
}
p, li, label, .stMarkdown { color: #8b949e; }

.kpi-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-top: 3px solid #e6a817;
    border-radius: 6px;
    padding: 1.2rem 1.4rem;
    text-align: center;
}
.kpi-card .kpi-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2.4rem;
    font-weight: 600;
    color: #e6a817;
    line-height: 1;
}
.kpi-card .kpi-label {
    font-size: 0.73rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #8b949e;
    margin-top: 0.4rem;
}
.kpi-card .kpi-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: #58a6ff;
    margin-top: 0.3rem;
}

.section-header {
    border-left: 3px solid #e6a817;
    padding-left: 0.8rem;
    margin: 1.6rem 0 0.8rem 0;
}
.section-header h2 {
    font-size: 1.05rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin: 0;
    color: #f0f6fc;
}
.section-header p {
    font-size: 0.78rem;
    margin: 0.15rem 0 0 0;
    color: #8b949e;
}

[data-testid="stDataFrame"] {
    border: 1px solid #30363d;
    border-radius: 6px;
}

.stTextInput input, .stTextArea textarea,
.stSelectbox div[data-baseweb="select"],
.stDateInput input {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    color: #c9d1d9 !important;
    border-radius: 4px !important;
}

.stButton > button {
    background: #e6a817;
    color: #0d1117;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    font-size: 0.82rem;
    letter-spacing: 0.06em;
    border: none;
    border-radius: 4px;
    padding: 0.55rem 1.6rem;
    transition: background 0.15s;
}
.stButton > button:hover {
    background: #f5bb2c;
    color: #0d1117;
}

hr { border: none; border-top: 1px solid #30363d; margin: 1.5rem 0; }

.sidebar-logo {
    padding: 1.2rem 1rem 1rem;
    border-bottom: 1px solid #30363d;
    margin-bottom: 1rem;
}
.sidebar-logo .app-name {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1rem;
    font-weight: 600;
    color: #e6a817;
    letter-spacing: 0.05em;
}
.sidebar-logo .app-sub {
    font-size: 0.7rem;
    color: #8b949e;
    letter-spacing: 0.04em;
    margin-top: 2px;
}

[data-testid="metric-container"] {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 0.8rem;
}
details {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 4px;
    padding: 0.2rem;
}
</style>
""", unsafe_allow_html=True)

# ======================================================================
#  DB CONFIG  — override via environment variables in production
# ======================================================================
DB_CONFIG = {
    "host":     os.getenv("HSE_DB_HOST", "localhost"),
    "user":     os.getenv("HSE_DB_USER", "root"),
    "password": os.getenv("HSE_DB_PASS", ""),   # <- set your MySQL password here
    "database": os.getenv("HSE_DB_NAME", "hse_db"),
    "charset":  "utf8mb4",
}

# Shared Plotly theme
CHART_LAYOUT = dict(
    font=dict(family="IBM Plex Sans", color="#8b949e"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#161b22",
    xaxis=dict(gridcolor="#21262d", linecolor="#30363d", showgrid=True),
    yaxis=dict(gridcolor="#21262d", linecolor="#30363d", showgrid=True),
    margin=dict(l=40, r=20, t=40, b=40),
)

# ======================================================================
#  DATABASE LAYER
# ======================================================================

@st.cache_resource(show_spinner=False)
def get_connection():
    """
    Returns a cached MySQL connection for the Streamlit session.
    Displays a user-friendly error and halts if the DB is unreachable.
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        st.error(
            "**Database connection failed.**\n\n"
            f"`{e}`\n\n"
            "Check that MySQL is running and DB_CONFIG credentials are correct."
        )
        st.stop()


def run_query(sql: str, params: tuple = None) -> pd.DataFrame:
    """
    Execute a SELECT query and return a Pandas DataFrame.
    Silently re-connects on dropped connections.
    """
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
    """
    Execute an INSERT / UPDATE / DELETE and commit.
    Returns True on success, False on failure (rolls back automatically).
    """
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
#  SIDEBAR
# ======================================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="app-name">⛽  HSE-DB</div>
        <div class="app-sub">UGANDA OIL &amp; GAS SECTOR</div>
        <div class="app-sub" style="margin-top:4px;color:#e6a81799;">
            Tilenga · Kingfisher · EACOP
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "NAVIGATE",
        options=[
            "📊  Dashboard",
            "🗂  Incident Register",
            "➕  Report Incident",
            "🎓  Training Matrix",
        ],
    )

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.68rem;color:#484f58;font-family:IBM Plex Mono,monospace;"
        "line-height:1.7;'>"
        "HSE DATABASE SYSTEM<br>"
        "Database Systems Project 2025<br>"
        "Author: Gilbert<br>"
        "Stack: MySQL 8 · Streamlit<br>"
        "</div>",
        unsafe_allow_html=True,
    )

# ======================================================================
#  PAGE 1 — DASHBOARD
# ======================================================================
if "Dashboard" in page:

    st.markdown(
        "<h1 style='margin-bottom:0.1rem;'>HSE Performance Dashboard</h1>"
        "<p style='margin-top:0;font-size:0.82rem;color:#8b949e;'>"
        "Albertine Graben Operations — All Active Sites</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # ── KPI row ────────────────────────────────────────────────────
    df_kpi = run_query("""
        SELECT
          (SELECT COUNT(*) FROM incidents)                                       AS total_incidents,
          (SELECT COUNT(*) FROM incidents WHERE inc_status = 'Open')            AS open_incidents,
          (SELECT COUNT(*) FROM incidents WHERE incident_type = 'LTI')          AS total_lti,
          (SELECT COUNT(*) FROM incidents
           WHERE severity IN ('High','Critical'))                                AS high_critical,
          (SELECT site_name FROM sites
           ORDER BY FIELD(hse_risk_category,'Critical','High','Medium','Low')
           LIMIT 1)                                                              AS highest_risk_site,
          ROUND(
            (SELECT COUNT(*) FROM employee_training WHERE cert_status='Valid')
            * 100.0
            / NULLIF((SELECT COUNT(*) FROM employee_training),0)
          , 1)                                                                   AS training_pct
    """)

    if not df_kpi.empty:
        r = df_kpi.iloc[0]

        def kpi_card(col, value, label, sub=""):
            col.markdown(
                f"<div class='kpi-card'>"
                f"<div class='kpi-value'>{value}</div>"
                f"<div class='kpi-label'>{label}</div>"
                f"{'<div class=kpi-sub>' + sub + '</div>' if sub else ''}"
                f"</div>",
                unsafe_allow_html=True,
            )

        c1, c2, c3, c4, c5 = st.columns(5)
        kpi_card(c1, int(r["total_incidents"]),  "Total Incidents",      "All time")
        kpi_card(c2, int(r["open_incidents"]),   "Open Incidents",       "Needs action")
        kpi_card(c3, int(r["total_lti"]),         "LTI Events",           "Lost Time Injuries")
        kpi_card(c4, f"{r['training_pct']}%",    "Training Compliance",  "Valid certs")
        kpi_card(c5,
                 (r["highest_risk_site"][:16] if r["highest_risk_site"] else "N/A"),
                 "Highest Risk Site", "CRITICAL category")

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    # ── Charts row ─────────────────────────────────────────────────
    col_l, col_r = st.columns([3, 2], gap="large")

    with col_l:
        st.markdown(
            "<div class='section-header'><h2>Incidents by Site</h2>"
            "<p>Stacked by severity — all recorded events</p></div>",
            unsafe_allow_html=True,
        )
        df_site = run_query("""
            SELECT s.site_name, i.severity, COUNT(*) AS cnt
            FROM incidents i JOIN sites s ON i.site_id = s.site_id
            GROUP BY s.site_name, i.severity
            ORDER BY cnt DESC
        """)
        if not df_site.empty:
            sev_colors = {"Critical":"#ff7b72","High":"#fb8f44",
                          "Medium":"#e6a817","Low":"#3fb950"}
            fig = px.bar(
                df_site, x="site_name", y="cnt", color="severity",
                color_discrete_map=sev_colors,
                labels={"site_name":"","cnt":"Incidents","severity":"Severity"},
                barmode="stack",
            )
            fig.update_layout(**CHART_LAYOUT,
                legend=dict(orientation="h", yanchor="bottom", y=1.02,
                            font=dict(size=11,color="#8b949e"), bgcolor="rgba(0,0,0,0)"),
                xaxis_tickangle=-18, xaxis_tickfont=dict(size=10),
            )
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown(
            "<div class='section-header'><h2>Incident Type Breakdown</h2>"
            "<p>Distribution across event categories</p></div>",
            unsafe_allow_html=True,
        )
        df_type = run_query("""
            SELECT incident_type, COUNT(*) AS cnt
            FROM incidents GROUP BY incident_type ORDER BY cnt DESC
        """)
        if not df_type.empty:
            fig2 = px.pie(
                df_type, names="incident_type", values="cnt",
                color_discrete_sequence=["#e6a817","#fb8f44","#ff7b72",
                                         "#58a6ff","#3fb950","#bc8cff"],
                hole=0.55,
            )
            fig2.update_layout(**CHART_LAYOUT,
                annotations=[dict(text=f"<b>{df_type['cnt'].sum()}</b><br>total",
                                  x=0.5,y=0.5,font=dict(size=14,color="#e6a817"),
                                  showarrow=False)],
                legend=dict(font=dict(size=11,color="#8b949e"),bgcolor="rgba(0,0,0,0)"),
            )
            fig2.update_traces(
                textposition="outside", textfont_size=10,
                marker=dict(line=dict(color="#0d1117",width=2)),
            )
            st.plotly_chart(fig2, use_container_width=True)

    # ── Recent incidents ───────────────────────────────────────────
    st.markdown(
        "<div class='section-header'><h2>Recent Incidents</h2>"
        "<p>Latest 5 entries across all sites</p></div>",
        unsafe_allow_html=True,
    )
    df_recent = run_query("""
        SELECT
          i.incident_id                        AS `ID`,
          DATE(i.incident_date)                AS `Date`,
          s.site_name                          AS `Site`,
          i.incident_type                      AS `Type`,
          i.severity                           AS `Severity`,
          i.inc_status                         AS `Status`,
          CONCAT(e.first_name,' ',e.last_name) AS `Reported By`
        FROM incidents i
          JOIN sites     s ON i.site_id     = s.site_id
          JOIN employees e ON i.reported_by = e.employee_id
        ORDER BY i.incident_date DESC LIMIT 5
    """)
    if not df_recent.empty:
        st.dataframe(df_recent, use_container_width=True, hide_index=True)

    # ── Expiry alert banner ────────────────────────────────────────
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
        st.warning(
            f"⚠️  **{len(df_exp)} certification(s)** expired or expiring within 60 days. "
            "Workers must not be deployed to controlled areas without valid certs."
        )
        st.dataframe(df_exp, use_container_width=True, hide_index=True)


# ======================================================================
#  PAGE 2 — INCIDENT REGISTER (READ + FILTER)
# ======================================================================
elif "Incident Register" in page:

    st.markdown(
        "<h1>Incident Register</h1>"
        "<p style='font-size:0.82rem;color:#8b949e;'>"
        "Full incident log — filter by site, severity, type, or status</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # Fetch dropdown data
    df_sites_dd = run_query("SELECT site_name FROM sites ORDER BY site_name")
    site_options = ["All Sites"] + df_sites_dd["site_name"].tolist()

    f1, f2, f3, f4 = st.columns(4)
    with f1: sel_site = st.selectbox("Site",     site_options)
    with f2: sel_sev  = st.selectbox("Severity", ["All","Critical","High","Medium","Low"])
    with f3: sel_type = st.selectbox("Type",     ["All","Near-Miss","First Aid","MTC",
                                                   "LTI","Fatality","Environmental"])
    with f4: sel_stat = st.selectbox("Status",   ["All","Open","Under Investigation","Closed"])

    # Build dynamic query
    wheres = ["1=1"]
    params = []
    if sel_site != "All Sites":
        wheres.append("s.site_name = %s"); params.append(sel_site)
    if sel_sev != "All":
        wheres.append("i.severity = %s");  params.append(sel_sev)
    if sel_type != "All":
        wheres.append("i.incident_type = %s"); params.append(sel_type)
    if sel_stat != "All":
        wheres.append("i.inc_status = %s"); params.append(sel_stat)

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

    st.markdown(
        f"<div class='section-header'><h2>Results</h2>"
        f"<p>{len(df_inc)} incident(s) match current filters</p></div>",
        unsafe_allow_html=True,
    )

    if df_inc.empty:
        st.info("No incidents match the selected filters.")
    else:
        st.dataframe(
            df_inc, use_container_width=True, hide_index=True, height=420,
            column_config={
                "Description": st.column_config.TextColumn(width="large"),
                "ID":          st.column_config.NumberColumn(width="small"),
            },
        )

        # Expandable detail view
        st.markdown("---")
        sel_id = st.selectbox("Select Incident ID for full detail", df_inc["ID"].tolist())
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
                st.markdown("**Incident Description**")
                st.info(str(r["description"]))
                if r["immediate_action"]:
                    st.markdown("**Immediate Action**"); st.success(str(r["immediate_action"]))
                if r["corrective_action"]:
                    st.markdown("**Corrective Action Plan**"); st.warning(str(r["corrective_action"]))


# ======================================================================
#  PAGE 3 — REPORT NEW INCIDENT (CREATE)
# ======================================================================
elif "Report Incident" in page:

    st.markdown(
        "<h1>Report New Incident</h1>"
        "<p style='font-size:0.82rem;color:#8b949e;'>"
        "Fields marked * are mandatory. Reports are logged immediately to the HSE database.</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # Fetch lookup tables for dropdowns
    df_sites_f = run_query(
        "SELECT site_id, site_name FROM sites WHERE site_status='Operational' ORDER BY site_name")
    df_emps_f  = run_query(
        "SELECT employee_id, CONCAT(first_name,' ',last_name,' — ',job_title) AS display "
        "FROM employees WHERE emp_status='Active' ORDER BY last_name")

    site_map = dict(zip(df_sites_f["site_name"], df_sites_f["site_id"]))
    emp_map  = dict(zip(df_emps_f["display"],    df_emps_f["employee_id"]))

    with st.form("incident_form", clear_on_submit=True):
        st.markdown(
            "<div class='section-header'><h2>Incident Details</h2></div>",
            unsafe_allow_html=True,
        )
        r1a, r1b = st.columns(2)
        with r1a:
            inc_date = st.date_input("Date *", value=datetime.date.today(),
                                     max_value=datetime.date.today())
            inc_time = st.time_input("Time *", value=datetime.time(8, 0))
        with r1b:
            inc_site = st.selectbox("Site *", list(site_map.keys()))
            reporter = st.selectbox("Reported By (FSO) *", list(emp_map.keys()))

        r2a, r2b = st.columns(2)
        with r2a:
            inc_type   = st.selectbox("Incident Type *",
                ["Near-Miss","First Aid","MTC","LTI","Fatality","Environmental"])
            severity   = st.selectbox("Severity *", ["Low","Medium","High","Critical"])
        with r2b:
            root_cause = st.selectbox("Root Cause *",
                ["Procedural Violation","Equipment Failure","Human Error",
                 "Environmental Condition","Management System Gap"])
            involved_opts = ["None — third party / unknown"] + list(emp_map.keys())
            involved   = st.selectbox("Person Involved (if employee)", involved_opts)

        st.markdown(
            "<div class='section-header' style='margin-top:1rem'><h2>Narrative</h2></div>",
            unsafe_allow_html=True,
        )
        description      = st.text_area("Description * (min. 30 chars)", height=110,
            placeholder="Describe what happened, where on site, and the sequence of events...")
        immediate_action = st.text_area("Immediate Action Taken", height=80,
            placeholder="Steps taken immediately to prevent escalation...")
        corrective_action= st.text_area("Corrective Action Plan", height=80,
            placeholder="Longer-term remediation to prevent recurrence...")

        submitted = st.form_submit_button("⚡  SUBMIT INCIDENT REPORT")

    if submitted:
        errors = []
        if not description or len(description.strip()) < 30:
            errors.append("Description must be at least 30 characters.")
        if errors:
            for err in errors:
                st.error(f"❌ {err}")
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
                    f"✅ **Incident logged.** Type: {inc_type} | Severity: {severity} | "
                    f"Site: {inc_site}. Rig Manager notified."
                )
                with st.expander("View submitted record"):
                    st.json({
                        "incident_date": str(inc_dt),
                        "site": inc_site, "type": inc_type, "severity": severity,
                        "root_cause": root_cause, "reported_by": reporter,
                        "description": description.strip(),
                    })


# ======================================================================
#  PAGE 4 — TRAINING MATRIX (M:N RELATIONSHIP VISUALISATION)
# ======================================================================
elif "Training Matrix" in page:

    st.markdown(
        "<h1>Training &amp; Certification Matrix</h1>"
        "<p style='font-size:0.82rem;color:#8b949e;'>"
        "M:N relationship — employees ↔ training_courses via employee_training junction table</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # KPI row
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
        k1,k2,k3,k4 = st.columns(4)
        def t_kpi(col, v, lbl, sub=""):
            col.markdown(
                f"<div class='kpi-card'>"
                f"<div class='kpi-value'>{v}</div>"
                f"<div class='kpi-label'>{lbl}</div>"
                f"{'<div class=kpi-sub>'+sub+'</div>' if sub else ''}"
                f"</div>", unsafe_allow_html=True)
        t_kpi(k1, int(r["total_records"]), "Total Records",    "All employees × courses")
        t_kpi(k2, int(r["valid_certs"]),   "Valid Certs",      "Currently compliant")
        t_kpi(k3, int(r["expired_certs"]), "Expired Certs",    "Action required")
        t_kpi(k4, f"{r['avg_score']}%",    "Avg. Pass Score",  "All assessments")

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    # Show the M:N JOIN SQL for educational context
    st.markdown(
        "<div class='section-header'><h2>Full Training Matrix</h2>"
        "<p>JOIN across employees · employee_training · training_courses · sites</p></div>",
        unsafe_allow_html=True,
    )
    with st.expander("📄 View SQL — M:N JOIN Query"):
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

    # Filters
    f1, f2 = st.columns(2)
    with f1:
        status_f = st.multiselect("Filter by Status",
            ["Valid","Expired","Pending Renewal"],
            default=["Valid","Expired","Pending Renewal"])
    with f2:
        cats = df_matrix["Category"].unique().tolist() if not df_matrix.empty else []
        cat_f = st.multiselect("Filter by Category", cats, default=cats)

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

        # Course coverage chart
        st.markdown(
            "<div class='section-header'><h2>Certification Coverage by Course</h2>"
            "<p>Valid vs Expired per course code</p></div>",
            unsafe_allow_html=True,
        )
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
                color_discrete_map={"Valid":"#3fb950","Expired":"#ff7b72",
                                    "Pending Renewal":"#e6a817"},
                labels={"course_code":"Course","cnt":"Employees","cert_status":"Status"},
                barmode="group",
            )
            fig3.update_layout(**CHART_LAYOUT,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,
                            font=dict(size=11,color="#8b949e"),bgcolor="rgba(0,0,0,0)"))
            fig3.update_traces(marker_line_width=0)
            st.plotly_chart(fig3, use_container_width=True)

        # Per-employee compliance bar
        st.markdown(
            "<div class='section-header'><h2>Per-Employee Compliance</h2>"
            "<p>Ratio of valid certifications — sorted ascending</p></div>",
            unsafe_allow_html=True,
        )
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
                color_continuous_scale=["#ff7b72","#e6a817","#3fb950"],
                range_color=[0,100],
                labels={"compliance_pct":"Compliance %","employee":""},
                text="compliance_pct",
            )
            fig4.update_traces(texttemplate="%{text:.0f}%",
                               textposition="outside", marker_line_width=0)
            fig4.update_layout(**CHART_LAYOUT, coloraxis_showscale=False, height=380,
                               xaxis=dict(range=[0,115],gridcolor="#21262d"))
            st.plotly_chart(fig4, use_container_width=True)
