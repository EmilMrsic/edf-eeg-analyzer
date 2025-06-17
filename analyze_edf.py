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

def compute_absolute_power(edf_path):
    raw = mne.io.read_raw_edf(edf_path, preload=True)
    
    # Resample to 256 Hz if necessary
    if raw.info['sfreq'] != 256:
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
    
    df.to_csv("absolute_power.csv", index=False)
    df.to_excel("absolute_power.xlsx", index=False)
    return df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Compute absolute EEG band power from an EDF file",
    )
    parser.add_argument("edf_path", help="Path to EDF file")
    args = parser.parse_args()

    compute_absolute_power(args.edf_path)
