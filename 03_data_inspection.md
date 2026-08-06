# Day 5 — First Data Inspection

## What we're working with

We ended up using the Kaggle "clean" export (`clean-dataset.csv`) rather than the raw Mendeley
`.mat` files directly — see the note at the bottom of `docs/02_dataset_comparison.md` for why: the
raw glucose labels are stored as MATLAB "table" objects, a proprietary format that neither Python
(scipy) nor Octave (a free MATLAB alternative I installed to double-check) can fully decode
without actual MATLAB software. The Kaggle CSV was exported from the same original dataset by the
same researcher, so it's the same underlying subjects and recordings, just already unpacked into a
usable format. The raw `.mat` signal files are still kept in `ml/data/raw/` for reference.

## Basic shape

- **844,946 rows, 13 columns**
- **Zero missing values** in any column — a pleasant surprise for a real-world dataset.
- **22 unique patients** (not 23 as the literature describes for the full raw dataset — patient
  #4 appears to be missing from this export entirely. Worth remembering as a known gap.)

## Understanding the row structure (important, and not obvious at first glance)

Each patient in this dataset had several separate recording sessions (1 to 7 of them). Rather
than simply stacking each recording's samples one after another, the rows in this CSV
**interleave** a patient's recordings round-robin: sample 1 of recording A, sample 1 of recording
B, sample 1 of recording C, ..., then sample 2 of recording A, and so on. The `index` column
(0 through however many recordings that patient has, minus one) tells you which recording a row
actually belongs to.

We verified this carefully rather than assuming it: for every single patient, the number of
distinct `index` values exactly matches the number of distinct `Glucose_level` values, and a
given `index` always maps to the same glucose value throughout — e.g. for patient 1,
`index == 0` is always glucose 99, `index == 1` is always glucose 102, and so on. So **the glucose
labels are correctly and consistently attached to the right recording** — good news, since a
misalignment bug here would have quietly ruined every model we trained on it.

## A modeling caution worth flagging now

The `Heart_Rate`, `Systolic_Peak`, `Diastolic_Peak`, and `Pulse_Area` columns are *not* a single
fixed value per recording the way `Glucose_level` is — they change every few thousand rows within
a single recording (roughly every 1,600 interleaved cycles). That suggests these were computed
as a rolling/windowed estimate over time, recalculated periodically, rather than one summary
number for the whole recording. That's fine to know about, but it means we shouldn't blindly treat
these columns as trustworthy, ready-made per-recording features — on Day 6-8 we'll do our own
proper feature extraction from the raw waveform per recording, and use these existing columns only
as a rough sanity check/comparison, not as ground truth.

## Glucose label distribution

| stat | value (mg/dL) |
|---|---|
| min | 88 |
| 25th percentile | 102 |
| median | 110 |
| mean | 115.4 |
| 75th percentile | 128 |
| max | 183 |

This matches what the original Mendeley dataset description said: concentrated in the normal/
near-normal range, with only a handful of recordings reaching more clearly elevated glucose
levels. This is a real limitation of the data, not something we're introducing — our model will
be more meaningfully evaluated on "is this reading in the normal range or somewhat elevated" than
on precisely nailing values across the full diabetic range.

## Next up (Day 6)

Plot a few actual PPG waveforms (one per recording) and the overall glucose distribution, to see
the signal shape with our own eyes before we start cleaning/filtering it.
