"""
Day 7 — Clean/filter the PPG signal and segment it into individual heartbeat cycles.

Steps:
  1. Reconstruct each recording's raw waveform (undoing the interleaved row order).
  2. Drop recordings shorter than a minimum duration (see Day 6 EDA finding).
  3. Bandpass-filter each remaining recording to remove baseline wander and high-frequency noise.
  4. Normalize (z-score) the filtered signal.
  5. Detect individual heartbeats (peaks) and cut the signal into one segment per heartbeat,
     resampled to a fixed length so every segment is comparable regardless of heart rate.

Run with:  .venv/bin/python ml/notebooks/day7_preprocessing.py
Outputs:   ml/data/processed/segments.csv (not committed to git — raw/processed data is
           gitignored; this script is what's reproducible and committed instead)
           docs/figures/filtering_example.png
           docs/figures/segmented_heartbeats.png
"""
import numpy as np
import pandas as pd
from scipy.signal import butter, sosfiltfilt, find_peaks
import matplotlib.pyplot as plt

DATA_PATH = "ml/data/raw/kaggle_clean/clean-dataset.csv"
FS = 2175.0  # sampling rate in Hz, per the dataset's documentation
MIN_DURATION_SEC = 4.0
MIN_SAMPLES = int(MIN_DURATION_SEC * FS)
SEGMENT_LENGTH = 100  # every heartbeat cycle gets resampled to this many points

FIG_DIR = "docs/figures"
OUT_DIR = "ml/data/processed"


def bandpass_filter(signal, fs, low=0.5, high=8.0, order=4):
    """Keep only the 0.5-8 Hz band, which comfortably covers real heart rates (30-480 bpm)
    while removing slow baseline drift (below 0.5 Hz) and high-frequency sensor noise (above 8 Hz).

    Uses second-order-sections (sos) form rather than the more common (b, a) transfer-function
    form. This matters here: at a high sample rate (2175 Hz) with such a narrow passband, the
    (b, a) coefficients become numerically unstable and filtfilt silently explodes to nonsense
    values (found this the hard way - the first version of this filter produced values around
    1e110 without raising an error). sos form is the numerically robust way to apply the same
    filter and is the standard recommendation for exactly this situation."""
    nyq = fs / 2
    sos = butter(order, [low / nyq, high / nyq], btype="band", output="sos")
    return sosfiltfilt(sos, signal)


def zscore(signal):
    return (signal - signal.mean()) / (signal.std() + 1e-8)


def reconstruct_recordings(df):
    recs = {}
    for (pid, idx), group in df.groupby(["Patient_Id", "index"]):
        recs[(pid, idx)] = {
            "signal": group["PPG_Signal"].to_numpy(dtype=float),
            "glucose": group["Glucose_level"].iloc[0],
        }
    return recs


def segment_heartbeats(filtered, fs):
    """Find peaks (one per heartbeat) and cut the signal around each into a fixed-length segment.

    Note: PPG peak detection is not perfect. Early testing here found that a permissive distance
    threshold occasionally lets the "dicrotic notch" (a smaller secondary bump after the main
    heartbeat peak, from the reflected pulse wave) get detected as its own peak, producing
    implausible back-to-back short intervals. Capping at a max plausible resting-ish heart rate
    of 150 bpm (rather than a very permissive 200+ bpm) filters most of these out. This is a
    tunable heuristic, not a perfect solution - a proper systolic-peak-specific detector would be
    the next improvement if we needed higher precision."""
    min_distance = int(fs * 60 / 150)  # assume max plausible heart rate ~150 bpm
    peaks, _ = find_peaks(filtered, distance=min_distance, prominence=0.5)
    segments = []
    cycle_lengths = []
    for i in range(len(peaks) - 1):
        start, end = peaks[i], peaks[i + 1]
        cycle = filtered[start:end]
        if len(cycle) < 5:
            continue
        # resample every cycle to the same fixed number of points regardless of heart rate
        x_old = np.linspace(0, 1, len(cycle))
        x_new = np.linspace(0, 1, SEGMENT_LENGTH)
        resampled = np.interp(x_new, x_old, cycle)
        segments.append(resampled)
        cycle_lengths.append(end - start)  # samples between this beat's peak and the next
    return segments, cycle_lengths, peaks


def main():
    df = pd.read_csv(DATA_PATH)
    recordings = reconstruct_recordings(df)
    print(f"Reconstructed {len(recordings)} recordings.")

    kept, dropped = 0, 0
    all_segments = []
    example_raw = example_filtered = example_peaks = None

    for (pid, idx), rec in recordings.items():
        raw = rec["signal"]
        if len(raw) < MIN_SAMPLES:
            dropped += 1
            continue
        kept += 1

        filtered = bandpass_filter(raw, FS)
        normalized = zscore(filtered)
        segments, cycle_lengths, peaks = segment_heartbeats(normalized, FS)

        if example_raw is None and len(segments) >= 5:
            example_raw, example_filtered, example_peaks = raw, normalized, peaks

        for seg_i, (seg, cyc_len) in enumerate(zip(segments, cycle_lengths)):
            all_segments.append({
                "patient_id": pid,
                "recording_index": idx,
                "heartbeat_index": seg_i,
                "glucose": rec["glucose"],
                "cycle_length_samples": cyc_len,
                "heart_rate_bpm": 60.0 * FS / cyc_len,
                **{f"p{i}": v for i, v in enumerate(seg)},
            })

    print(f"Kept {kept} recordings (>= {MIN_DURATION_SEC}s), dropped {dropped} (too short).")
    seg_df = pd.DataFrame(all_segments)
    print(f"Extracted {len(seg_df)} individual heartbeat segments total, "
          f"~{len(seg_df) / max(kept, 1):.1f} per recording on average.")

    import os
    os.makedirs(OUT_DIR, exist_ok=True)
    seg_df.to_csv(f"{OUT_DIR}/segments.csv", index=False)
    print(f"Saved {OUT_DIR}/segments.csv")

    # --- Figure 1: raw vs. filtered signal for one example recording ---
    fig, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    n_show = int(FS * 5)  # first 5 seconds
    axes[0].plot(example_raw[:n_show], color="#888888", linewidth=0.8)
    axes[0].set_title("Raw PPG signal (first 5 seconds)")
    axes[0].set_ylabel("Raw amplitude")
    axes[1].plot(example_filtered[:n_show], color="#4C72B0", linewidth=0.8)
    peaks_in_range = example_peaks[example_peaks < n_show]
    axes[1].plot(peaks_in_range, example_filtered[peaks_in_range], "o", color="#C44E52", markersize=4)
    axes[1].set_title("Filtered + normalized signal, with detected heartbeat peaks")
    axes[1].set_ylabel("Normalized amplitude")
    axes[1].set_xlabel("Sample number")
    fig.tight_layout()
    fig.savefig(f"{FIG_DIR}/filtering_example.png", dpi=150)
    plt.close(fig)
    print("Saved filtering_example.png")

    # --- Figure 2: several segmented heartbeat cycles overlaid ---
    fig, ax = plt.subplots(figsize=(7, 4.5))
    sample_segments = seg_df.filter(like="p").iloc[:30].to_numpy()
    for row in sample_segments:
        ax.plot(row, color="#4C72B0", alpha=0.3, linewidth=1)
    ax.set_title("30 individual heartbeat segments, resampled to a fixed length")
    ax.set_xlabel("Resampled position within one heartbeat cycle")
    ax.set_ylabel("Normalized amplitude")
    fig.tight_layout()
    fig.savefig(f"{FIG_DIR}/segmented_heartbeats.png", dpi=150)
    plt.close(fig)
    print("Saved segmented_heartbeats.png")


if __name__ == "__main__":
    main()
