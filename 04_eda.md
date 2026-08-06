# Day 6 — Exploratory Data Analysis (EDA)

Script: `ml/notebooks/day6_eda.py` (run with `.venv/bin/python ml/notebooks/day6_eda.py`).
Figures: `docs/figures/`.

## Correcting one thing from Day 5

While reconstructing the recordings for plotting, I realized the `index` column isn't reset to 0
for each patient the way I first assumed — it's actually one continuous recording ID across the
*entire* dataset (patient 16's three recordings are IDs 21, 22, and 23, for example, not 0-2).
That doesn't change anything we concluded on Day 5 — glucose labels are still correctly matched
per recording — it's just a more accurate mental model of the column, and it means grouping by
`(Patient_Id, index)` (or by `index` alone) both correctly identify one real recording.

## Reconstructed recordings

Undoing the interleaving gives **62 distinct recordings across 22 patients** (a couple fewer
than the ~67/23 the literature describes for the full raw dataset, consistent with patient #4
being entirely absent from this CSV export, as noted on Day 5).

## Glucose distribution (one value per recording, not per raw sample)

![Glucose distribution](figures/glucose_distribution.png)

Min 88, median 110, max 183 mg/dL — a real spread, but leaning toward the normal/near-normal
range, same conclusion as Day 5's per-row version, just now measured correctly (a value counted
once per recording, not once per raw sample — a recording with more samples was silently
over-represented in yesterday's per-row version).

## Real PPG waveforms

![Example waveforms](figures/example_waveforms.png)

The lowest-glucose and highest-glucose recordings' first ~3 seconds, plotted directly from the
reconstructed raw signal. Both show a clear, repeating pulsatile waveform — visually confirming
this is genuine PPG data with a real heartbeat rhythm, not noise. Good sign before we invest time
in feature extraction.

## Something unusual worth flagging: wildly different recording lengths

| stat | samples |
|---|---|
| min | 722 |
| 25th percentile | 11,702 |
| median | 14,590 |
| 75th percentile | 17,311 |
| max | 19,825 |

At the dataset's ~2175 Hz sampling rate, 722 samples is only about **0.33 seconds** — likely not
even a full heartbeat cycle. Three of patient 16's recordings are this short. That's a genuine
data quality issue, not something we're introducing: a recording that short may not contain
enough of a waveform to reliably compute heart rate or waveform-shape features at all.

**Decision for Day 7:** rather than silently including these, we'll set a minimum-length
threshold (e.g. at least ~3-4 full seconds, enough for several heartbeats) and explicitly exclude
recordings below it, documenting exactly how many get dropped and why — instead of pretending
every recording is equally usable.

## Next up (Day 7)

Clean and filter the raw signal (remove noise, normalize scale) and segment each recording into
individual heartbeat cycles, using only the recordings that pass the minimum-length check above.
