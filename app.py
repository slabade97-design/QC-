import hashlib
from datetime import date, datetime, timedelta
import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import text

# -------------------------------------------------------------
# 1. Page Config & Styling
# -------------------------------------------------------------
st.set_page_config(page_title="Encore QC Analytics", page_icon="🧬", layout="wide", initial_sidebar_state="expanded")

ENCORE_LOGO_URL = "https://encorehealthcare.in/wp-content/uploads/2023/12/encore-healthcare_transparent-1536x618.png"

PRODUCT_CLIENT_MAP = {
    "Becosules Capsules": "Pfizer Limited",
    "Becosules Z Capsules": "Pfizer Limited",
    "Imodium Capsules": "Kenvue Limited",
    "Stugeron Plus Tablets": "Dr. Reddy's Laboratories Limited",
    "Stugeron Forte Tablets": "Dr. Reddy's Laboratories Limited",
    "Ultracet Tablets": "Johnson & Johnson Pvt. Ltd",
    "Ultracet Semi_Tablets": "Johnson & Johnson Pvt. Ltd",
    "Topamac 25mg Tablets": "Johnson & Johnson Pvt. Ltd",
    "Topamac 50mg Tablets": "Johnson & Johnson Pvt. Ltd",
    "Topamac 100mg tablets": "Johnson & Johnson Pvt. Ltd",
    "Sibelium 5mg tablets": "Johnson & Johnson Pvt. Ltd",
    "Sibelium 10mg Tablets": "Johnson & Johnson Pvt. Ltd",
    "Risperdal 1mg Tablets": "Johnson & Johnson Pvt. Ltd",
    "Risperdal 2mg Tablets": "Johnson & Johnson Pvt. Ltd",
    "Risperdal 3mg tablets": "Johnson & Johnson Pvt. Ltd",
    "Risperdal 4mg Tablets": "Johnson & Johnson Pvt. Ltd",
    "Concor_10mg_Tablets": "Merck Specialities Private Limited",
    "Concor_5mg_Tablets": "Merck Specialities Private Limited",
    "Concor Cor_2.5mg_Tablets": "Merck Specialities Private Limited",
    "Concor Cor_1.25 mg_Tablets": "Merck Specialities Private Limited",
    "Concor Plus Tablets": "Merck Specialities Private Limited",
    "Calpol_500+_Tablet": "GSK (Glaxo Smithkline Pharma Limited)",
    "Calpol_650+_Tablets": "GSK (Glaxo Smithkline Pharma Limited)",
    "Calpol_500+_Tablets (Bulk)": "GSK (Glaxo Smithkline Pharma Limited)",
    "Zyloric_ 100mg_Tablets": "GSK (Glaxo Smithkline Pharma Limited)",
    "Zyloric_ 300mg_Tablets": "GSK (Glaxo Smithkline Pharma Limited)",
    "Lanoxin_Tablets": "GSK (Glaxo Smithkline Pharma Limited)",
    "Cobadex CZS_Tablets": "GSK (Glaxo Smithkline Pharma Limited)",
    "Zovirax_200mg_Tablets": "GSK (Glaxo Smithkline Pharma Limited)",
    "Zovirax_400mg_Tablets": "GSK (Glaxo Smithkline Pharma Limited)",
    "Zovirax_800mg_Tablets": "GSK (Glaxo Smithkline Pharma Limited)",
    "Zimig 250mg Tablets": "GSK (Glaxo Smithkline Pharma Limited)",
    "CCM Tablets": "GSK (Glaxo Smithkline Pharma Limited)",
    "Neurobion Forte Tablets": "P&G (Procter and Gamble) Health Limited",
    "Livogen Captab": "P&G (Procter and Gamble) Health Limited",
    "Livogen Z Captab": "P&G (Procter and Gamble) Health Limited",
    "Vicks Action_500mg_Tablets": "P&G (Procter and Gamble) Health Limited",
    "Alaspan AM Tablets": "Bayer Pharmaceuticals Private Limited",
    "Alaspan Tablets": "Bayer Pharmaceuticals Private Limited",
    "Polaramine Tablets": "Bayer Pharmaceuticals Private Limited",
    "Pangran Granules": "Haleon",
    "Crocin 650mg Tablets": "Haleon",
    "Crocin Pain Relief Tablets": "Haleon",
    "Crocin Advance Tablets": "Haleon",
    "Endoxy Capsules": "Encore Healthcare Private Limited",
    "Encipro 500mg Tablets": "Encore Healthcare Private Limited",
    "TAB-SUV Tablets": "Encore Healthcare Private Limited",
    "Xielol 50mg Tablets": "Encore Healthcare Private Limited",
    "Metroncore 250mg Tablets": "Encore Healthcare Private Limited",
    "Metroncore 500mg Tablets": "Encore Healthcare Private Limited",
    "Metroncore 400mg Tablets": "Encore Healthcare Private Limited",
    "Melomcore 5mg Tablets": "Encore Healthcare Private Limited",
    "Restigard-O Capsules": "Encore Healthcare Private Limited",
    "AD-CND Tablets": "Encore Healthcare Private Limited",
    "Ontadex Capsules": "Encore Healthcare Private Limited",
    "Xyctic 200mg Tablets": "Encore Healthcare Private Limited",
    "Encovolt Tablets": "Encore Healthcare Private Limited",
    "Melomcore 15mg Tablets": "Encore Healthcare Private Limited",
    "Parencore_1000mg_Tablets": "Encore Healthcare Private Limited",
    "UT-Flox_Tablets": "Encore Healthcare Private Limited",
    "Jimlig_100mg_Capsules": "Encore Healthcare Private Limited",
    "Jimlig_200mg_Capsules": "Encore Healthcare Private Limited",
    "Fe-sency_Tablets": "Encore Healthcare Private Limited",
    "Tofalig_5mg_Tablets": "Encore Healthcare Private Limited",
    "Atonl_ 50mg_TABLETS": "Encore Healthcare Private Limited",
    "Atonl_ 100mg_TABLETS": "Encore Healthcare Private Limited",
    "Jimlig_65mg SB_Capsules": "Encore Healthcare Private Limited",
    "Jimlig_130mg SB_Capsules": "Encore Healthcare Private Limited",
    "Encinim_Tablets": "Encore Healthcare Private Limited",
    "Entravo_10mg _Tablets": "Encore Healthcare Private Limited",
    "Entravo_15mg _Tablets": "Encore Healthcare Private Limited",
    "Entravo_20mg_Tablets": "Encore Healthcare Private Limited",
    "Flemico _Tablets": "Encore Healthcare Private Limited",
    "Gelabex_50mg_Tablets": "Encore Healthcare Private Limited",
    "Gelabex_100mg_Tablets": "Encore Healthcare Private Limited",
    "Gelabex_200mg_Tablets": "Encore Healthcare Private Limited",
    "Mebencore_100mg_Tablets": "Encore Healthcare Private Limited",
    "Encotac 150mg Tablets": "Encore Healthcare Private Limited",
    "Lirplan_25mg_Tablets": "Encore Healthcare Private Limited",
    "Lirplan_50mg_Tablets": "Encore Healthcare Private Limited",
    "Letapin_16mg_Tablets": "Encore Healthcare Private Limited",
    "Letapin_24mg_Tablets": "Encore Healthcare Private Limited",
    "Scino_2.5mg_Tablets": "Encore Healthcare Private Limited",
    "Scino_5mg_Tablets": "Encore Healthcare Private Limited",
    "Repsola_Tablets": "Encore Healthcare Private Limited",
    "Tab-SUV_250mg_Tablets": "Encore Healthcare Private Limited",
    "Enabolic_10mg_Tablets": "Encore Healthcare Private Limited",
    "Zower_Tablets": "Encore Healthcare Private Limited",
    "Ontadex BP_50mg_Capsules": "Encore Healthcare Private Limited",
    "Xyctic 400mg Tablets": "Encore Healthcare Private Limited",
    "Encofer_Tablets": "Encore Healthcare Private Limited"
}

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
    .stApp {{ background: #F7F9FC; }}
    
    .top-header {{
        background: linear-gradient(135deg, #0B1C3E 0%, #1A365D 100%);
        padding: 20px 30px; border-radius: 15px; color: white; margin-bottom: 30px;
        display: flex; align-items: center; box-shadow: 0 10px 25px rgba(11, 28, 62, 0.15);
    }}
    .top-header img {{ height: 50px; margin-right: 20px; }} 
    .top-header h1 {{ margin: 0; font-size: 2.2rem; font-weight: 800; }}
    .top-header p {{ margin: 5px 0 0 0; color: #94A3B8; font-weight: 500; }}

    .trendy-card {{ 
        background: #FFFFFF; border-radius: 16px; padding: 24px 20px; text-align: left; 
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.05); border-left: 6px solid #4318FF; 
        position: relative; overflow: hidden;
    }}
    .metric-value {{ font-size: 2.2rem; font-weight: 800; color: #1E293B; margin: 8px 0 0 0; }}
    .metric-label {{ color: #64748B; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; }}
    
    .stTabs [data-baseweb="tab-list"] {{ border-bottom: 2px solid #E2E8F0; }}
    .stTabs [aria-selected="true"] {{ border-bottom: 3px solid #4318FF; background-color: #FFFFFF; }}
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. Database Connection & Table Init
# -------------------------------------------------------------
conn = st.connection("postgresql", type="sql")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    with conn.session as s:
        s.execute(text("""
            CREATE TABLE IF NOT EXISTS qc_master_tracker (
                id SERIAL PRIMARY KEY, product_name TEXT, client_name TEXT, batch_no TEXT UNIQUE, ar_no TEXT,
                batch_size TEXT, mfg_date TEXT, exp_date TEXT, sample_qty TEXT,
                sample_receipt_date DATE, target_release_date DATE,
                chem_analyst TEXT, chem_qty TEXT, chem_start DATE, chem_end DATE,
                micro_analyst TEXT, micro_qty TEXT, micro_start DATE, micro_end DATE,
                chem_destruct_qty TEXT, chem_destroyed_by TEXT, 
                micro_destruct_qty TEXT, micro_destroyed_by TEXT,
                coa_completion_date DATE, status TEXT, delay_reason TEXT, remarks TEXT
            )
        """))
        s.execute(text("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, role TEXT NOT NULL)"))
        s.execute(text("CREATE TABLE IF NOT EXISTS user_logs (id SERIAL PRIMARY KEY, username TEXT, login_time TIMESTAMP, logout_time TIMESTAMP, usage_minutes REAL)"))
        
        if not s.execute(text("SELECT * FROM users WHERE username='admin'")).fetchone():
            s.execute(text("INSERT INTO users (username, password, role) VALUES (:u, :p, :r)"), {"u": "admin", "p": hash_password("admin@123"), "r": "admin"})
        s.commit()

init_db()

# -------------------------------------------------------------
# 3. Session & Auth Logic
# -------------------------------------------------------------
if 'logged_in' not in st.session_state:
    st.session_state.update({"logged_in": False, "username": "", "role": "", "log_id": None, "login_time": None})

def do_logout():
    if st.session_state.log_id:
        usage = (datetime.now() - st.session_state.login_time).total_seconds() / 60.0
        with conn.session as s:
            s.execute(text("UPDATE user_logs SET logout_time = :lo, usage_minutes = :um WHERE id = :id"), {"lo": datetime.now(), "um": usage, "id": st.session_state.log_id})
            s.commit()
    st.session_state.update({"logged_in": False, "username": "", "role": "", "log_id": None, "login_time": None})
    st.rerun()

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown(f'<div style="text-align:center;margin:30px 0;"><img src="{ENCORE_LOGO_URL}" style="height:70px;"><h2 style="color:#0B1C3E;font-weight:800;">Encore Healthcare</h2></div>', unsafe_allow_html=True)
        st.markdown('<div class="trendy-card" style="border-top:5px solid #4318FF;border-left:none;">', unsafe_allow_html=True)
        u_in = st.text_input("Username")
        p_in = st.text_input("Password", type="password")
        if st.button("Secure Login", type="primary", use_container_width=True):
            user = conn.query("SELECT id, role, password FROM users WHERE username = :u", params={"u": u_in})
            if not user.empty and user.iloc[0]['password'] == hash_password(p_in):
                st.session_state.update({"logged_in": True, "username": u_in, "role": user.iloc[0]['role'], "login_time": datetime.now()})
                with conn.session as s:
                    st.session_state.log_id = s.execute(text("INSERT INTO user_logs (username, login_time) VALUES (:u, :lt) RETURNING id"), {"u": u_in, "lt": st.session_state.login_time}).fetchone()[0]
                    s.commit()
                st.rerun()
            else:
                st.error("Invalid Credentials")
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 4. Main Application Hub
# -------------------------------------------------------------
else:
    st.sidebar.image(ENCORE_LOGO_URL, use_container_width=True)
    st.sidebar.markdown(f"<br>👤 **User:** {st.session_state.username}<br>🛡️ **Role:** {st.session_state.role.upper()}<br>", unsafe_allow_html=True)
    st.sidebar.button("🚪 Logout", on_click=do_logout, use_container_width=True)
    
    df = conn.query("SELECT * FROM qc_master_tracker", ttl=0)

    st.markdown(f'<div class="top-header"><img src="{ENCORE_LOGO_URL}"><div><h1>Encore QC Master Hub</h1><p>Finished Product Analysis Tracking</p></div></div>', unsafe_allow_html=True)

    tabs = st.tabs(["📊 Analytics Dashboard", "📝 Log New Batch", "📋 Master Database"] + (["🛡️ Admin Panel"] if st.session_state.role == "admin" else []))

    # --- TAB 1: ANALYTICS ---
    with tabs[0]:
        if not df.empty:
            df['sample_receipt_date'] = pd.to_datetime(df['sample_receipt_date'], errors='coerce')
            df['coa_completion_date'] = pd.to_datetime(df['coa_completion_date'], errors='coerce')
            
            total_batches = len(df)
            released = len(df[df['status'] == 'Released'])
            open_delays = len(df[df["delay_reason"].notna() & (df["delay_reason"] != "Within Time")])
            
            df['Total TAT'] = (df['coa_completion_date'] - df['sample_receipt_date']).dt.days
            avg_tat = df['Total TAT'].mean() if not df['Total TAT'].dropna().empty else 0
            
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f'<div class="trendy-card"><div class="metric-label">Total Batches</div><div class="metric-value">{total_batches}</div></div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="trendy-card" style="border-left-color: #05CD99;"><div class="metric-label">Released</div><div class="metric-value" style="color: #05CD99;">{released}</div></div>', unsafe_allow_html=True)
            c3.markdown(f'<div class="trendy-card" style="border-left-color: #F59E0B;"><div class="metric-label">Global Avg TAT (Days)</div><div class="metric-value" style="color: #F59E0B;">{avg_tat:.1f}</div></div>', unsafe_allow_html=True)
            c4.markdown(f'<div class="trendy-card" style="border-left-color: #EF4444;"><div class="metric-label">Open Delays</div><div class="metric-value" style="color: #EF4444;">{open_delays}</div></div>', unsafe_allow_html=True)

            st.markdown("---")
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                st.markdown("### 📈 Client Workload Distribution")
                client_counts = df['client_name'].value_counts().reset_index()
                client_counts.columns = ['Client', 'Count']
                fig_client = px.bar(client_counts, x='Client', y='Count', template="plotly_white", color_discrete_sequence=['#4318FF'])
                st.plotly_chart(fig_client, use_container_width=True)

            with col_chart2:
                st.markdown("### 🟢 Real-time Status Overview")
                status_counts = df['status'].value_counts().reset_index()
                status_counts.columns = ['Status', 'Count']
                fig_status = px.pie(status_counts, names='Status', values='Count', template="plotly_white", hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig_status, use_container_width=True)
        else:
            st.info("Awaiting batch data to populate analytics.")

    # --- TAB 2: INTAKE FORM ---
    with tabs[1]:
        st.markdown("### 📝 Master Log Registration")
        
        st.markdown("#### 📦 General Batch Information")
        g1, g2, g3, g4 = st.columns(4)
        
        # Selectbox for Product Name to ensure accurate mapping
        product_options = [""] + list(PRODUCT_CLIENT_MAP.keys())
        product_name = g1.selectbox("Product Name *", options=product_options)
        
        # Auto-fill Client Name based on the selection above
        auto_client = PRODUCT_CLIENT_MAP.get(product_name, "")
        client_name = g2.text_input("Client Name *", value=auto_client)
        
        batch_no = g3.text_input("Batch No. *")
        ar_no = g4.text_input("AR. No.")
        
        g5, g6, g7, g8 = st.columns(4)
        batch_size = g5.text_input("Batch Size")
        mfg_date = g6.text_input("Mfg Date (MM/YY)")
        exp_date = g7.text_input("Exp Date (MM/YY)")
        sample_qty = g8.text_input("Sample Quantity")

        g9, g10, _, _ = st.columns(4)
        sample_receipt_date = g9.date_input("Sample Receipt Date", value=date.today(), format="DD/MM/YYYY")
        
        # Auto Target Release Date (+6 Days)
        auto_target_date = sample_receipt_date + timedelta(days=6) if sample_receipt_date else None
        target_release_date = g10.date_input("Target Release Date (Auto +6 Days)", value=auto_target_date, format="DD/MM/YYYY", disabled=True)

        st.markdown("---")
        c_left, c_right = st.columns(2)
        with c_left:
            st.markdown("#### 🧪 Chemical Testing")
            chem_analyst = st.text_input("Chem Analyst")
            chem_qty = st.text_input("Chem Analysis Qty")
            chem_start = st.date_input("Chem Start Date", value=None, format="DD/MM/YYYY")
            chem_end = st.date_input("Chem Completion Date", value=None, format="DD/MM/YYYY")
        
        with c_right:
            st.markdown("#### 🧫 Microbiological Testing")
            micro_analyst = st.text_input("Micro Analyst")
            micro_qty = st.text_input("Micro Analysis Qty")
            micro_start = st.date_input("Micro Start Date", value=None, format="DD/MM/YYYY")
            micro_end = st.date_input("Micro Completion Date", value=None, format="DD/MM/YYYY")

        st.markdown("---")
        d_left, d_right = st.columns(2)
        with d_left:
            st.markdown("#### 🗑️ Chemical Destruction")
            chem_destruct_qty = st.text_input("Chem Destruct Qty")
            chem_destroyed_by = st.text_input("Chem Destroyed By")
        with d_right:
            st.markdown("#### 🗑️ Microbial Destruction")
            micro_destruct_qty = st.text_input("Micro Destruct Qty")
            micro_destroyed_by = st.text_input("Micro Destroyed By")

        st.markdown("---")
        st.markdown("#### 📄 Final Sign-Off & Status")
        f1, f2 = st.columns(2)
        coa_completion_date = f1.date_input("COA Completion Date", value=None, format="DD/MM/YYYY")
        remarks = f2.text_input("Remarks")

        # Dynamic Status Logic
        if coa_completion_date: derived_status = "Released"
        elif chem_end and micro_end: derived_status = "COA Awaited"
        elif chem_end or micro_end: derived_status = "Analysis Partially Completed"
        elif chem_start or micro_start: derived_status = "Under Analysis"
        elif sample_receipt_date: derived_status = "Sample Received"
        else: derived_status = "Pending"
        
        st.info(f"**Auto-Calculated Workflow Status:** {derived_status}")

        # Dynamic Delay Logic (Checking maximum date of analysis vs receipt)
        delay_reason = "Within Time"
        max_end_date = max(d for d in [chem_end, micro_end] if d) if chem_end or micro_end else None
        
        if sample_receipt_date and max_end_date:
            if (max_end_date - sample_receipt_date).days > 6:
                delay_reason = st.selectbox("Delay Reason (Required as TAT > 6 days) *", 
                    ["Instrument Maintenance", "OOS Investigation", "Manpower Crunch", "Pious Laboratory Await", "Other"])

        if st.button("💾 Save Batch Record", type="primary", use_container_width=True):
            if not product_name or not batch_no or not client_name:
                st.error("Product Name, Client Name, and Batch Number are required fields.")
            else:
                try:
                    with conn.session as s:
                        s.execute(text("""
                            INSERT INTO qc_master_tracker (
                                product_name, client_name, batch_no, ar_no, batch_size, mfg_date, exp_date, sample_qty,
                                sample_receipt_date, target_release_date, chem_analyst, chem_qty, chem_start, chem_end,
                                micro_analyst, micro_qty, micro_start, micro_end, chem_destruct_qty, chem_destroyed_by,
                                micro_destruct_qty, micro_destroyed_by, coa_completion_date, status, delay_reason, remarks
                            ) VALUES (
                                :pn, :cn, :bn, :ar, :bs, :md, :ed, :sq, :srd, :trd, :ca, :cq, :cs, :ce, :ma, :mq, :ms, :me,
                                :cdq, :cdb, :mdq, :mdb, :coa, :st, :dr, :rm
                            )
                        """), {
                            "pn": product_name, "cn": client_name, "bn": batch_no, "ar": ar_no, "bs": batch_size,
                            "md": mfg_date, "ed": exp_date, "sq": sample_qty, "srd": sample_receipt_date, "trd": target_release_date,
                            "ca": chem_analyst, "cq": chem_qty, "cs": chem_start, "ce": chem_end,
                            "ma": micro_analyst, "mq": micro_qty, "ms": micro_start, "me": micro_end,
                            "cdq": chem_destruct_qty, "cdb": chem_destroyed_by, "mdq": micro_destruct_qty, "mdb": micro_destroyed_by,
                            "coa": coa_completion_date, "st": derived_status, "dr": delay_reason, "rm": remarks
                        })
                        s.commit()
                    st.success(f"Batch {batch_no} successfully logged to vault.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: Batch Number already exists or format is invalid. ({e})")

    # --- TAB 3: LIVE GRID ---
    with tabs[2]:
        st.markdown("### 📋 Universal Centralized Database")
        if not df.empty:
            edited_df = st.data_editor(
                df, use_container_width=True, hide_index=True,
                column_config={
                    "sample_receipt_date": st.column_config.DateColumn("Sample Receipt Date", format="DD/MM/YYYY"),
                    "target_release_date": st.column_config.DateColumn("Target Release Date", format="DD/MM/YYYY"),
                    "chem_start": st.column_config.DateColumn("Chem Start Date", format="DD/MM/YYYY"),
                    "chem_end": st.column_config.DateColumn("Chem End Date", format="DD/MM/YYYY"),
                    "micro_start": st.column_config.DateColumn("Micro Start Date", format="DD/MM/YYYY"),
                    "micro_end": st.column_config.DateColumn("Micro End Date", format="DD/MM/YYYY"),
                    "coa_completion_date": st.column_config.DateColumn("COA Date", format="DD/MM/YYYY")
                }
            )
            if st.button("💾 Commit Table Modifications", type="primary"):
                edited_df.to_sql("qc_master_tracker", con=conn.engine, if_exists="replace", index=False)
                st.success("Database synchronized successfully!")
                st.rerun()

    # --- TAB 4: ADMIN PANEL ---
    if st.session_state.role == "admin":
        with tabs[3]:
            adm1, adm2 = st.columns([1, 2])
            with adm1:
                st.markdown("### 👤 User Management")
                with st.form("create_user_form", clear_on_submit=True):
                    new_user = st.text_input("New Username")
                    new_pass = st.text_input("Default Password", type="password")
                    new_role = st.selectbox("Role", ["user", "admin"])
                    if st.form_submit_button("Create User", type="primary"):
                        try:
                            with conn.session as s:
                                s.execute(text("INSERT INTO users (username, password, role) VALUES (:u, :p, :r)"), {"u": new_user, "p": hash_password(new_pass), "r": new_role})
                                s.commit()
                            st.success(f"User '{new_user}' created.")
                        except: st.error("Username already exists.")
                            
                st.markdown("#### Delete User")
                users_df = conn.query("SELECT id, username, role FROM users WHERE username != 'admin'", ttl=0)
                if not users_df.empty:
                    del_user = st.selectbox("Select user to delete", users_df['username'].tolist())
                    if st.button("Revoke Access"):
                        with conn.session as s:
                            s.execute(text("DELETE FROM users WHERE username = :u"), {"u": del_user})
                            s.commit()
                        st.success(f"User removed.")
                        st.rerun()
            with adm2:
                st.markdown("### 🕒 Access Logs")
                logs_df = conn.query("SELECT username, login_time, logout_time, usage_minutes FROM user_logs ORDER BY login_time DESC", ttl=0)
                st.dataframe(logs_df, use_container_width=True, hide_index=True, column_config={
                    "login_time": st.column_config.DatetimeColumn("Login Time", format="DD/MM/YYYY HH:mm"),
                    "logout_time": st.column_config.DatetimeColumn("Logout Time", format="DD/MM/YYYY HH:mm")
                })
