import hashlib
from datetime import date, datetime
import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import text

# -------------------------------------------------------------
# 1. Page Config & Premium Encore Healthcare Styling
# -------------------------------------------------------------
st.set_page_config(
    page_title="Encore QC Analytics",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Official Encore Healthcare Logo
ENCORE_LOGO_URL = "https://encorehealthcare.in/wp-content/uploads/2023/12/encore-healthcare_transparent-1536x618.png"

st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* =========================================================
   GLOBAL
   ========================================================= */

html, body, [class*="css"] {{
    font-family: 'Plus Jakarta Sans', sans-serif;
}}

.stApp {{
    background:
        radial-gradient(
            circle at 5% 0%,
            rgba(67,24,255,0.035),
            transparent 25%
        ),
        radial-gradient(
            circle at 95% 10%,
            rgba(5,205,153,0.035),
            transparent 25%
        ),
        #F7F9FC;
}}

#MainMenu {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}

header {{
    visibility: hidden;
}}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {{
    background:
        linear-gradient(
            180deg,
            #06142D 0%,
            #0B1C3E 50%,
            #102C54 100%
        );

    border-right: 1px solid rgba(255,255,255,0.08);
}}

section[data-testid="stSidebar"] * {{
    color: #E2E8F0;
}}

section[data-testid="stSidebar"] img {{
    padding: 12px 8px 18px 8px;
}}

section[data-testid="stSidebar"] hr {{
    border-color: rgba(255,255,255,0.10);
}}

section[data-testid="stSidebar"] button {{
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.10);
    background: rgba(255,255,255,0.055);
    transition: all 0.25s ease;
}}

section[data-testid="stSidebar"] button:hover {{
    background: rgba(255,255,255,0.12);
    border-color: rgba(255,255,255,0.18);
    transform: translateY(-1px);
}}


/* =========================================================
   DASHBOARD HEADER
   ========================================================= */

.top-header {{
    position: relative;
    overflow: hidden;

    background:
        radial-gradient(
            circle at 90% 20%,
            rgba(67,24,255,0.30),
            transparent 27%
        ),
        radial-gradient(
            circle at 10% 100%,
            rgba(5,205,153,0.13),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #06142D 0%,
            #0B1C3E 48%,
            #183A69 100%
        );

    padding: 24px 30px;
    border-radius: 18px;

    color: white;
    margin-bottom: 28px;

    display: flex;
    align-items: center;

    box-shadow:
        0 15px 40px rgba(11,28,62,0.18),
        inset 0 1px 0 rgba(255,255,255,0.07);

    animation: headerEnter 0.65s ease-out;
}}

.top-header::before {{
    content: '';

    position: absolute;

    width: 220px;
    height: 220px;

    right: -70px;
    top: -110px;

    border-radius: 50%;

    background: rgba(255,255,255,0.035);

    animation: floatingOrb 8s ease-in-out infinite;
}}

.top-header::after {{
    content: '';

    position: absolute;

    width: 130px;
    height: 130px;

    right: 180px;
    bottom: -90px;

    border-radius: 50%;

    background: rgba(67,24,255,0.10);

    animation: floatingOrb 10s ease-in-out infinite reverse;
}}

.top-header img {{
    height: 56px;
    width: auto;

    margin-right: 22px;

    position: relative;
    z-index: 2;

    animation: logoFloat 4s ease-in-out infinite;
}}

.top-header h1 {{
    margin: 0;

    font-size: 2.1rem;
    font-weight: 800;

    letter-spacing: -0.6px;

    position: relative;
    z-index: 2;
}}

.top-header p {{
    margin: 6px 0 0 0;

    color: #A8B7CC;

    font-weight: 500;
    font-size: 0.90rem;

    position: relative;
    z-index: 2;
}}


/* =========================================================
   KPI CARDS
   ========================================================= */

.trendy-card {{
    position: relative;
    overflow: hidden;

    background:
        linear-gradient(
            145deg,
            #FFFFFF 0%,
            #FBFCFF 100%
        );

    border-radius: 16px;

    padding: 22px 20px;

    text-align: left;

    box-shadow:
        0 5px 20px rgba(15,23,42,0.055),
        0 1px 2px rgba(15,23,42,0.04);

    border-left: 5px solid #4318FF;

    transition:
        transform 0.30s ease,
        box-shadow 0.30s ease;

    animation: cardEnter 0.55s ease-out both;
}}

.trendy-card:hover {{
    transform: translateY(-5px);

    box-shadow:
        0 18px 38px rgba(15,23,42,0.11),
        0 5px 12px rgba(15,23,42,0.04);
}}

.trendy-card::after {{
    content: '';

    position: absolute;

    width: 105px;
    height: 105px;

    right: -38px;
    top: -38px;

    border-radius: 50%;

    background:
        linear-gradient(
            135deg,
            rgba(67,24,255,0.025),
            rgba(67,24,255,0.10)
        );

    transition: transform 0.5s ease;
}}

.trendy-card:hover::after {{
    transform: scale(1.35);
}}

.metric-value {{
    font-size: 2.35rem;

    font-weight: 800;

    color: #1E293B;

    margin: 8px 0 0 0;

    letter-spacing: -1px;
}}

.metric-label {{
    color: #64748B;

    font-size: 0.76rem;

    font-weight: 800;

    text-transform: uppercase;

    letter-spacing: 1.1px;
}}


/* =========================================================
   TABS
   ========================================================= */

.stTabs [data-baseweb="tab-list"] {{
    gap: 6px;

    border-bottom: 1px solid #E2E8F0;

    padding-bottom: 0;
}}

.stTabs [data-baseweb="tab"] {{
    background: transparent;

    border: none;

    padding: 13px 19px;

    color: #64748B;

    font-weight: 700;

    transition:
        color 0.2s ease,
        background 0.2s ease,
        transform 0.2s ease;
}}

.stTabs [data-baseweb="tab"]:hover {{
    color: #0B1C3E;

    background: rgba(67,24,255,0.035);

    transform: translateY(-1px);
}}

.stTabs [aria-selected="true"] {{
    color: #0B1C3E !important;

    border-bottom: 3px solid #4318FF;

    background: #FFFFFF;

    border-radius: 9px 9px 0 0;

    box-shadow:
        0 -2px 10px rgba(15,23,42,0.025);
}}


/* =========================================================
   INPUTS
   ========================================================= */

div[data-baseweb="input"],
div[data-baseweb="select"] {{
    border-radius: 10px;
}}

input {{
    border-radius: 10px !important;
}}

textarea {{
    border-radius: 10px !important;
}}

div[data-baseweb="input"]:focus-within {{
    border-color: #4318FF !important;

    box-shadow:
        0 0 0 1px rgba(67,24,255,0.15) !important;
}}


/* =========================================================
   PRIMARY BUTTONS
   ========================================================= */

button[kind="primary"] {{
    border-radius: 10px !important;

    font-weight: 700 !important;

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease !important;
}}

button[kind="primary"]:hover {{
    transform: translateY(-2px);

    box-shadow:
        0 9px 22px rgba(67,24,255,0.22) !important;
}}


/* =========================================================
   FORMS
   ========================================================= */

[data-testid="stForm"] {{
    background:
        linear-gradient(
            145deg,
            #FFFFFF 0%,
            #FBFCFF 100%
        );

    border: 1px solid #E8EDF5;

    border-radius: 17px;

    padding: 25px;

    box-shadow:
        0 5px 20px rgba(15,23,42,0.045);
}}


/* =========================================================
   DATAFRAME
   ========================================================= */

[data-testid="stDataFrame"] {{
    border-radius: 14px;

    overflow: hidden;

    border: 1px solid #E8EDF5;

    box-shadow:
        0 5px 20px rgba(15,23,42,0.045);
}}


/* =========================================================
   LOGIN SCREEN
   ========================================================= */

.login-background {{
    position: fixed;

    inset: 0;

    width: 100vw;
    height: 100vh;

    overflow: hidden;

    background:
        radial-gradient(
            circle at 15% 20%,
            rgba(67,24,255,0.22),
            transparent 30%
        ),
        radial-gradient(
            circle at 85% 80%,
            rgba(5,205,153,0.14),
            transparent 28%
        ),
        linear-gradient(
            135deg,
            #040D20 0%,
            #0B1C3E 48%,
            #102B52 100%
        );

    z-index: -1;
}}


/* =========================================================
   LOGIN ANIMATED ORBS
   ========================================================= */

.login-orb {{
    position: absolute;

    border-radius: 50%;

    opacity: 0.45;

    animation:
        loginOrbFloat 10s ease-in-out infinite;
}}

.orb-one {{
    width: 280px;
    height: 280px;

    background: rgba(67,24,255,0.17);

    top: 6%;
    left: 7%;
}}

.orb-two {{
    width: 210px;
    height: 210px;

    background: rgba(5,205,153,0.13);

    bottom: 10%;
    right: 10%;

    animation-delay: -3s;
}}

.orb-three {{
    width: 130px;
    height: 130px;

    background: rgba(255,255,255,0.055);

    top: 56%;
    left: 22%;

    animation-delay: -6s;
}}


/* =========================================================
   LOGIN CARD
   ========================================================= */

.login-card {{
    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.985),
            rgba(248,250,255,0.965)
        );

    border: 1px solid rgba(255,255,255,0.70);

    border-radius: 24px;

    padding: 34px 38px 20px 38px;

    box-shadow:
        0 30px 80px rgba(0,0,0,0.25),
        0 8px 30px rgba(0,0,0,0.12);

    backdrop-filter: blur(18px);

    animation:
        loginCardEnter 0.8s cubic-bezier(.2,.8,.2,1);
}}


/* =========================================================
   LOGIN LOGO
   ========================================================= */

.login-logo {{
    width: 180px;

    display: block;

    margin: 0 auto 16px auto;

    animation:
        loginLogoEnter 0.9s ease-out,
        loginLogoFloat 4s ease-in-out 1s infinite;
}}


/* =========================================================
   LOGIN TEXT
   ========================================================= */

.login-title {{
    text-align: center;

    color: #0B1C3E;

    font-size: 1.65rem;

    font-weight: 800;

    margin-bottom: 4px;
}}

.login-subtitle {{
    text-align: center;

    color: #64748B;

    font-size: 0.82rem;

    font-weight: 600;

    margin-bottom: 23px;
}}


/* =========================================================
   LOGIN ACCENT
   ========================================================= */

.login-accent {{
    height: 4px;

    width: 52px;

    border-radius: 20px;

    margin: 0 auto 22px auto;

    background:
        linear-gradient(
            90deg,
            #4318FF,
            #05CD99
        );

    animation:
        accentGrow 0.8s ease-out;
}}


/* =========================================================
   LOGIN FOOTER
   ========================================================= */

.login-footer {{
    text-align: center;

    margin-top: 20px;

    color: #94A3B8;

    font-size: 0.72rem;

    font-weight: 600;

    line-height: 1.6;
}}


/* =========================================================
   ANIMATIONS
   ========================================================= */

@keyframes loginCardEnter {{

    from {{
        opacity: 0;

        transform:
            translateY(35px)
            scale(0.97);
    }}

    to {{
        opacity: 1;

        transform:
            translateY(0)
            scale(1);
    }}
}}

@keyframes loginLogoEnter {{

    from {{
        opacity: 0;

        transform:
            translateY(-18px)
            scale(0.88);
    }}

    to {{
        opacity: 1;

        transform:
            translateY(0)
            scale(1);
    }}
}}

@keyframes loginLogoFloat {{

    0%, 100% {{
        transform: translateY(0);
    }}

    50% {{
        transform: translateY(-5px);
    }}
}}

@keyframes loginOrbFloat {{

    0%, 100% {{
        transform:
            translate(0,0)
            scale(1);
    }}

    50% {{
        transform:
            translate(25px,-20px)
            scale(1.08);
    }}
}}

@keyframes headerEnter {{

    from {{
        opacity: 0;
        transform: translateY(-15px);
    }}

    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

@keyframes cardEnter {{

    from {{
        opacity: 0;
        transform: translateY(15px);
    }}

    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

@keyframes logoFloat {{

    0%, 100% {{
        transform: translateY(0);
    }}

    50% {{
        transform: translateY(-3px);
    }}
}}

@keyframes floatingOrb {{

    0%, 100% {{
        transform: translate(0,0);
    }}

    50% {{
        transform: translate(-18px,15px);
    }}
}}

@keyframes accentGrow {{

    from {{
        width: 0;
        opacity: 0;
    }}

    to {{
        width: 52px;
        opacity: 1;
    }}
}}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 768px) {{

    .top-header {{
        padding: 20px;
    }}

    .top-header img {{
        height: 42px;
        margin-right: 14px;
    }}

    .top-header h1 {{
        font-size: 1.35rem;
    }}

    .top-header p {{
        font-size: 0.75rem;
    }}

    .trendy-card {{
        padding: 18px;
    }}

    .metric-value {{
        font-size: 1.9rem;
    }}

    .login-card {{
        padding: 28px 22px 18px 22px;
    }}

    .login-logo {{
        width: 155px;
    }}
}}

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
                id SERIAL PRIMARY KEY,
                product_name TEXT,
                strength TEXT,
                batch_no TEXT UNIQUE,
                sample_receipt_date DATE,
                analysis_start_date DATE,
                analysis_completion_date DATE,
                review_completion_date DATE,
                coa_completion_date DATE,
                target_release_date DATE,
                analyst_name TEXT,
                status TEXT DEFAULT 'In Progress',
                delay_reason TEXT,
                actual_testing_hours REAL
            )
        """))

        s.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """))

        s.execute(text("""
            CREATE TABLE IF NOT EXISTS user_logs (
                id SERIAL PRIMARY KEY,
                username TEXT,
                login_time TIMESTAMP,
                logout_time TIMESTAMP,
                usage_minutes REAL
            )
        """))

        admin_check = s.execute(
            text(
                "SELECT * FROM users WHERE username='admin'"
            )
        ).fetchone()

        if not admin_check:

            s.execute(
                text("""
                    INSERT INTO users
                    (username, password, role)
                    VALUES (:u, :p, :r)
                """),
                {
                    "u": "admin",
                    "p": hash_password("admin@123"),
                    "r": "admin"
                }
            )

        s.commit()


init_db()


# -------------------------------------------------------------
# 3. Session & Auth
# -------------------------------------------------------------

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.log_id = None
    st.session_state.login_time = None


def do_logout():

    if st.session_state.log_id:

        logout_time = datetime.now()

        usage_duration = (
            logout_time -
            st.session_state.login_time
        ).total_seconds() / 60.0

        with conn.session as s:

            s.execute(
                text("""
                    UPDATE user_logs
                    SET logout_time = :lo,
                        usage_minutes = :um
                    WHERE id = :id
                """),
                {
                    "lo": logout_time,
                    "um": usage_duration,
                    "id": st.session_state.log_id
                }
            )

            s.commit()

    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.log_id = None
    st.session_state.login_time = None

    st.rerun()


# -------------------------------------------------------------
# 4. Login Screen
# -------------------------------------------------------------

if not st.session_state.logged_in:

    st.markdown(
        """
        <div class="login-background">

            <div class="login-orb orb-one"></div>

            <div class="login-orb orb-two"></div>

            <div class="login-orb orb-three"></div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<br><br><br>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(
        [1, 1.2, 1]
    )

    with col2:

        st.markdown(
            f"""
            <div class="login-card">

                <img
                    src="{ENCORE_LOGO_URL}"
                    class="login-logo"
                >

                <div class="login-title">
                    Encore Healthcare
                </div>

                <div class="login-subtitle">
                    QC Operations Hub
                </div>

                <div class="login-accent"></div>

            </div>
            """,
            unsafe_allow_html=True
        )

        username_input = st.text_input(
            "Username"
        )

        password_input = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "🔐  Secure Login",
            type="primary",
            use_container_width=True
        ):

            user_df = conn.query(
                "SELECT id, role, password FROM users WHERE username = :u",
                params={
                    "u": username_input
                }
            )

            if (
                not user_df.empty
                and user_df.iloc[0]["password"]
                == hash_password(password_input)
            ):

                st.session_state.logged_in = True

                st.session_state.username = (
                    username_input
                )

                st.session_state.role = (
                    user_df.iloc[0]["role"]
                )

                st.session_state.login_time = (
                    datetime.now()
                )

                with conn.session as s:

                    result = s.execute(
                        text("""
                            INSERT INTO user_logs
                            (username, login_time)
                            VALUES (:u, :lt)
                            RETURNING id
                        """),
                        {
                            "u": username_input,
                            "lt": st.session_state.login_time
                        }
                    )

                    st.session_state.log_id = (
                        result.fetchone()[0]
                    )

                    s.commit()

                st.rerun()

            else:

                st.error(
                    "Invalid Username or Password"
                )

        st.markdown(
            """
            <div class="login-footer">

                Secure QC Analytics Environment
                <br>

                <span style="opacity:0.65;">
                    Encore Healthcare
                </span>

            </div>
            """,
            unsafe_allow_html=True
        )


# -------------------------------------------------------------
# 5. Main Application
# -------------------------------------------------------------

else:

    # ---------------------------------------------------------
    # Sidebar
    # ---------------------------------------------------------

    st.sidebar.image(
        ENCORE_LOGO_URL,
        use_container_width=True
    )

    st.sidebar.markdown(
        "<br>",
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        f"""
        <div style="
            background:rgba(255,255,255,0.055);
            border:1px solid rgba(255,255,255,0.08);
            border-radius:12px;
            padding:14px;
            margin-bottom:12px;
        ">

            <div style="
                color:#94A3B8;
                font-size:11px;
                font-weight:700;
                text-transform:uppercase;
                letter-spacing:1px;
            ">
                User
            </div>

            <div style="
                color:white;
                font-size:15px;
                font-weight:700;
                margin-top:5px;
            ">
                👤 {st.session_state.username}
            </div>

            <div style="
                color:#A8B7CC;
                font-size:12px;
                margin-top:4px;
            ">
                🛡️ {st.session_state.role.upper()}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.button(
        "🚪 Logout",
        on_click=do_logout,
        use_container_width=True
    )

    st.sidebar.markdown("---")


    # ---------------------------------------------------------
    # Data Fetching & Processing
    # ---------------------------------------------------------

    df = conn.query(
        "SELECT * FROM fp_analysis",
        ttl=0
    )

    st.sidebar.subheader(
        "📅 Global Date Filter"
    )

    if not df.empty:

        df["sample_receipt_date"] = pd.to_datetime(
            df["sample_receipt_date"],
            errors="coerce"
        )

        df["MonthYear"] = (
            df["sample_receipt_date"]
            .dt.to_period("M")
        )

        available_months = sorted(
            df["MonthYear"]
            .dropna()
            .unique(),
            reverse=True
        )

        available_months_str = [
            m.strftime("%B %Y")
            for m in available_months
        ]

        current_month_str = (
            pd.Timestamp.now()
            .strftime("%B %Y")
        )

        default_index = (
            available_months_str.index(
                current_month_str
            )
            if current_month_str
            in available_months_str
            else 0
        )

        if available_months_str:

            selected_month_str = st.sidebar.selectbox(
                "Select Month",
                available_months_str,
                index=default_index
            )

            selected_period = pd.Period(
                datetime.strptime(
                    selected_month_str,
                    "%B %Y"
                ),
                freq="M"
            )

            df = df[
                df["MonthYear"]
                == selected_period
            ]

        df["Queue Time (Days)"] = (
            pd.to_datetime(
                df["analysis_start_date"]
            )
            - df["sample_receipt_date"]
        ).dt.days

        df["Testing Time (Days)"] = (
            pd.to_datetime(
                df["analysis_completion_date"]
            )
            -
            pd.to_datetime(
                df["analysis_start_date"]
            )
        ).dt.days

        df["Review Time (Days)"] = (
            pd.to_datetime(
                df["review_completion_date"]
            )
            -
            pd.to_datetime(
                df["analysis_completion_date"]
            )
        ).dt.days

        df["COA Time (Days)"] = (
            pd.to_datetime(
                df["coa_completion_date"]
            )
            -
            pd.to_datetime(
                df["review_completion_date"]
            )
        ).dt.days

        df["Total TAT (Days)"] = (
            df["Queue Time (Days)"]
            +
            df["Testing Time (Days)"]
            +
            df["Review Time (Days)"]
            +
            df["COA Time (Days)"]
        )

    else:

        st.sidebar.info(
            "No data available to filter."
        )


    # ---------------------------------------------------------
    # Stylish Custom Header
    # ---------------------------------------------------------

    st.markdown(
        f"""
        <div class="top-header">

            <img src="{ENCORE_LOGO_URL}">

            <div>

                <h1>
                    Encore Healthcare QC Hub
                </h1>

                <p>
                    Finished Product Analysis &amp;
                    Workflow Tracking
                </p>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ---------------------------------------------------------
    # Tabs
    # ---------------------------------------------------------

    tab_list = [
        "📊 Analytics Dashboard",
        "📝 Log New Batch",
        "📋 Master Database"
    ]

    if st.session_state.role == "admin":

        tab_list.append(
            "🛡️ Admin Panel"
        )

    tabs = st.tabs(tab_list)


    # =========================================================
    # TAB 1: ANALYTICS
    # =========================================================

    with tabs[0]:

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )

        total_batches = len(df)

        released = (
            len(
                df[df["status"] == "Release"]
            )
            if total_batches > 0
            else 0
        )

        avg_tat = (
            df["Total TAT (Days)"].mean()
            if (
                total_batches > 0
                and "Total TAT (Days)" in df
            )
            else 0
        )

        open_delays = (
            len(
                df[
                    df["delay_reason"].notna()
                    &
                    (
                        df["delay_reason"]
                        != "Within Time"
                    )
                ]
            )
            if total_batches > 0
            else 0
        )


        # -----------------------------------------------------
        # KPI Cards
        # -----------------------------------------------------

        c1, c2, c3, c4 = st.columns(4)

        c1.markdown(
            f"""
            <div class="trendy-card"
                 style="border-left-color:#4318FF;">

                <div class="metric-label">
                    Total Batches
                </div>

                <div class="metric-value">
                    {total_batches:,}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        c2.markdown(
            f"""
            <div class="trendy-card"
                 style="border-left-color:#05CD99;">

                <div class="metric-label">
                    Released
                </div>

                <div class="metric-value"
                     style="color:#05CD99;">

                    {released}

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        c3.markdown(
            f"""
            <div class="trendy-card"
                 style="border-left-color:#F59E0B;">

                <div class="metric-label">
                    Avg TAT (Days)
                </div>

                <div class="metric-value"
                     style="color:#F59E0B;">

                    {avg_tat:.1f}

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        c4.markdown(
            f"""
            <div class="trendy-card"
                 style="border-left-color:#EF4444;">

                <div class="metric-label">
                    Open Delays
                </div>

                <div class="metric-value"
                     style="color:#EF4444;">

                    {open_delays}

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )


        # -----------------------------------------------------
        # Workflow Chart
        # -----------------------------------------------------

        if (
            total_batches > 0
            and "Queue Time (Days)" in df
            and df["Queue Time (Days)"]
            .notna()
            .any()
        ):

            st.markdown(
                "### 🚦 Micro-Stage Workflow Durations"
            )

            stage_df = df[
                [
                    "batch_no",
                    "Queue Time (Days)",
                    "Testing Time (Days)",
                    "Review Time (Days)",
                    "COA Time (Days)"
                ]
            ].dropna()

            fig_stack = px.bar(
                stage_df,
                x="batch_no",
                y=[
                    "Queue Time (Days)",
                    "Testing Time (Days)",
                    "Review Time (Days)",
                    "COA Time (Days)"
                ],
                template="plotly_white",
                color_discrete_sequence=[
                    "#1E293B",
                    "#4318FF",
                    "#05CD99",
                    "#F59E0B"
                ]
            )

            fig_stack.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    family="Plus Jakarta Sans"
                ),
                margin=dict(
                    l=20,
                    r=20,
                    t=20,
                    b=20
                ),
                hovermode="x unified"
            )

            fig_stack.update_xaxes(
                showgrid=False
            )

            fig_stack.update_yaxes(
                gridcolor="#EEF2F7",
                zeroline=False
            )

            st.plotly_chart(
                fig_stack,
                use_container_width=True
            )


    # =========================================================
    # TAB 2: INTAKE FORM
    # =========================================================

    with tabs[1]:

        st.markdown(
            "<br>### 📝 Batch Registration Form",
            unsafe_allow_html=True
        )

        with st.form(
            "full_intake_form",
            clear_on_submit=True
        ):

            f_col1, f_col2, f_col3 = st.columns(3)

            with f_col1:

                product_name = st.text_input(
                    "Product Name *"
                )

                batch_no = st.text_input(
                    "Batch Number *"
                )

                analyst_name = st.text_input(
                    "Name of Analyst"
                )

                status = st.selectbox(
                    "Status",
                    [
                        "In Progress",
                        "Release",
                        "Delayed"
                    ]
                )

            with f_col2:

                sample_receipt_date = st.date_input(
                    "Sample Receipt Date",
                    value=date.today()
                )

                analysis_start_date = st.date_input(
                    "Analysis Start Date",
                    value=None
                )

                analysis_completion_date = st.date_input(
                    "Analysis Completion Date",
                    value=None
                )

            with f_col3:

                review_completion_date = st.date_input(
                    "Review Completion Date",
                    value=None
                )

                coa_completion_date = st.date_input(
                    "COA Completion Date",
                    value=None
                )

                delay_reason = st.selectbox(
                    "Delay Reason",
                    [
                        "Within Time",
                        "Instrument Maintenance",
                        "OOS Investigation",
                        "Manpower Crunch",
                        "Other"
                    ]
                )

                actual_testing_hours = st.number_input(
                    "Actual Testing Time (Hours)",
                    min_value=0.0
                )

            st.markdown(
                "<br>",
                unsafe_allow_html=True
            )

            if st.form_submit_button(
                "💾 Save Batch to Vault",
                type="primary",
                use_container_width=True
            ):

                if not product_name or not batch_no:

                    st.error(
                        "Product Name and Batch Number are required."
                    )

                else:

                    try:

                        with conn.session as s:

                            s.execute(
                                text("""
                                    INSERT INTO fp_analysis
                                    (
                                        product_name,
                                        batch_no,
                                        analyst_name,
                                        status,
                                        delay_reason,
                                        sample_receipt_date,
                                        analysis_start_date,
                                        analysis_completion_date,
                                        review_completion_date,
                                        coa_completion_date,
                                        actual_testing_hours
                                    )
                                    VALUES
                                    (
                                        :pn,
                                        :bn,
                                        :an,
                                        :st,
                                        :dr,
                                        :srd,
                                        :asd,
                                        :acd,
                                        :rcd,
                                        :ccd,
                                        :ath
                                    )
                                """),
                                {
                                    "pn": product_name,
                                    "bn": batch_no,
                                    "an": analyst_name,
                                    "st": status,
                                    "dr": delay_reason,
                                    "srd": sample_receipt_date,
                                    "asd": analysis_start_date,
                                    "acd": analysis_completion_date,
                                    "rcd": review_completion_date,
                                    "ccd": coa_completion_date,
                                    "ath": actual_testing_hours
                                }
                            )

                            s.commit()

                        st.success(
                            f"Batch {batch_no} saved securely."
                        )

                        st.rerun()

                    except Exception:

                        st.error(
                            "Error: Batch Number already exists in the system."
                        )


    # =========================================================
    # TAB 3: LIVE GRID
    # =========================================================

    with tabs[2]:

        st.markdown(
            "<br>### 📋 Centralized Database Editor",
            unsafe_allow_html=True
        )

        if not df.empty:

            edited_df = st.data_editor(
                df.drop(
                    columns=["MonthYear"],
                    errors="ignore"
                ),
                use_container_width=True,
                hide_index=True
            )

            if st.button(
                "💾 Commit Modifications",
                type="primary"
            ):

                save_df = edited_df.drop(
                    columns=[
                        "Queue Time (Days)",
                        "Testing Time (Days)",
                        "Review Time (Days)",
                        "COA Time (Days)",
                        "Total TAT (Days)"
                    ],
                    errors="ignore"
                )

                save_df.to_sql(
                    "fp_analysis",
                    con=conn.engine,
                    if_exists="replace",
                    index=False
                )

                st.success(
                    "Database synchronized successfully!"
                )

                st.rerun()


    # =========================================================
    # TAB 4: ADMIN PANEL
    # =========================================================

    if st.session_state.role == "admin":

        with tabs[3]:

            adm_col1, adm_col2 = st.columns(
                [1, 2]
            )

            with adm_col1:

                st.markdown(
                    "<br>### 👤 User Management",
                    unsafe_allow_html=True
                )

                with st.form(
                    "create_user_form",
                    clear_on_submit=True
                ):

                    new_user = st.text_input(
                        "New Username"
                    )

                    new_pass = st.text_input(
                        "Default Password",
                        type="password"
                    )

                    new_role = st.selectbox(
                        "Role",
                        [
                            "user",
                            "admin"
                        ]
                    )

                    if st.form_submit_button(
                        "Create User",
                        type="primary"
                    ):

                        if new_user and new_pass:

                            try:

                                with conn.session as s:

                                    s.execute(
                                        text("""
                                            INSERT INTO users
                                            (
                                                username,
                                                password,
                                                role
                                            )
                                            VALUES
                                            (
                                                :u,
                                                :p,
                                                :r
                                            )
                                        """),
                                        {
                                            "u": new_user,
                                            "p": hash_password(
                                                new_pass
                                            ),
                                            "r": new_role
                                        }
                                    )

                                    s.commit()

                                st.success(
                                    f"User '{new_user}' created."
                                )

                            except Exception:

                                st.error(
                                    "Username already exists."
                                )

                        else:

                            st.error(
                                "Fill all fields."
                            )


                st.markdown(
                    "#### Delete User"
                )

                users_df = conn.query(
                    """
                    SELECT id, username, role
                    FROM users
                    WHERE username != 'admin'
                    """,
                    ttl=0
                )

                if not users_df.empty:

                    del_user = st.selectbox(
                        "Select user to delete",
                        users_df["username"].tolist()
                    )

                    if st.button(
                        "Revoke Access"
                    ):

                        with conn.session as s:

                            s.execute(
                                text("""
                                    DELETE FROM users
                                    WHERE username = :u
                                """),
                                {
                                    "u": del_user
                                }
                            )

                            s.commit()

                        st.success(
                            f"User '{del_user}' removed."
                        )

                        st.rerun()


            with adm_col2:

                st.markdown(
                    "<br>### 🕒 Access & Audit Logs",
                    unsafe_allow_html=True
                )

                logs_df = conn.query(
                    """
                    SELECT
                        username,
                        login_time,
                        logout_time,
                        usage_minutes
                    FROM user_logs
                    ORDER BY login_time DESC
                    """,
                    ttl=0
                )

                st.dataframe(
                    logs_df,
                    use_container_width=True,
                    hide_index=True
                )

