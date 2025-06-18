import base64
import io
import os
from pathlib import Path

import pandas as pd
import streamlit as st

import streamlit_app


def _decode_sample_edf(tmp_path: Path) -> Path:
    b64_path = Path(__file__).parent / "data" / "sample.edf.b64"
    edf_bytes = base64.b64decode(b64_path.read_text())
    edf_path = tmp_path / "sample.edf"
    edf_path.write_bytes(edf_bytes)
    return edf_path


def test_main_with_upload(tmp_path, monkeypatch):
    edf_path = _decode_sample_edf(tmp_path)
    monkeypatch.setenv("TEST_EDF_PATH", str(edf_path))

    class FakeUpload:
        def __init__(self, path: str):
            self._bytes = Path(path).read_bytes()

        def getbuffer(self):
            return self._bytes

    def fake_file_uploader(*args, **kwargs):
        return FakeUpload(os.environ["TEST_EDF_PATH"])

    captured = {}

    monkeypatch.setattr(st, "file_uploader", fake_file_uploader)
    monkeypatch.setattr(st, "download_button", lambda *a, **k: None)
    monkeypatch.setattr(st, "title", lambda *a, **k: None)

    def fake_dataframe(df: pd.DataFrame):
        captured["df"] = df

    monkeypatch.setattr(st, "dataframe", fake_dataframe)

    streamlit_app.main()

    assert "df" in captured
    assert isinstance(captured["df"], pd.DataFrame)
    assert not captured["df"].empty


def test_main_no_upload(monkeypatch):
    monkeypatch.setattr(st, "file_uploader", lambda *a, **k: None)
    monkeypatch.setattr(st, "download_button", lambda *a, **k: None)
    monkeypatch.setattr(st, "title", lambda *a, **k: None)

    called = False

    def fake_dataframe(_df):
        nonlocal called
        called = True

    monkeypatch.setattr(st, "dataframe", fake_dataframe)

    streamlit_app.main()

    assert not called
