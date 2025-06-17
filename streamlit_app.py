import tempfile
from io import BytesIO

import pandas as pd
import streamlit as st

from analyze_edf import compute_absolute_power

st.title("EDF EEG Absolute Power Analyzer")

uploaded_file = st.file_uploader("Upload EDF file", type=["edf"])

if uploaded_file is not None:
    with st.spinner("Analyzing..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".edf") as tmp:
            tmp.write(uploaded_file.getbuffer())
            tmp_path = tmp.name
        df = compute_absolute_power(tmp_path)

    st.subheader("Absolute Power per Channel")
    st.dataframe(df)

    csv_data = df.to_csv(index=False).encode("utf-8")
    xls_buffer = BytesIO()
    df.to_excel(xls_buffer, index=False)
    xls_data = xls_buffer.getvalue()

    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="absolute_power.csv",
        mime="text/csv",
    )
    st.download_button(
        label="Download Excel",
        data=xls_data,
        file_name="absolute_power.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
    )

