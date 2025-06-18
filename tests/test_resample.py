import numpy as np
import mne

from analyze_edf import compute_absolute_power


def test_resample_non_integer(tmp_path, capsys):
    sfreq = 255.5
    data = np.zeros((1, int(sfreq)))
    info = mne.create_info(ch_names=["Fz"], sfreq=sfreq, ch_types="eeg")
    raw = mne.io.RawArray(data, info)
    edf_path = tmp_path / "non_int.edf"
    mne.export.export_raw(raw, edf_path, fmt="edf")

    compute_absolute_power(str(edf_path))
    captured = capsys.readouterr().out
    assert "256.0 Hz" in captured
