# Day 7 — Cleaning, Filtering, and Segmenting into Heartbeats

Script: `ml/notebooks/day7_preprocessing.py`. Output: `ml/data/processed/segments.csv`
(regenerable from the script — not committed to git, since raw/processed data files are
gitignored by design; the script is the reproducible, committed artifact).

## A real bug, found and fixed

The first version of the bandpass filter (0.5-8 Hz, isolating the heart-rate frequency range and
removing baseline drift/high-frequency noise) silently produced garbage: filtered values around
**10^110** instead of a normal signal. This is a known numerical-stability issue with
`scipy.signal.butter`'s default output form (`b, a` transfer-function coefficients) at a high
sample rate (2175 Hz) combined with such a narrow passband relative to that rate — the
coefficients become poorly conditioned. The fix is to request `output="sos"` (second-order
sections) instead, which is the numerically robust way to represent the same filter, and use
`sosfiltfilt` instead of `filtfilt`. After the fix, the filtered signal looks exactly as
expected — see the figure below.

This is worth calling out because it produced *no error message* — the pipeline ran, filled a
dataframe, and returned zero usable heartbeat segments, which could easily have been misread as
"this dataset just doesn't work" rather than "the filter is broken." Catching it required
actually inspecting intermediate values rather than trusting that no-crash means correct.

## Pipeline steps

1. **Minimum-length filter:** recordings shorter than 4 seconds are dropped (see Day 6's finding
   of some ~0.3-second recordings). This dropped **7 of 62 recordings**, leaving **55**.
2. **Bandpass filter (0.5-8 Hz):** removes slow baseline wander and high-frequency noise while
   keeping the physiologically plausible heart-rate range (30-480 bpm).
3. **Normalization (z-score):** rescales each recording to mean 0, standard deviation 1, so
   recordings with different absolute signal levels become comparable.
4. **Heartbeat segmentation:** detect peaks (one per heartbeat) with `scipy.signal.find_peaks`,
   then cut the signal between each consecutive pair of peaks and resample every cycle to a
   fixed 100 points, so cycles from different heart rates are still directly comparable in
   shape.

## Peak detection is a heuristic, not a perfect solution — documented honestly

Early testing (before settling on final parameters) showed that a real PPG waveform has a
**dicrotic notch** — a smaller secondary bump shortly after the main systolic peak, caused by
the reflected pulse wave — which a too-permissive peak detector can occasionally mistake for a
second heartbeat, producing an implausible short interval right next to a normal one. Capping the
minimum allowed distance between peaks at a plausible **150 bpm** (rather than a very permissive
200+ bpm) filters out most of these false detections. This is a tunable heuristic that works well
enough for this dataset, not a fully robust systolic-peak detector — worth remembering if we ever
see a recording with unusually noisy segmentation results.

## Results

- **474 individual heartbeat segments** extracted from 55 recordings (~8.6 per recording).
- Visual sanity check below: the raw signal, the cleaned/filtered signal with detected peaks
  marked, and 30 real segmented heartbeat cycles overlaid — they line up consistently in shape,
  which is a good sign the segmentation is working correctly.

![Filtering example](figures/filtering_example.png)

![Segmented heartbeats](figures/segmented_heartbeats.png)

## Next up (Day 8)

Turn each segmented heartbeat into a small set of meaningful numeric features (heart rate, peak
ratios, area under the curve, etc.) — the actual inputs our ML model will learn from.
