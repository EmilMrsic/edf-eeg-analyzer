---
title: Pinguis Vir EDF Reader
emoji: 🧨
colorFrom: gray
colorTo: indigo
sdk: streamlit
sdk_version: "1.46.0"
app_file: streamlit_app.py
pinned: false
---

# edf-eeg-analyzer
Utility for analyzing EEG EDF files

## Usage

Run the CLI to compute absolute power bands:

```bash
python analyze_edf.py <input.edf> [-o OUTPUT_DIR]
```

The optional `-o` flag sets the directory for the generated
`absolute_power.csv` and `absolute_power.xlsx` files. By default the files are
written to the current working directory.
# EDF → Absolute‑Power Utility  
*(technical & managerial specification)*  

---

## 1.  Business Goal

> **Deliver a tiny, self‑hosted web tool that lets any clinician or researcher drop an `.edf` EEG recording (256 Hz) into a browser window and immediately download a CSV/XLSX table of absolute power values – per channel, per band – along with an on‑screen preview.**

There are no cloud APIs, licences, or proprietary binaries: everything runs in pure Python (MNE‑Python, NumPy, SciPy, Pandas, Streamlit).

---

## 2.  Functional Requirements (user‑visible)

| # | Requirement | Success Criteria |
|---|-------------|------------------|
| **FR‑1** | **File‑upload** accepts `.edf` via drag‑and‑drop or file‑picker. | Upload widget shows file name; no refresh/reload. |
| **FR‑2** | Compute absolute power for every EEG channel in five canonical bands: <br>• Delta 0.5–3 Hz • Theta 4–7 Hz • Alpha 8–12 Hz • Beta 15–20 Hz • Hi‑Beta 20–30 Hz | Table contains *exactly* these five columns in this order, with ≥ 1 numeric row. |
| **FR‑3** | Display the results interactively (sortable, scrollable). | `st.dataframe` renders after processing; values match exported files. |
| **FR‑4** | Provide **two** download buttons – CSV and Excel. | Clicking yields `absolute_power.csv` and `absolute_power.xlsx` with identical data. |
| **FR‑5** | Single‑command launch: `streamlit run streamlit_app.py`. | Fresh clone + `pip install -r requirements.txt` + run command works on macOS/Linux/Windows. |

---

## 3.  Non‑Functional Requirements

- **Runtime:** < 10 s for a typical 5‑minute, 19‑channel EDF on a laptop i7‑8750H.  
- **Footprint:** Codebase ≤ 300 LoC (excluding comments/tests).  
- **Reproducibility:** All dependencies pinned in `requirements.txt`.  
- **Portability:** No hard‑coded paths; everything writes to process CWD or OS temp dir.  
- **Coding Standards:** PEP‑8, flake8 < 6 warnings.  
- **Licence:** MIT.

---

## 4.  Algorithm & Equations *(“how it knows what to do”)*

### 4.1  Preliminaries  

- **Sampling rate (`f_s`):** 256 Hz (resample iff EDF differs).  
- **Epoch length (`T_e`):** 2 s → `N = 512` samples.  
- **Window:** Hann  
  \( w[n] = 0.5 \left(1 - \cos\frac{2\pi n}{N-1}\right) \), \( n = 0\ldots N-1 \)  
- **Overlap:** 50 % → `n_overlap = 256` samples.  
- **FFT length:** `N_fft = N` (no zero‑padding).  

### 4.2  Welch’s Method  

For every channel \(c\):

1. Split signal \(x_c[n]\) into \(E\) overlapping epochs \(x_{c,e}[n]\).  
2. **Per‑epoch periodogram**  
   \[
     P_{c,e}[k] \;=\;
       \frac{1}{f_s \, N \, U}
       \Bigl|\,
         \sum_{n=0}^{N-1} w[n] \, x_{c,e}[n] \,
         e^{-j 2\pi kn / N}
       \Bigr|^2,
       \quad k = 0\ldots N/2
   \]  
   where \( U = \tfrac{1}{N} \sum_{n=0}^{N-1} w[n]^2 \) (energy normalisation).
3. **Average across epochs**  
   \[
     \operatorname{PSD}_c[k] \;=\; \frac{1}{E} \sum_{e=1}^{E} P_{c,e}[k]
   \]

### 4.3  Absolute‑Power Integration  

Let \(f_k = k \, \frac{f_s}{N}\) (frequency bin centers).  
For each band \(b = (f_{\text{low}},\,f_{\text{high}})\):

\[
  P_{c,b} \;=\;
    \int_{f_{\text{low}}}^{f_{\text{high}}}
      \operatorname{PSD}_c(f)\,df
  \;\approx\;
    \sum_{k:\;f_{\text{low}}\le f_k \le f_{\text{high}}}
      \operatorname{PSD}_c[k] \,\Delta f
\]
with \( \Delta f = \tfrac{f_s}{N} = 0.5 \text{ Hz} \).  
Implementation uses `numpy.trapz` for slight additional accuracy.

Result units = **µV²** (because PSD unit × Hz).

### 4.4  Optional Categorical Mapping  

User‑defined thresholds (e.g. percentile bands) produce:

| Code | Meaning |
|------|---------|
| VHI  | Very High |
| HI   | High |
| OK   | Normal |
| LO   | Low |
| VLO  | Very Low |

Mapping is pure post‑processing:  
`label = f(power, thresholds_json)`.

---

## 5.  Work‑Breakdown Structure & Owners

| WBS | Task | Owner | Output Artifact |
|-----|------|-------|-----------------|
| 1.0 | Repository skeleton | *you* | README.md, .gitignore |
| 2.0 | Virtualenv + `requirements.txt` | Codex | lockfile |
| 3.0 | `analyze_edf.py` (section 4 logic) | Codex | CLI script, unit test |
| 4.0 | `streamlit_app.py` (UI) | Codex | Web front‑end |
| 5.0 | Documentation pass | Codex | In‑code docstrings, updated README |
| 6.0 | Deployment guide | Codex | DEPLOY.md |
| 7.0 | (Stretch) categorical labeller + tests | Codex | `band_labels.py`, tests |

---

## 6.  Acceptance Checklist

- [ ] CLI script outputs `absolute_power.csv` **and** `absolute_power.xlsx` with 5 columns and one row per EEG channel.  
- [ ] Values reproduce manual MNE‑Python calculation within ±0.1 %.  
- [ ] Streamlit workflow succeeds for `sample.edf` (to be committed under `tests/data/`).  
- [ ] `pip install -r requirements.txt` works on clean Ubuntu GitHub Action.  
- [ ] `flake8` < 6 warnings.  

---

## 7.  Timeline (calendar days)

| Day | Deliverable |
|-----|-------------|
| 0   | Repo + this spec pushed |
| 0‑1 | 2.0 & 3.0 completed, unit tests green |
| 1‑2 | 4.0 done – local Streamlit works |
| 2   | 5.0 & 6.0 committed |
| 3   | Stretch goals / polish |

---

## 8.  References

- Welch, P. (1967). *The use of fast Fourier transform for the estimation of power spectra*. IEEE Transactions on Audio and Electroacoustics, 15(2), 70‑73.  
- MNE‑Python API > `mne.time_frequency.psd_welch`.  
- SciPy 1.12 > `scipy.signal.get_window`.

---
## Development

Install dependencies, run the unit tests, and check linting:

```bash
pip install -r requirements.txt
pip install pytest flake8
pytest
flake8 .
```

`flake8` is configured via `.flake8` and should report fewer than six warnings.


> **Hand‑off to Codex:**  
> 1. Create the repo and commit `PROJECT_SPEC.md`.  
> 2. Follow WBS in section 5.  
> 3. Tick items in section 6 as they pass.  
> 4. Ask for clarification only when something blocks forward progress.
