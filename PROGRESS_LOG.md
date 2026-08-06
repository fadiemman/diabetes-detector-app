# Progress Log

A dated record of what was actually done each session (separate from the plan in
`ROADMAP.md`, which is what we *intend* to do).

---

### 2026-08-03 — Day 0: Project kickoff

- Decided on the project: a smartphone-camera-based diabetes/blood-glucose estimator (PPG-based),
  framed explicitly as a research/portfolio prototype, not a medical device.
- Reviewed current research on smartphone-camera PPG glucose estimation and identified candidate
  public datasets (Mendeley PPG+glucose dataset, a 2025 multimodal dataset in Nature Scientific
  Data, and a Kaggle PPG+blood-sugar dataset) — to be evaluated properly in Phase 1.
- Decisions made:
  - Frontend: build a React web app first (browser camera capture), port to React Native later
    if the web version works well.
  - Version control: local git now; GitHub repo to be created and connected on Day 1.
  - Scope: aim for the full pipeline (feature extraction → glucose estimation), clearly labeled
    as an experimental/research result, rather than stopping at an easier proxy task.
  - Project folder connected on the user's own computer (via the Claude desktop app) so files
    stay available locally, not just inside this session.
- Created project scaffold: `README.md`, `ROADMAP.md`, `GLOSSARY.md`, this log, and
  `.gitignore`. Initialized local git repository with the first commit.

**Next up (Day 1):** create an empty GitHub repository and connect this project to it.

---

### 2026-08-05 — Day 1: Connected to GitHub

- Created an empty, public GitHub repository: `fadiemman/diabetes-detector-app`.
- Ran into a sandbox limitation: Claude's cloud workspace has a network security layer that
  blocks git pushes to repositories that weren't pre-authorized for the session, even with a
  valid personal access token — so the push had to be done from the user's own computer instead.
- User initialized git locally in the OneDrive project folder and successfully pushed the Day 0
  scaffold to GitHub. The repo is now live.
- **Working pattern going forward:** Claude does the actual coding/training in its cloud
  workspace, syncs updated files into the local project folder (via the desktop bridge), and the
  user commits + pushes from their own machine using the three commands: `git add -A`,
  `git commit -m "..."`, `git push`.

**Next up (Day 2):** set up the Python virtual environment and install the first ML/backend
libraries.

---

### 2026-08-05 — Day 2: Environment setup

- Created a Python virtual environment (`.venv`) for the project.
- Installed the first set of libraries: `pandas`, `numpy`, `scikit-learn`, `matplotlib`,
  `fastapi`, `uvicorn`, `joblib` — recorded in `requirements.txt` so the environment can be
  recreated exactly.
- Confirmed Node.js (v22) and npm (v10) are available for the React frontend, which we'll set up
  later in Phase 5.
- Added `SETUP.md` explaining how to recreate this environment locally if the user ever wants to
  run the project on their own machine.

**Next up (Day 3):** learn PPG (photoplethysmography) fundamentals and write up, in plain
language, how a camera can pick up a pulse signal — and be honest about why glucose estimation
from it is scientifically hard.

---

### 2026-08-06 — Day 3: PPG fundamentals

- Wrote up `docs/01_ppg_fundamentals.md`: how PPG works, how a phone camera + flash acts as a
  light sensor, what's reliably measurable (heart rate, HRV, rough SpO2), and — importantly —
  why blood glucose is a fundamentally harder, indirect signal to extract compared to oxygen,
  with real research sources.
- Also fixed a Day 2 bug: `requirements.txt` had pulled in `uvloop`, a Linux/Mac-only performance
  package, which broke `pip install` on the user's Windows machine. Removed it (uvicorn works
  fine without it) and reinstalled cleanly on Windows.
- Confirmed working pattern: user is on a work laptop this week (different device than the one
  originally connected), so files are being handed over via chat and pushed manually through
  VS Code rather than the automatic desktop bridge — works exactly the same either way.

**Next up (Day 4):** compare the candidate public PPG + blood-glucose datasets and pick which
one(s) to build with.

---

### 2026-08-06 — Day 4: Dataset comparison and choice

- Researched and compared three candidate public datasets in `docs/02_dataset_comparison.md`:
  the Mendeley "Mazandaran" fingertip PPG + glucometer dataset (23 subjects, 67 recordings,
  2175 Hz), the PhysioCGM multimodal dataset (10 subjects, wrist PPG + Dexcom CGM, multi-day),
  and a Kaggle dataset that couldn't be fully verified.
- **Decision:** start with the Mendeley Mazandaran dataset — it's the closest match to our
  fingertip-camera concept and uses real glucometer readings as ground truth, even though it's
  small and skewed toward near-normal glucose values (a limitation we're documenting honestly
  rather than hiding). PhysioCGM is noted as a strong stretch dataset for later, once the
  pipeline works end to end.

**Next up (Day 5):** download the chosen dataset into `ml/data/raw/` and do a first inspection
with pandas.

---

### 2026-08-06 — Day 5: Got the real data, and a detour

- Downloaded the Mendeley Mazandaran dataset (via the user's browser, since this environment
  can't reach data-hosting sites directly) — 67 raw signal `.mat` files, 67 label `.mat` files,
  and figures, now in `ml/data/raw/`.
- Hit a real blocker: the label files store glucose values as MATLAB "table" objects, a
  proprietary format. Neither Python (scipy) nor Octave (installed specifically to double-check)
  could decode them without actual MATLAB software.
- Found that the same dataset's creator had already exported a clean CSV version to Kaggle
  ("PPG signal with Blood sugar level data") — same subjects/recordings, already unpacked. Had
  the user download and upload that instead.
- Did the first real inspection in `docs/03_data_inspection.md`: 844,946 rows, 22 patients (one
  missing from this export), zero missing values, and — importantly — verified the glucose
  labels are correctly matched to the right recording despite an unusual interleaved row
  ordering. Also flagged that some pre-computed feature columns look like rolling/windowed
  estimates rather than one-per-recording values, so we'll compute our own features later rather
  than trust them blindly.

**Next up (Day 6):** plot a few real PPG waveforms and the glucose distribution — the actual EDA
(exploratory data analysis).

---

### 2026-08-06 — Day 6: EDA — real waveforms and the true glucose distribution

- Wrote `ml/notebooks/day6_eda.py`, which reconstructs 62 distinct recordings (undoing the
  interleaved row structure) and plots: the glucose distribution correctly measured once per
  recording (`docs/figures/glucose_distribution.png`), and the actual PPG waveform for the
  lowest- and highest-glucose recordings (`docs/figures/example_waveforms.png`) — both show a
  clean, repeating heartbeat pattern, a good sign.
- Corrected a small misunderstanding from Day 5: the `index` column is one continuous recording
  ID across the whole dataset, not reset per patient — doesn't change any conclusion, just a
  clearer mental model.
- Flagged a real data quality issue: recording lengths vary from 722 to 19,825 samples — the
  shortest ones (all from patient 16) are under half a second, likely too short to contain even
  one full heartbeat. Decided to exclude recordings below a minimum-length threshold starting
  Day 7, rather than silently including unreliable ones.

**Next up (Day 7):** clean/filter the signal and segment each (sufficiently long) recording into
individual heartbeat cycles.

---

### 2026-08-06 — Day 7: Filtering, segmentation, and a real bug fixed

- Wrote `ml/notebooks/day7_preprocessing.py`: drops recordings under 4 seconds (7 of 62 dropped),
  bandpass-filters (0.5-8 Hz) and z-score normalizes the rest, then detects heartbeats and cuts
  each recording into individual, fixed-length (resampled) heartbeat segments.
- Hit and fixed a real, silent bug: the first version of the filter produced numerically unstable
  garbage (values around 10^110) due to how `scipy.signal.butter` represented the filter at this
  sample rate/passband combination — switched to the more robust "second-order sections" (SOS)
  form, which fixed it completely. No error was thrown; it required actually inspecting
  intermediate values to catch.
- Extracted 474 individual heartbeat segments from the 55 usable recordings. Visual sanity check
  (in `docs/05_preprocessing.md`) shows the segments line up consistently in shape.
- Documented that peak detection is a tuned heuristic (capped at a plausible 150 bpm to avoid
  mistaking the PPG waveform's "dicrotic notch" for a second heartbeat), not a perfect solution.

**Next up (Day 8):** turn each heartbeat segment into meaningful numeric features (heart rate,
peak ratios, area under the curve) for the model to actually learn from.

---

### 2026-08-06 — Day 8: Feature engineering

- Went back and added `cycle_length_samples`/`heart_rate_bpm` to Day 7's segment output (needed
  for real heart-rate features, missed on the first pass).
- Wrote `ml/notebooks/day8_features.py`: computes 7 shape/timing features per heartbeat
  (systolic/diastolic peak amplitude, reflection index, pulse amplitude, pulse width, area under
  curve, heart rate), then aggregates to **one row per recording** (55 rows) rather than one row
  per heartbeat — important, since the true glucose label only exists per recording, and
  modeling at the heartbeat level would let the same recording leak across train/test later.
  Also computed heart rate variability properly at the recording level.
- Found `pulse_width_half_height` is nearly constant/uninformative, a side effect of our
  peak-to-peak segmentation choice — flagged rather than hidden, to revisit at Day 10.
- Ran a correlation sanity check against glucose: all weak (under ~0.3), matching Day 3's
  expectation that PPG-glucose signal is indirect and weak, not a modeling failure.

**Next up (Day 9):** build the train/validation/test split on the 55 recording-level rows.
