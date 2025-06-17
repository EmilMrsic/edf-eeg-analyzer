import base64
from pathlib import Path

import pandas as pd

from analyze_edf import compute_absolute_power


def _decode_sample_edf(tmp_path: Path) -> Path:
    b64_path = Path(__file__).parent / "data" / "sample.edf.b64"
    edf_bytes = base64.b64decode(b64_path.read_text())
    edf_path = tmp_path / "sample.edf"
    edf_path.write_bytes(edf_bytes)
    return edf_path


def test_compute_absolute_power(tmp_path):
    edf_path = _decode_sample_edf(tmp_path)
    df = compute_absolute_power(edf_path)
    assert not df.empty
    expected_cols = ["Channel", "Delta", "Theta", "Alpha", "Beta", "Hi-Beta"]
    assert list(df.columns) == expected_cols
