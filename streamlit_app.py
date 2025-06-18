    uploaded_file = st.file_uploader("Upload EDF file", type="edf")

    edf_path = None
    notice = None
    if uploaded_file is not None:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".edf") as tmp:
                tmp.write(uploaded_file.getbuffer())
                edf_path = tmp.name
        except Exception as exc:
            notice = f"Error reading uploaded file: {exc}"

    if edf_path is None and DEFAULT_EDF_PATH:
        edf_path = DEFAULT_EDF_PATH
        default_msg = f"Using default EDF at '{DEFAULT_EDF_PATH}'."
        notice = f"{notice}. {default_msg}" if notice else default_msg

    if notice:
        st.info(notice)

    if edf_path:
        try:
            df = compute_absolute_power(edf_path)
        finally:
            # Only remove if it was a temp file
            if uploaded_file is not None:
                os.remove(edf_path)

        df_display = df.copy()
        for col in df_display.columns:
            if df_display[col].dtype != "object":
                df_display[col] = df_display[col].apply(lambda v: f"{v:.3e}")
        st.dataframe(df_display)

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