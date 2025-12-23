import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
import json

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(page_title="Advanced CSV Intelligence App", layout="wide")

# ==================================================
# ACCESS CONTROL
# ==================================================
PASSWORD = "admin123"

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    with st.form("login"):
        st.title("🔐 Secure Access")
        pwd = st.text_input("Enter password", type="password")
        submit = st.form_submit_button("Login")

        if submit and pwd == PASSWORD:
            st.session_state.auth = True
            st.rerun()
        elif submit:
            st.error("Invalid password")
    st.stop()

# ==================================================
# CUSTOM CSS
# ==================================================
st.markdown("""
<style>
html, body, [class*="css"] { font-size:18px; }
h1 { font-size:42px !important; font-weight:800; }
thead th { font-size:20px !important; }
tbody td { font-size:18px !important; }
</style>
""", unsafe_allow_html=True)

# ==================================================
# VIEW COUNTER
# ==================================================
VIEW_FILE = "views.txt"
Path(VIEW_FILE).write_text(Path(VIEW_FILE).read_text() if Path(VIEW_FILE).exists() else "0")

if "viewed" not in st.session_state:
    Path(VIEW_FILE).write_text(str(int(Path(VIEW_FILE).read_text()) + 1))
    st.session_state.viewed = True

total_views = Path(VIEW_FILE).read_text()

# ==================================================
# BEHAVIOR ANALYTICS
# ==================================================
ANALYTICS_FILE = "analytics.json"

def load_analytics():
    if not Path(ANALYTICS_FILE).exists():
        Path(ANALYTICS_FILE).write_text("{}")
        return {}

    content = Path(ANALYTICS_FILE).read_text().strip()

    if not content:
        Path(ANALYTICS_FILE).write_text("{}")
        return {}

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        Path(ANALYTICS_FILE).write_text("{}")
        return {}

def log_event(event):
    data = load_analytics()
    data[event] = data.get(event, 0) + 1
    Path(ANALYTICS_FILE).write_text(json.dumps(data, indent=2))

# ==================================================
# MULTI-CSV MANAGER
# ==================================================
csv_files = list(Path(".").glob("*.csv"))
csv_names = [f.name for f in csv_files]

selected_csv = st.sidebar.selectbox("📁 Select Dataset", csv_names)
log_event("dataset_selected")

@st.cache_data
def load_csv(file):
    return pd.read_csv(file)

df = load_csv(selected_csv)

# ==================================================
# INTELLIGENT CSV UNDERSTANDING
# ==================================================
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
categorical_cols = df.select_dtypes(exclude=np.number).columns.tolist()

st.title("📊 Advanced CSV Intelligence App")
st.caption(f"👀 Total Views: {total_views}")
st.caption(f"🧠 Dataset: {selected_csv}")

# ==================================================
# COLUMN CONTROLS
# ==================================================
with st.sidebar:
    st.subheader("🔧 Column Controls")
    visible_cols = st.multiselect(
        "Visible Columns",
        df.columns.tolist(),
        default=df.columns.tolist()
    )

df = df[visible_cols]

# ==================================================
# CONDITIONAL FORMATTING
# ==================================================
def highlight_max(s):
    return ['background-color: #ffeaa7' if v == s.max() else '' for v in s]

styled_df = df.style
if numeric_cols:
    styled_df = styled_df.apply(highlight_max, subset=numeric_cols)

st.dataframe(styled_df, use_container_width=True, height=500)

# ==================================================
# AUTO DASHBOARD
# ==================================================
st.subheader("📈 Auto Insights Dashboard")

if numeric_cols:
    col = st.selectbox("Select numeric column", numeric_cols)
    fig, ax = plt.subplots()
    ax.hist(df[col].dropna())
    st.pyplot(fig)
    log_event("chart_viewed")

# ==================================================
# WHAT-IF ANALYSIS
# ==================================================
st.subheader("🧪 What-If Analysis")

if numeric_cols:
    col = st.selectbox("What-If Column", numeric_cols, key="whatif")
    factor = st.slider("Multiply values by", 0.5, 2.0, 1.0)
    df[col] = df[col] * factor
    st.dataframe(df[[col]].head())

# ==================================================
# DATA QUALITY
# ==================================================
st.subheader("🧠 Data Quality")
st.write("Missing values:")
st.write(df.isnull().sum())

st.write("Duplicate rows:", df.duplicated().sum())

# ==================================================
# AI INSIGHTS (STUB – PLUG READY)
# ==================================================
st.subheader("🤖 AI Insights (Coming Soon)")
st.info("Ask questions like: 'Explain trends' or 'Find anomalies'")
st.text_input("Ask the dataset")

# ==================================================
# ADMIN PANEL
# ==================================================
with st.expander("🛠 Admin Analytics"):
    analytics = json.loads(Path(ANALYTICS_FILE).read_text())
    st.json(analytics)
