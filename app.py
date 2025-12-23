import streamlit as st
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="CSV Viewer",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS (BIGGER, ATTENTION-GRABBING FONTS)
# --------------------------------------------------
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-size: 18px;
    }

    h1 {
        font-size: 42px !important;
        font-weight: 800 !important;
    }

    thead th {
        font-size: 20px !important;
        font-weight: 700 !important;
    }

    tbody td {
        font-size: 18px !important;
        padding: 10px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# SIMPLE IN-APP VIEW COUNTER
# --------------------------------------------------
VIEW_FILE = "views.txt"

def get_views():
    if not Path(VIEW_FILE).exists():
        Path(VIEW_FILE).write_text("0")
    return int(Path(VIEW_FILE).read_text())

def increment_views():
    views = get_views() + 1
    Path(VIEW_FILE).write_text(str(views))
    return views

if "viewed" not in st.session_state:
    st.session_state.viewed = True
    total_views = increment_views()
else:
    total_views = get_views()

# --------------------------------------------------
# APP UI
# --------------------------------------------------
st.title("📊 CSV File Viewer")
st.caption(f"👀 Total App Views: {total_views}")

st.write("This table displays the CSV file located in the same directory as the app.")

# --------------------------------------------------
# LOAD CSV (SAME DIRECTORY)
# --------------------------------------------------
CSV_FILE = "sample.csv"

if Path(CSV_FILE).exists():
    try:
        df = pd.read_csv(CSV_FILE)

        st.success("CSV file loaded successfully!")

        st.dataframe(
            df,
            use_container_width=True,
            height=600
        )

        with st.expander("📌 CSV Details"):
            st.write("Rows:", df.shape[0])
            st.write("Columns:", df.shape[1])
            st.write("Column Names:", list(df.columns))

    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
else:
    st.error(f"CSV file `{CSV_FILE}` not found in the app directory.")
