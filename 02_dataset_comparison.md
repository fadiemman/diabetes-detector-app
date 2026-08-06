# Day 4 — Comparing Candidate Datasets

Before writing a line of ML code, we need real data: a set of PPG (pulse) signals, each paired
with a true, lab-measured blood glucose value. Here are the three public candidates that were
worth investigating, what was actually confirmed about each, and which one we're starting with.

## Candidate 1: Mendeley "Mazandaran" PPG + glucose dataset — **chosen for Day 5**

- **Source:** [Mendeley Data, ID 37pm7jk7jn](https://data.mendeley.com/datasets/37pm7jk7jn/1) —
  "The dataset of photoplethysmography signals collected from a pulse sensor to measure blood
  glucose level."
- **Confirmed details** (via the paper [Non-Invasive Glucose Level Monitoring from PPG using a
  Hybrid CNN-GRU Deep Learning Network](https://arxiv.org/html/2411.11094v1), which uses this
  exact dataset): 67 raw PPG recordings from 23 participants, sampled at 2175 Hz, with blood
  glucose measured using a standard finger-prick glucometer (Accu-Chek Active).
- **Why it fits us:** a pulse sensor placed on a fingertip is the closest public match to what a
  phone camera + flash captures — same body location, same underlying signal type (transmission
  PPG through a fingertip), and the ground truth is a real glucose reading, not a proxy.
- **Known limitation (their words, not just ours):** glucose values in this dataset mostly fall
  in a narrow range (roughly 88-187 mg/dL, concentrated around 98-138 mg/dL) — i.e. it's weighted
  toward normal/near-normal glucose levels, not people in a strongly hyperglycemic state. The
  original authors flag this as a limitation for clinical use, and we'll flag it too: our model
  will be more meaningfully tested on "is glucose in the normal range or not" than on precise
  values across the full diabetic range.
- **Size:** small (67 recordings) by modern ML standards, but appropriate as a first, learnable
  dataset while we build the whole pipeline end to end. We can add a second dataset later once
  the pipeline works.

## Candidate 2: PhysioCGM — multimodal dataset, Nature Scientific Data (2025)

- **Source:** [A multimodal physiological dataset for non-invasive blood glucose estimation](https://www.nature.com/articles/s41597-025-06090-6), data on
  [FigShare](https://doi.org/10.6084/m9.figshare.28136294).
- **Confirmed details:** 10 participants with Type 1 diabetes, recorded continuously for up to 17
  days each in normal daily life (not a lab visit). PPG from an Empatica E4 wrist sensor (64 Hz),
  plus ECG, skin conductance, temperature, and accelerometer data. Glucose ground truth from a
  Dexcom G6 continuous glucose monitor, a real reading every 5 minutes.
- **Why it's tempting:** far more data volume (multi-day, multi-signal, continuous glucose
  labels instead of single-point finger-pricks) and it's specifically built for this kind of
  research.
- **Why we're not starting here:** the PPG is captured at the *wrist* by a dedicated medical
  wearable, not a fingertip by an RGB phone camera — a meaningfully different sensor placement
  and signal chain than our app. It's also licensed CC BY-NC-ND (non-commercial, no derivative
  redistribution), which is fine for our non-commercial research use but worth knowing.
- **Plan:** keep this as a strong **Phase 3 stretch dataset** once our basic pipeline works on
  Candidate 1 — it would let us test whether the approach generalizes to a much larger, more
  realistic dataset.

## Candidate 3: Kaggle "PPG signal with Blood sugar level data"

- **Source:** [Kaggle dataset by muhammadyasirsaleem](https://www.kaggle.com/datasets/muhammadyasirsaleem/ppg-signal-with-blood-sugar-level-data).
- **Status:** Kaggle's page didn't expose enough detail through automated fetching to confirm
  subject count, sampling rate, or exact license, and it may in fact be a re-hosting of the same
  underlying Mazandaran data. We're not relying on it for now — if we ever need it, we'll
  reassess once we can inspect it directly (e.g. after downloading, on Day 5).

## Decision

We'll build the pipeline first on the **Mendeley Mazandaran dataset (Candidate 1)** — closest
match to our real sensor setup, real invasive-glucometer ground truth, small enough to move fast
with. We'll be upfront in the README about its narrow glucose range. Once the full pipeline
(preprocessing → features → model → API → app) works end to end, PhysioCGM is the natural next
dataset to try, to see if the approach holds up on a much larger, more realistic sample.

**Next up (Day 5):** download the Mendeley dataset into `ml/data/raw/` and do a first inspection.
