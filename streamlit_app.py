import io
import os
import tempfile
import streamlit as st
from analyze_edf import compute_absolute_power

def main():
    st.set_page_config(
        page_title="Pinguis Vir EDF Reader",
        page_icon="🧨",
        layout="centered",
    )
    st.title("🧨 Pinguis Vir EDF Reader")

    uploaded_file = st.file_uploader("Upload an EDF file", type="edf")

    edf_path = None
    notice = None

    if uploaded_file is not None:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".edf") as tmp:
                tmp.write(uploaded_file.getbuffer())
                edf_path = tmp.name
        except Exception as exc:
            notice = f"❌ Error reading uploaded file: {exc}"

    if notice:
        st.info(notice)

    if edf_path is not None:
        try:
            df = compute_absolute_power(edf_path)
        finally:
            # Clean up uploaded temp file
            if uploaded_file is not None:
                os.remove(edf_path)

        # Format for display
        formatted_df = df.copy()
        for col in df.columns:
            if col != "Channel":
                formatted_df[col] = df[col].apply(lambda x: f"{x:.2e}")
        st.dataframe(formatted_df)

        # CSV + Excel export
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
