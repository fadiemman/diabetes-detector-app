# Day 8 — Feature Engineering

Script: `ml/notebooks/day8_features.py`. Reads Day 7's 474 heartbeat segments, outputs
`ml/data/processed/heartbeat_features.csv` (one row per heartbeat) and, more importantly,
`ml/data/processed/recording_features.csv` (one row per **recording** — 55 rows, matching the
55 usable recordings from Day 7). That second file is what we'll actually train a model on.

## Why aggregate up to one row per recording

`Glucose_level` is a single true value *per recording*, not per individual heartbeat. If we
trained directly on 474 heartbeat-level rows, the same true glucose value would appear ~8-9
times (once per heartbeat in that recording), and a naive train/test split could put some
heartbeats from the same recording in training and others in testing — letting the model
"cheat" by recognizing a recording it's effectively already seen. Aggregating to one row per
recording (using the mean and standard deviation of each feature across that recording's
heartbeats) avoids this, and gives an honest 55 independent examples to work with.

## Features computed per heartbeat, then aggregated per recording

- **heart_rate_bpm** — beats per minute, from the time between consecutive heartbeat peaks.
- **systolic_peak_amplitude** — how tall the main pulse is.
- **diastolic_peak_amplitude** — how tall the secondary "dicrotic notch" bump is (the reflected
  pulse wave, mentioned back on Day 7).
- **reflection_index** — diastolic ÷ systolic amplitude. This is a real, published PPG feature
  linked (weakly) to arterial stiffness, one of the more literature-grounded features here.
- **pulse_amplitude** — the height from trough to systolic peak.
- **pulse_width_half_height** — how wide the pulse is at half its height.
- **area_under_curve** — the total area under one heartbeat cycle.
- **hrv_bpm_std** (heart rate variability) — computed properly at the recording level, as the
  standard deviation of heart rate *across that recording's heartbeats* — this genuinely can't be
  computed from a single isolated heartbeat, which is why it only makes sense after aggregation.

## An honest problem found in one of these features

`pulse_width_half_height` turned out to be nearly constant (~0.99 for most heartbeats) — not a
useful, varying feature at all. The reason: our heartbeat segments are defined **peak-to-peak**
(Day 7), so both ends of every segment are already near the systolic peak height, and only the
brief dip around the trough drops below half-height. That makes this feature closer to "how
narrow is the trough dip" than the usual clinical meaning of pulse width, and with so little
variation it likely won't help the model much. Flagging this now rather than silently keeping a
near-useless feature — Day 10's feature-importance check will confirm whether it's worth keeping.

## Sanity check: correlation with glucose

| feature | correlation with glucose |
|---|---|
| systolic_peak_amplitude_std | 0.30 |
| pulse_amplitude_mean | -0.29 |
| pulse_amplitude_std | 0.22 |
| area_under_curve_mean | -0.16 |
| reflection_index_std | 0.12 |
| hrv_bpm_std | 0.11 |
| heart_rate_bpm_mean | 0.01 (essentially none) |
| pulse_width_half_height_mean | 0.02 (essentially none) |

These are all weak correlations (nothing above ~0.3) — exactly what Day 3's research told us to
expect, since glucose has no direct optical signature and only an indirect, weak relationship to
waveform shape. This isn't a failure; a real model will need to combine many weakly-correlated
features together rather than rely on any single one, which is exactly what Day 10's model
training will attempt. Notably, `heart_rate_bpm` alone shows essentially zero correlation — a
useful, honest reminder that heart rate by itself isn't a meaningful glucose proxy, consistent
with the research we read on Day 3.

## Next up (Day 9)

Build the train/validation/test split on these 55 recording-level rows, and lock in a random
seed so results are reproducible.
