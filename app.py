import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="CSV Viewer", layout="wide")

# 🔥 Custom CSS for bigger fonts
st.markdown(
    """
    <style>
    /* Main app font */
    html, body, [class*="css"] {
        font-size: 18px;
    }

    /* Dataframe header */
    thead th {
        font-size: 20px !important;
        font-weight: 700 !important;
    }

    /* Dataframe cells */
    tbody td {
        font-size: 18px !important;
        padding: 10px !important;
    }

    /* Title */
    h1 {
        font-size: 42px !important;
        font-weight: 800 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 CSV File Viewer")

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
