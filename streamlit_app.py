import io
import os
import tempfile
import streamlit as st
from analyze_edf import compute_absolute_power

def main():
    st.title("EDF EEG Absolute Power Analyzer")

    uploaded_file = st.file_uploader("Upload EDF file", type="edf")
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".edf") as tmp:
            tmp.write(uploaded_file.getbuffer())
            tmp_path = tmp.name

        try:
            df = compute_absolute_power(tmp_path)
        finally:
            os.remove(tmp_path)

        df_display = df.copy()
        for col in df_display.columns:
            if df_display[col].dtype != "object":
                df_display[col] = df_display[col].apply(lambda v: f"{v:.3e}")
        st.dataframe(df_display)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", data=csv, file_name="absolute_power.csv", mime="text/csv")

        excel_io = io.BytesIO()
        df.to_excel(excel_io, index=False)
        st.download_button(
            "Download Excel",
            data=excel_io.getvalue(),
            file_name="absolute_power.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

if __name__ == "__main__":
    main()
