import io
import os
import tempfile
import streamlit as st
from analyze_edf import compute_absolute_power

# Configuration
# ``DEFAULT_EDF_PATH`` can point to an EDF file on disk that will be used
# when no file is uploaded via the UI. This is primarily useful for
# demonstrations or local testing of the app.
DEFAULT_EDF_PATH = os.environ.get("DEFAULT_EDF_PATH")

def main():
    st.title("EDF EEG Absolute Power Analyzer")

    uploaded_file = st.file_uploader("Upload EDF file", type="edf")

    edf_path = None
    notice = None
    if uploaded_file is not None:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".edf") as tmp:
                tmp.write(uploaded_file.getbuffer())
                edf_path = tmp.name
        except Exception as exc:  # pragma: no cover - UI feedback only
            notice = f"Error reading uploaded file: {exc}"  # noqa: E501

    if edf_path is None and DEFAULT_EDF_PATH:
        edf_path = DEFAULT_EDF_PATH
        default_msg = f"Using default EDF at '{DEFAULT_EDF_PATH}'."
        notice = f"{notice}. {default_msg}" if notice else default_msg

    if notice:
        st.info(notice)

    if edf_path:
        df = compute_absolute_power(edf_path)
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download CSV",
            data=csv,
            file_name="absolute_power.csv",
            mime="text/csv",
        )

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
