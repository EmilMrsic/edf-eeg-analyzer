import numpy as np
import mne

from analyze_edf import compute_absolute_power, BANDS


def test_compute_absolute_power_columns(tmp_path):
    sfreq = 256
    data = np.zeros((1, sfreq))
    info = mne.create_info(ch_names=["Fz"], sfreq=sfreq, ch_types="eeg")
    raw = mne.io.RawArray(data, info)
    edf_path = tmp_path / "dummy.edf"
    mne.export.export_raw(raw, edf_path, fmt="edf")

    df = compute_absolute_power(str(edf_path), output_dir=tmp_path)
    assert list(df.columns) == ["Channel"] + list(BANDS.keys())
    csv_path = tmp_path / "absolute_power.csv"
    xlsx_path = tmp_path / "absolute_power.xlsx"
    assert csv_path.exists()
    assert xlsx_path.exists()
    csv_path.unlink()
    xlsx_path.unlink()
