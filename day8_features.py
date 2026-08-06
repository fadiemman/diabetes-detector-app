"""
Day 8 — Turn each heartbeat segment into meaningful numeric features.

Reads ml/data/processed/segments.csv (474 individual, resampled heartbeat cycles from Day 7)
and computes, for each heartbeat:
  - heart_rate_bpm            (already computed in Day 7, carried through)
  - systolic_peak_amplitude   how tall the main pulse is
  - diastolic_peak_amplitude  how tall the secondary "dicrotic notch" bump is
  - reflection_index          diastolic / systolic amplitude ratio (a real clinical PPG feature -
                               related to arterial stiffness, and one of the few PPG-derived
                               numbers with a documented, if weak, statistical link to glucose)
  - pulse_amplitude            peak-to-trough height
  - pulse_width_half_height    how wide the pulse is at half its height (shape/timing feature)
  - area_under_curve           total area under one heartbeat cycle

Then aggregates these per RECORDING (mean + standard deviation across that recording's
heartbeats), because the actual thing we're predicting (Glucose_level) is one value per
recording, not per individual heartbeat — modeling at the heartbeat level would treat the same
true label as hundreds of "different" independent examples, which overstates how much data we
really have and risks leaking near-identical heartbeats from the same recording across a
train/test split later.

Also computes heart rate variability (HRV) properly at the recording level: the standard
deviation of consecutive heartbeat intervals within a recording, which is meaningless for a
single isolated heartbeat.

Run with:  .venv/bin/python ml/notebooks/day8_features.py
Outputs:   ml/data/processed/heartbeat_features.csv   (one row per heartbeat)
           ml/data/processed/recording_features.csv   (one row per recording - what Day 9+ modeling uses)
"""
import numpy as np
import pandas as pd

IN_PATH = "ml/data/processed/segments.csv"
OUT_HEARTBEAT = "ml/data/processed/heartbeat_features.csv"
OUT_RECORDING = "ml/data/processed/recording_features.csv"


def extract_shape_features(cycle):
    """cycle is a 1D array of SEGMENT_LENGTH resampled points spanning one peak-to-peak
    heartbeat (so it starts near the systolic peak, dips to the trough, shows the dicrotic
    notch, then rises back toward the next peak)."""
    n = len(cycle)
    systolic_peak_amplitude = cycle[0]  # the cycle boundary IS the systolic peak, by construction
    trough_idx = int(np.argmin(cycle))
    trough_amplitude = cycle[trough_idx]
    pulse_amplitude = systolic_peak_amplitude - trough_amplitude

    # dicrotic notch / diastolic peak: the highest point strictly after the trough (before the
    # cycle climbs all the way back up toward the next systolic peak at the very end)
    search_zone = cycle[trough_idx:n - 5] if trough_idx < n - 5 else cycle[trough_idx:]
    if len(search_zone) > 2:
        diastolic_peak_amplitude = search_zone.max()
    else:
        diastolic_peak_amplitude = np.nan

    reflection_index = (
        diastolic_peak_amplitude / systolic_peak_amplitude
        if systolic_peak_amplitude != 0 else np.nan
    )

    # pulse width at half height (a standard PPG shape descriptor)
    half_height = trough_amplitude + pulse_amplitude / 2
    above = np.where(cycle >= half_height)[0]
    pulse_width_half_height = (above.max() - above.min()) / n if len(above) > 0 else np.nan

    area_under_curve = np.trapezoid(cycle - trough_amplitude) / n  # normalized by length

    return {
        "systolic_peak_amplitude": systolic_peak_amplitude,
        "diastolic_peak_amplitude": diastolic_peak_amplitude,
        "reflection_index": reflection_index,
        "pulse_amplitude": pulse_amplitude,
        "pulse_width_half_height": pulse_width_half_height,
        "area_under_curve": area_under_curve,
    }


def main():
    df = pd.read_csv(IN_PATH)
    point_cols = [c for c in df.columns if c.startswith("p") and c[1:].isdigit()]
    print(f"Loaded {len(df)} heartbeat segments with {len(point_cols)} waveform points each.")

    feature_rows = []
    for _, row in df.iterrows():
        cycle = row[point_cols].to_numpy(dtype=float)
        feats = extract_shape_features(cycle)
        feature_rows.append({
            "patient_id": row["patient_id"],
            "recording_index": row["recording_index"],
            "heartbeat_index": row["heartbeat_index"],
            "glucose": row["glucose"],
            "heart_rate_bpm": row["heart_rate_bpm"],
            **feats,
        })

    feat_df = pd.DataFrame(feature_rows)
    feat_df.to_csv(OUT_HEARTBEAT, index=False)
    print(f"Saved {OUT_HEARTBEAT} ({len(feat_df)} rows).")
    print("\nPer-heartbeat feature summary:")
    print(feat_df.drop(columns=["patient_id", "recording_index", "heartbeat_index"]).describe())

    # --- Aggregate to one row per recording (the actual modeling unit) ---
    numeric_feats = [
        "heart_rate_bpm", "systolic_peak_amplitude", "diastolic_peak_amplitude",
        "reflection_index", "pulse_amplitude", "pulse_width_half_height", "area_under_curve",
    ]
    agg_spec = {f: ["mean", "std"] for f in numeric_feats}
    grouped = feat_df.groupby(["patient_id", "recording_index"])
    rec_df = grouped.agg(agg_spec)
    rec_df.columns = ["_".join(c) for c in rec_df.columns]
    rec_df = rec_df.reset_index()

    # heart rate variability: std of consecutive beat-to-beat intervals within a recording
    # (implied by heart_rate_bpm's std across beats, already computed above as heart_rate_bpm_std -
    #  renaming it to be explicit about what it represents)
    rec_df = rec_df.rename(columns={"heart_rate_bpm_std": "hrv_bpm_std"})

    n_beats = grouped.size().rename("n_heartbeats")
    glucose = grouped["glucose"].first().rename("glucose")
    rec_df = rec_df.merge(n_beats, on=["patient_id", "recording_index"])
    rec_df = rec_df.merge(glucose, on=["patient_id", "recording_index"])

    rec_df.to_csv(OUT_RECORDING, index=False)
    print(f"\nSaved {OUT_RECORDING} ({len(rec_df)} rows - one per recording).")
    print(rec_df.describe())


if __name__ == "__main__":
    main()
