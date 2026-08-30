import hashlib
from datetime import date, datetime
import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import text

# -------------------------------------------------------------
# 1. Page Config & Ultra-Stylish Encore Healthcare Styling
# -------------------------------------------------------------
st.set_page_config(page_title="Encore QC Analytics", page_icon="🧬", layout="wide", initial_sidebar_state="expanded")

# Official Encore Healthcare Logo
ENCORE_LOGO_URL = "https://encorehealthcare.in/wp-content/uploads/2023/12/encore-healthcare_transparent-1536x618.png"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
    
    /* Background & Main App */
    .stApp {{ background: #F7F9FC; }}
    
    /* Custom Header Bar */
    .top-header {{
        background: linear-gradient(135deg, #0B1C3E 0%, #1A365D 100%);
        padding: 20px 30px;
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
        display: flex;
        align-items: center;
        box-shadow: 0 10px 25px rgba(11, 28, 62, 0.15);
    }}
    .top-header img {{ height: 50px; margin-right: 20px; }} 
    .top-header h1 {{ margin: 0; font-size: 2.2rem; font-weight: 800; letter-spacing: 0.5px; }}
    .top-header p {{ margin: 5px 0 0 0; color: #94A3B8; font-weight: 500; }}

    /* Stylish Metric Cards */
    .trendy-card {{ 
        background: #FFFFFF; 
        border-radius: 16px; 
        padding: 24px 20px; 
        text-align: left; 
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.05); 
        border-left: 6px solid #4318FF; 
        transition: transform 0.3s ease, box-shadow 0.3s ease; 
        position: relative;
        overflow: hidden;
    }}
    .trendy-card:hover {{ 
        transform: translateY(-5px); 
        box-shadow: 0px 15px 30px rgba(0, 0, 0, 0.1); 
    }}
    .trendy-card::after {{ 
        content: ''; position: absolute; top: -20px; right: -20px; 
        width: 100px; height: 100px; border-radius: 50%;
        background: linear-gradient(135deg, rgba(67, 24, 255, 0.05), rgba(67, 24, 255, 0.1));
    }}
    .metric-value {{ font-size: 2.4rem; font-weight: 800; color: #1E293B; margin: 8px 0 0 0; }}
    .metric-label {{ color: #64748B; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }}
    
    /* Styled Tabs */
    .stTabs [data-baseweb="tab-list"] {{ gap: 8px; border-bottom: 2px solid #E2E8F0; padding-bottom: 0px; }}
    .stTabs [data-baseweb="tab"] {{ 
        background-color: transparent; border: none; padding: 12px 20px; 
        color: #64748B; font-weight: 600; transition: all 0.2s;
    }}
    .stTabs [aria-selected="true"] {{ 
        color: #0B1C3E !important; border-bottom: 3px solid #4318FF; background-color: #FFFFFF;
        border-radius: 8px 8px 0 0; box-shadow: 0px -2px 10px rgba(0,0,0,0.02);
    }}
    
    #MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. Database Connection & Init
# -------------------------------------------------------------
conn = st.connection("postgresql", type="sql")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    with conn.session as s:
        s.execute(text("""
            CREATE TABLE IF NOT EXISTS fp_analysis (
                id SERIAL PRIMARY KEY, product_name TEXT, strength TEXT, batch_no TEXT UNIQUE,
                sample_receipt_date DATE, analysis_start_date DATE, analysis_completion_date DATE,
                review_completion_date DATE, coa_completion_date DATE, target_release_date DATE,
                analyst_name TEXT, status TEXT DEFAULT 'In Progress', delay_reason TEXT, actual_testing_hours REAL
            )
        """))
        s.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY, username TEXT UNIQUE NOT NULL, 
                password TEXT NOT NULL, role TEXT NOT NULL
            )
        """))
        s.execute(text("""
            CREATE TABLE IF NOT EXISTS user_logs (
                id SERIAL PRIMARY KEY, username TEXT, login_time TIMESTAMP, 
                logout_time TIMESTAMP, usage_minutes REAL
            )
        """))
        
        admin_check = s.execute(text("SELECT * FROM users WHERE username='admin'")).fetchone()
        if not admin_check:
            s.execute(text("INSERT INTO users (username, password, role) VALUES (:u, :p, :r)"), 
                      {"u": "admin", "p": hash_password("admin@123"), "r": "admin"})
        s.commit()

init_db()

# -------------------------------------------------------------
# 3. Session & Auth
# -------------------------------------------------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.log_id = None
    st.session_state.login_time = None

def do_logout():
    if st.session_state.log_id:
        logout_time = datetime.now()
        usage_duration = (logout_time - st.session_state.login_time).total_seconds() / 60.0
        with conn.session as s:
            s.execute(text("UPDATE user_logs SET logout_time = :lo, usage_minutes = :um WHERE id = :id"), 
                      {"lo": logout_time, "um": usage_duration, "id": st.session_state.log_id})
            s.commit()
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.log_id = None
    st.session_state.login_time = None
    st.rerun()

if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="{ENCORE_LOGO_URL}" style="height: 70px;">
                <h2 style="color: #0B1C3E; font-weight: 800; margin-top: 10px;">Encore Healthcare</h2>
                <p style="color: #64748B;">QC Operations Hub</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="trendy-card" style="border-left: none; border-top: 5px solid #4318FF; text-align: center;">', unsafe_allow_html=True)
        st.subheader("🔐 System Login")
        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")
        
        if st.button("Secure Login", type="primary", use_container_width=True):
            user_df = conn.query("SELECT id, role, password FROM users WHERE username = :u", params={"u": username_input})
            if not user_df.empty and user_df.iloc[0]['password'] == hash_password(password_input):
                st.session_state.logged_in = True
                st.session_state.username = username_input
                st.session_state.role = user_df.iloc[0]['role']
                st.session_state.login_time = datetime.now()
                
                with conn.session as s:
                    result = s.execute(text("INSERT INTO user_logs (username, login_time) VALUES (:u, :lt) RETURNING id"), 
                                       {"u": username_input, "lt": st.session_state.login_time})
                    st.session_state.log_id = result.fetchone()[0]
                    s.commit()
                st.rerun()
            else:
                st.error("Invalid Username or Password")
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 4. Main Application
# -------------------------------------------------------------
else:
    # Sidebar
    st.sidebar.image(ENCORE_LOGO_URL, use_container_width=True)
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    st.sidebar.write(f"👤 **User:** {st.session_state.username}")
    st.sidebar.write(f"🛡️ **Role:** {st.session_state.role.upper()}")
    st.sidebar.button("🚪 Logout", on_click=do_logout, use_container_width=True)
    st.sidebar.markdown("---")

    # Data Fetching & Processing
    df = conn.query("SELECT * FROM fp_analysis", ttl=0)

    st.sidebar.subheader("📅 Global Date Filter")
    if not df.empty:
        df['sample_receipt_date'] = pd.to_datetime(df['sample_receipt_date'], errors='coerce')
        df['MonthYear'] = df['sample_receipt_date'].dt.to_period('M')
        
        available_months = sorted(df['MonthYear'].dropna().unique(), reverse=True)
        available_months_str = [m.strftime('%B %Y') for m in available_months]
        
        current_month_str = pd.Timestamp.now().strftime('%B %Y')
        default_index = available_months_str.index(current_month_str) if current_month_str in available_months_str else 0
        
        if available_months_str:
            selected_month_str = st.sidebar.selectbox("Select Month", available_months_str, index=default_index)
            selected_period = pd.Period(datetime.strptime(selected_month_str, '%B %Y'), freq='M')
            df = df[df['MonthYear'] == selected_period]
            
        df['Queue Time (Days)'] = (pd.to_datetime(df['analysis_start_date']) - df['sample_receipt_date']).dt.days
        df['Testing Time (Days)'] = (pd.to_datetime(df['analysis_completion_date']) - pd.to_datetime(df['analysis_start_date'])).dt.days
        df['Review Time (Days)'] = (pd.to_datetime(df['review_completion_date']) - pd.to_datetime(df['analysis_completion_date'])).dt.days
        df['COA Time (Days)'] = (pd.to_datetime(df['coa_completion_date']) - pd.to_datetime(df['review_completion_date'])).dt.days
        df['Total TAT (Days)'] = df['Queue Time (Days)'] + df['Testing Time (Days)'] + df['Review Time (Days)'] + df['COA Time (Days)']
    else:
        st.sidebar.info("No data available to filter.")

    # Stylish Custom Header
    st.markdown(f"""
        <div class="top-header">
            <img src="{ENCORE_LOGO_URL}">
            <div>
                <h1>Encore Healthcare QC Hub</h1>
                <p>Finished Product Analysis & Workflow Tracking</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    tab_list = ["📊 Analytics Dashboard", "📝 Log New Batch", "📋 Master Database"]
    if st.session_state.role == "admin": tab_list.append("🛡️ Admin Panel")
    tabs = st.tabs(tab_list)

    # --- TAB 1: ANALYTICS ---
    with tabs[0]:
        st.markdown("<br>", unsafe_allow_html=True)
        total_batches = len(df)
        released = len(df[df['status'] == 'Release']) if total_batches > 0 else 0
        avg_tat = df['Total TAT (Days)'].mean() if total_batches > 0 and 'Total TAT (Days)' in df else 0
        open_delays = len(df[df["delay_reason"].notna() & (df["delay_reason"] != "Within Time")]) if total_batches > 0 else 0
        
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f'<div class="trendy-card" style="border-left-color: #4318FF;"><div class="metric-label">Total Batches</div><div class="metric-value">{total_batches:,}</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="trendy-card" style="border-left-color: #05CD99;"><div class="metric-label">Released</div><div class="metric-value" style="color: #05CD99;">{released}</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="trendy-card" style="border-left-color: #F59E0B;"><div class="metric-label">Avg TAT (Days)</div><div class="metric-value" style="color: #F59E0B;">{avg_tat:.1f}</div></div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="trendy-card" style="border-left-color: #EF4444;"><div class="metric-label">Open Delays</div><div class="metric-value" style="color: #EF4444;">{open_delays}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if total_batches > 0 and 'Queue Time (Days)' in df and df['Queue Time (Days)'].notna().any():
            st.markdown("### 🚦 Micro-Stage Workflow Durations")
            stage_df = df[['batch_no', 'Queue Time (Days)', 'Testing Time (Days)', 'Review Time (Days)', 'COA Time (Days)']].dropna()
            fig_stack = px.bar(stage_df, x="batch_no", y=['Queue Time (Days)', 'Testing Time (Days)', 'Review Time (Days)', 'COA Time (Days)'], 
                               template="plotly_white", color_discrete_sequence=['#1E293B', '#4318FF', '#05CD99', '#F59E0B'])
            fig_stack.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(family="Plus Jakarta Sans"))
            st.plotly_chart(fig_stack, use_container_width=True)

    # --- TAB 2: INTAKE FORM ---
    with tabs[1]:
        st.markdown("<br>### 📝 Batch Registration Form", unsafe_allow_html=True)
        with st.form("full_intake_form", clear_on_submit=True):
            f_col1, f_col2, f_col3 = st.columns(3)
            with f_col1:
                product_name = st.text_input("Product Name *")
                batch_no = st.text_input("Batch Number *")
                analyst_name = st.text_input("Name of Analyst")
                status = st.selectbox("Status", ["In Progress", "Release", "Delayed"])
            with f_col2:
                sample_receipt_date = st.date_input("Sample Receipt Date", value=date.today())
                analysis_start_date = st.date_input("Analysis Start Date", value=None)
                analysis_completion_date = st.date_input("Analysis Completion Date", value=None)
            with f_col3:
                review_completion_date = st.date_input("Review Completion Date", value=None)
                coa_completion_date = st.date_input("COA Completion Date", value=None)
                delay_reason = st.selectbox("Delay Reason", ["Within Time", "Instrument Maintenance", "OOS Investigation", "Manpower Crunch", "Other"])
                actual_testing_hours = st.number_input("Actual Testing Time (Hours)", min_value=0.0)
                
            st.markdown("<br>", unsafe_allow_html=True)
            if st.form_submit_button("💾 Save Batch to Vault", type="primary", use_container_width=True):
                if not product_name or not batch_no:
                    st.error("Product Name and Batch Number are required.")
                else:
                    try:
                        with conn.session as s:
                            s.execute(text("""
                                INSERT INTO fp_analysis (product_name, batch_no, analyst_name, status, delay_reason, 
                                sample_receipt_date, analysis_start_date, analysis_completion_date, review_completion_date, 
                                coa_completion_date, actual_testing_hours) 
                                VALUES (:pn, :bn, :an, :st, :dr, :srd, :asd, :acd, :rcd, :ccd, :ath)
                            """), {"pn": product_name, "bn": batch_no, "an": analyst_name, "st": status, "dr": delay_reason, "srd": sample_receipt_date, "asd": analysis_start_date, "acd": analysis_completion_date, "rcd": review_completion_date, "ccd": coa_completion_date, "ath": actual_testing_hours})
                            s.commit()
                        st.success(f"Batch {batch_no} saved securely.")
                        st.rerun()
                    except Exception:
                        st.error("Error: Batch Number already exists in the system.")

    # --- TAB 3: LIVE GRID ---
    with tabs[2]:
        st.markdown("<br>### 📋 Centralized Database Editor", unsafe_allow_html=True)
        if not df.empty:
            edited_df = st.data_editor(df.drop(columns=['MonthYear'], errors='ignore'), use_container_width=True, hide_index=True)
            if st.button("💾 Commit Modifications", type="primary"):
                save_df = edited_df.drop(columns=['Queue Time (Days)', 'Testing Time (Days)', 'Review Time (Days)', 'COA Time (Days)', 'Total TAT (Days)'], errors='ignore')
                save_df.to_sql("fp_analysis", con=conn.engine, if_exists="replace", index=False)
                st.success("Database synchronized successfully!")
                st.rerun()

    # --- TAB 4: ADMIN PANEL ---
    if st.session_state.role == "admin":
        with tabs[3]:
            adm_col1, adm_col2 = st.columns([1, 2])
            with adm_col1:
                st.markdown("<br>### 👤 User Management", unsafe_allow_html=True)
                with st.form("create_user_form", clear_on_submit=True):
                    new_user = st.text_input("New Username")
                    new_pass = st.text_input("Default Password", type="password")
                    new_role = st.selectbox("Role", ["user", "admin"])
                    if st.form_submit_button("Create User", type="primary"):
                        if new_user and new_pass:
                            try:
                                with conn.session as s:
                                    s.execute(text("INSERT INTO users (username, password, role) VALUES (:u, :p, :r)"), {"u": new_user, "p": hash_password(new_pass), "r": new_role})
                                    s.commit()
                                st.success(f"User '{new_user}' created.")
                            except Exception:
                                st.error("Username already exists.")
                        else:
                            st.error("Fill all fields.")
                            
                st.markdown("#### Delete User")
                users_df = conn.query("SELECT id, username, role FROM users WHERE username != 'admin'", ttl=0)
                if not users_df.empty:
                    del_user = st.selectbox("Select user to delete", users_df['username'].tolist())
                    if st.button("Revoke Access"):
                        with conn.session as s:
                            s.execute(text("DELETE FROM users WHERE username = :u"), {"u": del_user})
                            s.commit()
                        st.success(f"User '{del_user}' removed.")
                        st.rerun()
            with adm_col2:
                st.markdown("<br>### 🕒 Access & Audit Logs", unsafe_allow_html=True)
                logs_df = conn.query("SELECT username, login_time, logout_time, usage_minutes FROM user_logs ORDER BY login_time DESC", ttl=0)
                st.dataframe(logs_df, use_container_width=True, hide_index=True)
