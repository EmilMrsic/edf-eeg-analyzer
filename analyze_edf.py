import argparse
import os
from pathlib import Path

import mne
import numpy as np
import pandas as pd
from scipy.signal import welch

# Define EEG bands
BANDS = {
    'Delta': (0.5, 3),
    'Theta': (4, 7),
    'Alpha': (8, 12),
    'Beta': (15, 20),
    'Hi-Beta': (20, 30),
}

def compute_absolute_power(edf_path, output_dir="."):
    """Return per-channel absolute power for an EDF recording.

    Parameters
    ----------
    edf_path : str or pathlib.Path
        Path to the EDF file to analyze.
    output_dir : str or pathlib.Path, optional
        Directory where ``absolute_power.csv`` and ``absolute_power.xlsx``
        will be written. Defaults to the current working directory.

    Returns
    -------
    pandas.DataFrame
        Table of absolute power values for each channel.

    Notes
    -----
    Writes ``absolute_power.csv`` and ``absolute_power.xlsx`` to
    ``output_dir``.
    """
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    raw = mne.io.read_raw_edf(edf_path, preload=True)

    # Resample to 256 Hz if necessary
    if abs(raw.info['sfreq'] - 256) > 1e-6:
        raw.resample(256)
    sfreq = raw.info['sfreq']

    data = raw.get_data()
    ch_names = raw.ch_names
    print(f"Loaded EDF with {len(ch_names)} channels at {sfreq} Hz")
    print("Channels:", ch_names)

    results = []

    for i, signal in enumerate(data):
        f, psd = welch(
            signal,
            fs=sfreq,
            window='hann',
            nperseg=512,
            noverlap=256,
            nfft=512,
            scaling='density'
        )

        band_powers = {}
        for band, (low, high) in BANDS.items():
            idx = np.logical_and(f >= low, f <= high)
            power = np.trapz(psd[idx], f[idx])  # µV²
            band_powers[band] = power

        band_powers['Channel'] = ch_names[i]
        print(f"Processed channel: {ch_names[i]}, Band powers: {band_powers}")
        results.append(band_powers)

    df = pd.DataFrame(results)
    df = df[['Channel'] + list(BANDS.keys())]

    csv_path = out_dir / "absolute_power.csv"
    xlsx_path = out_dir / "absolute_power.xlsx"
    df.to_csv(csv_path, index=False)
    df.to_excel(xlsx_path, index=False)
    return df


def main(argv=None):
    """Parse CLI arguments and run :func:`compute_absolute_power`.

    Parameters
    ----------
    argv : list[str] | None, optional
        Arguments to parse. Defaults to ``sys.argv[1:]``.

    Returns
    -------
    pandas.DataFrame
        The DataFrame produced by :func:`compute_absolute_power`.

    The CSV and XLSX files are written to the directory specified by
    ``-o`` (default: current directory).
    """

    parser = argparse.ArgumentParser(
        description="Compute absolute power bands from an EDF file"
    )
    parser.add_argument(
        "edf_path",
        help="Path to the input EDF file"
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default=".",
        help="Directory to write the CSV/XLSX results"
    )
    args = parser.parse_args(argv)

    output_dir = os.path.abspath(args.output_dir)
    df = compute_absolute_power(args.edf_path, output_dir=output_dir)
    return df


if __name__ == "__main__":
    main()