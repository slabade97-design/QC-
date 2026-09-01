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
    .top-header {{ background: linear-gradient(135deg, #0B1C3E 0%, #1A365D 100%); padding: 20px 30px; border-radius: 15px; color: white; margin-bottom: 30px; display: flex; align-items: center; box-shadow: 0 10px 25px rgba(11, 28, 62, 0.15); }}
    .top-header img {{ height: 50px; margin-right: 20px; }} 
    .top-header h1 {{ margin: 0; font-size: 2.2rem; font-weight: 800; }}
    .top-header p {{ margin: 5px 0 0 0; color: #94A3B8; font-weight: 500; }}
    .trendy-card {{ background: #FFFFFF; border-radius: 16px; padding: 24px 20px; text-align: left; box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.05); border-left: 6px solid #4318FF; position: relative; overflow: hidden; }}
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
    # Block 1: Main Tracker Table
    with conn.session as s:
        s.execute(text("""
            CREATE TABLE IF NOT EXISTS qc_master_tracker (
                id SERIAL PRIMARY KEY, product_name TEXT, client_name TEXT, batch_no TEXT UNIQUE, ar_no TEXT,
                batch_size TEXT, mfg_date TEXT, exp_date TEXT, sample_qty TEXT,
                sample_receipt_date DATE, target_release_date DATE,
                chem_analyst TEXT, chem_qty TEXT, chem_start TIMESTAMP, chem_end TIMESTAMP, chem_analysis_hrs REAL,
                micro_analyst TEXT, micro_qty TEXT, micro_start TIMESTAMP, micro_end TIMESTAMP, micro_analysis_hrs REAL,
                total_analysis_hrs REAL, chem_destruct_qty TEXT, chem_destroyed_by TEXT, 
                micro_destruct_qty TEXT, micro_destroyed_by TEXT,
                coa_completion_date DATE, status TEXT, delay_reason TEXT, remarks TEXT
            )
        """))
        s.commit()
        
    # Block 2: Safe Column Alteration (Independent Transaction to prevent aborts)
    try:
        with conn.session as s:
            s.execute(text("ALTER TABLE qc_master_tracker ADD COLUMN IF NOT EXISTS total_analysis_hrs REAL"))
            s.commit()
    except Exception:
        pass

    # Block 3: User & Log Tables
    with conn.session as s:
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
            
            # Sub-graph: Time Analysis per Batch
            st.markdown("### ⏱️ Analysis Time per Batch (Chemical vs Micro)")
            time_df = df[['batch_no', 'chem_analysis_hrs', 'micro_analysis_hrs']].dropna(subset=['batch_no']).copy()
            # Melt dataframe to plot stacked bars
            time_df_melted = time_df.melt(id_vars="batch_no", value_vars=['chem_analysis_hrs', 'micro_analysis_hrs'], var_name="Analysis Type", value_name="Hours")
            fig_time = px.bar(time_df_melted, x="batch_no", y="Hours", color="Analysis Type", template="plotly_white", color_discrete_sequence=["#4318FF", "#05CD99"])
            fig_time.update_layout(xaxis_title="Batch Number", yaxis_title="Time Required (Hours)")
            st.plotly_chart(fig_time, use_container_width=True)
            
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
        
        # New Product Handling Logic
        product_options = [""] + list(PRODUCT_CLIENT_MAP.keys()) + ["➕ Add New Product..."]
        selected_product = g1.selectbox("Product Name *", options=product_options)
        
        if selected_product == "➕ Add New Product...":
            product_name = g1.text_input("Enter New Product Name *")
            client_name = g2.text_input("Enter Client Name *")
        else:
            product_name = selected_product
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
            
            c_s1, c_s2 = st.columns(2)
            chem_start_d = c_s1.date_input("Chem Start Date", value=None, format="DD/MM/YYYY")
            chem_start_t = c_s2.time_input("Chem Start Time", value=None)
            
            c_e1, c_e2 = st.columns(2)
            chem_end_d = c_e1.date_input("Chem Completion Date", value=None, format="DD/MM/YYYY")
            chem_end_t = c_e2.time_input("Chem Completion Time", value=None)
            
            chem_start = datetime.combine(chem_start_d, chem_start_t) if chem_start_d and chem_start_t else None
            chem_end = datetime.combine(chem_end_d, chem_end_t) if chem_end_d and chem_end_t else None
            chem_hours = (chem_end - chem_start).total_seconds() / 3600 if chem_start and chem_end else 0
            
            if chem_hours > 0:
                st.success(f"⏱️ Calculated Chem Time: {chem_hours:.2f} Hrs")

        with c_right:
            st.markdown("#### 🧫 Microbiological Testing")
            micro_analyst = st.text_input("Micro Analyst")
            micro_qty = st.text_input("Micro Analysis Qty")
            
            m_s1, m_s2 = st.columns(2)
            micro_start_d = m_s1.date_input("Micro Start Date", value=None, format="DD/MM/YYYY")
            micro_start_t = m_s2.time_input("Micro Start Time", value=None)
            
            m_e1, m_e2 = st.columns(2)
            micro_end_d = m_e1.date_input("Micro Completion Date", value=None, format="DD/MM/YYYY")
            micro_end_t = m_e2.time_input("Micro Completion Time", value=None)

            micro_start = datetime.combine(micro_start_d, micro_start_t) if micro_start_d and micro_start_t else None
            micro_end = datetime.combine(micro_end_d, micro_end_t) if micro_end_d and micro_end_t else None
            micro_hours = (micro_end - micro_start).total_seconds() / 3600 if micro_start and micro_end else 0
            
            if micro_hours > 0:
                st.success(f"⏱️ Calculated Micro Time: {micro_hours:.2f} Hrs")

        # Total Calculation
        total_analysis_hrs = chem_hours + micro_hours
        if total_analysis_hrs > 0:
            st.info(f"**Total Combined Analysis Time:** {total_analysis_hrs:.2f} Hrs")

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

        # Dynamic Delay Reason + Custom Input
        delay_reason = "Within Time"
        max_end_date = max(d for d in [chem_end, micro_end] if d) if chem_end or micro_end else None
        
        if sample_receipt_date and max_end_date:
            if (max_end_date.date() - sample_receipt_date).days > 6:
                delay_options = ["Instrument Maintenance", "OOS Investigation", "Manpower Crunch", "Pious Laboratory Await", "Other", "➕ Add New Reason..."]
                selected_delay = st.selectbox("Delay Reason (Required as TAT > 6 days) *", delay_options)
                
                if selected_delay == "➕ Add New Reason...":
                    delay_reason = st.text_input("Enter Custom Delay Reason *")
                else:
                    delay_reason = selected_delay

        if st.button("💾 Save Batch Record", type="primary", use_container_width=True):
            if not product_name or not batch_no or not client_name:
                st.error("Product Name, Client Name, and Batch Number are required fields.")
            else:
                try:
                    with conn.session as s:
                        s.execute(text("""
                            INSERT INTO qc_master_tracker (
                                product_name, client_name, batch_no, ar_no, batch_size, mfg_date, exp_date, sample_qty,
                                sample_receipt_date, target_release_date, chem_analyst, chem_qty, chem_start, chem_end, chem_analysis_hrs,
                                micro_analyst, micro_qty, micro_start, micro_end, micro_analysis_hrs, total_analysis_hrs, chem_destruct_qty, chem_destroyed_by,
                                micro_destruct_qty, micro_destroyed_by, coa_completion_date, status, delay_reason, remarks
                            ) VALUES (
                                :pn, :cn, :bn, :ar, :bs, :md, :ed, :sq, :srd, :trd, :ca, :cq, :cs, :ce, :c_hrs, :ma, :mq, :ms, :me, :m_hrs, :t_hrs,
                                :cdq, :cdb, :mdq, :mdb, :coa, :st, :dr, :rm
                            )
                        """), {
                            "pn": product_name, "cn": client_name, "bn": batch_no, "ar": ar_no, "bs": batch_size,
                            "md": mfg_date, "ed": exp_date, "sq": sample_qty, "srd": sample_receipt_date, "trd": target_release_date,
                            "ca": chem_analyst, "cq": chem_qty, "cs": chem_start, "ce": chem_end, "c_hrs": chem_hours,
                            "ma": micro_analyst, "mq": micro_qty, "ms": micro_start, "me": micro_end, "m_hrs": micro_hours, "t_hrs": total_analysis_hrs,
                            "cdq": chem_destruct_qty, "cdb": chem_destroyed_by, "mdq": micro_destruct_qty, "mdb": micro_destroyed_by,
                            "coa": coa_completion_date, "st": derived_status, "dr": delay_reason, "rm": remarks
                        })
                        s.commit()
                    st.success(f"Batch {batch_no} successfully logged to vault.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: Batch Number already exists or format is invalid. ({e})")

    # --- TAB 3: LIVE GRID & EXCEL UPLOAD ---
    with tabs[2]:
        st.markdown("### 📋 Universal Centralized Database")
        
        # Excel Upload Section to ingest historical data rapidly
        with st.expander("📂 Bulk Upload from Master Excel Template"):
            st.info("Upload your existing 'QC_Finished_Product_Analysis_Tracking_Template' to merge data directly into the system.")
            uploaded_file = st.file_uploader("Select Excel File", type=["xlsx", "xlsm"])
            
            if uploaded_file and st.button("Merge Data to Database", type="primary"):
                try:
                    upload_df = pd.read_excel(uploaded_file, sheet_name=0)
                    
                    # The first row contains secondary sub-headers in your excel file. We skip index 0.
                    upload_df = upload_df.iloc[1:].copy()
                    
                    # Explicit mapping from Excel Column Position -> Database Schema
                    # This prevents 'Unnamed: 12' pandas errors
                    rename_map = {
                        upload_df.columns[1]: 'product_name',
                        upload_df.columns[2]: 'client_name',
                        upload_df.columns[3]: 'batch_no',
                        upload_df.columns[4]: 'ar_no',
                        upload_df.columns[5]: 'batch_size',
                        upload_df.columns[6]: 'mfg_date',
                        upload_df.columns[7]: 'exp_date',
                        upload_df.columns[8]: 'sample_qty',
                        upload_df.columns[9]: 'sample_receipt_date',
                        upload_df.columns[10]: 'target_release_date',
                        upload_df.columns[11]: 'chem_analyst',
                        upload_df.columns[12]: 'chem_qty',
                        upload_df.columns[13]: 'chem_start',
                        upload_df.columns[14]: 'chem_end',
                        upload_df.columns[15]: 'chem_analysis_hrs',
                        upload_df.columns[16]: 'micro_analyst',
                        upload_df.columns[17]: 'micro_qty',
                        upload_df.columns[18]: 'micro_start',
                        upload_df.columns[19]: 'micro_end',
                        upload_df.columns[20]: 'micro_analysis_hrs',
                        upload_df.columns[21]: 'total_analysis_hrs',
                        upload_df.columns[22]: 'coa_completion_date',
                        upload_df.columns[24]: 'status',
                        upload_df.columns[25]: 'chem_destruct_qty',
                        upload_df.columns[26]: 'chem_destroyed_by',
                        upload_df.columns[27]: 'micro_destruct_qty',
                        upload_df.columns[28]: 'micro_destroyed_by',
                        upload_df.columns[29]: 'delay_reason',
                        upload_df.columns[30]: 'remarks',
                    }
                    
                    db_df = upload_df[list(rename_map.keys())].rename(columns=rename_map)
                    db_df.dropna(subset=['batch_no'], inplace=True) # Drop entirely blank rows
                    
                    # Clean and format dates safely for SQL insertion
                    for col in ['sample_receipt_date', 'target_release_date', 'chem_start', 'chem_end', 'micro_start', 'micro_end', 'coa_completion_date']:
                        db_df[col] = pd.to_datetime(db_df[col], errors='coerce')
                    
                    # Clean and format numeric time cols
                    for col in ['chem_analysis_hrs', 'micro_analysis_hrs', 'total_analysis_hrs']:
                        db_df[col] = pd.to_numeric(db_df[col], errors='coerce').fillna(0)
                        
                    # Commit parsed records to database automatically
                    db_df.to_sql("qc_master_tracker", con=conn.engine, if_exists="append", index=False)
                    st.success("Historical Excel Data successfully synchronized with the Vault!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error parsing uploaded file. Please ensure it perfectly matches the standard template. Details: {e}")

        # Live Editable Data Grid
        if not df.empty:
            edited_df = st.data_editor(
                df, use_container_width=True, hide_index=True,
                column_config={
                    "sample_receipt_date": st.column_config.DateColumn("Sample Receipt Date", format="DD/MM/YYYY"),
                    "target_release_date": st.column_config.DateColumn("Target Release Date", format="DD/MM/YYYY"),
                    "chem_start": st.column_config.DatetimeColumn("Chem Start", format="DD/MM/YYYY HH:mm"),
                    "chem_end": st.column_config.DatetimeColumn("Chem End", format="DD/MM/YYYY HH:mm"),
                    "chem_analysis_hrs": st.column_config.NumberColumn("Chem Hrs", format="%.2f"),
                    "micro_start": st.column_config.DatetimeColumn("Micro Start", format="DD/MM/YYYY HH:mm"),
                    "micro_end": st.column_config.DatetimeColumn("Micro End", format="DD/MM/YYYY HH:mm"),
                    "micro_analysis_hrs": st.column_config.NumberColumn("Micro Hrs", format="%.2f"),
                    "total_analysis_hrs": st.column_config.NumberColumn("Total Hrs", format="%.2f"),
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
