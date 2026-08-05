# Roadmap — Diabetes Detector App

Pace: roughly **one step per session/day**. Do not skip ahead — each phase builds on the
previous one, and each step ends with something that actually runs, so we never end up with a
pile of half-finished pieces.

Legend: each step lists what we'll build, and the new technical terms/tools it introduces
(these get added to `GLOSSARY.md` as we go, for interview prep).

---

## Phase 0 — Foundations & Setup

- **Day 0 (today):** Project scaffold created — folder structure, README, this roadmap,
  glossary, progress log, `.gitignore`. Local git repository initialized.
  *Terms: repository, README, .gitignore, markdown.*
- **Day 1:** Create an empty repository on GitHub and connect this project to it (`git remote`,
  `git push`). Learn the core git workflow: `git status`, `git add`, `git commit`, `git push`,
  branches.
  *Terms: git, GitHub, remote, commit, branch, push/pull.*
- **Day 2:** Set up the Python environment (virtual environment) and Node.js environment;
  install first libraries (`pandas`, `numpy`, `scikit-learn`, `fastapi`). Understand what a
  virtual environment is and why we use one.
  *Terms: virtual environment, pip, package manager, dependency.*

## Phase 1 — Understanding the Science & the Data

- **Day 3:** Learn PPG (photoplethysmography) fundamentals — how a camera + light picks up the
  blood-volume pulse, what heart rate/SpO2-style signals look like, and honestly, why glucose
  estimation from this signal is hard and not yet clinically solved. Written up in
  `GLOSSARY.md`/`docs/`.
  *Terms: PPG, photoplethysmography, blood volume pulse, signal-to-noise ratio.*
- **Day 4:** Compare candidate public datasets that pair PPG signals with blood glucose
  readings, pick one (or two) to start with, and document exactly what's inside them (sampling
  rate, number of subjects, labels).
  *Terms: dataset, sampling rate, ground truth label, data dictionary.*
- **Day 5:** Download the chosen dataset(s) into `ml/data/raw/` and do a first inspection with
  pandas (row counts, columns, missing values).
  *Terms: dataframe, missing data, raw vs. processed data.*

## Phase 2 — Data Exploration & Preprocessing

- **Day 6:** Exploratory Data Analysis (EDA) — plot example PPG waveforms and the distribution
  of glucose values in the dataset; note anything unusual.
  *Terms: EDA, histogram, outlier.*
- **Day 7:** Clean and filter the raw signal (remove noise, normalize scale) and segment it into
  individual heartbeat cycles.
  *Terms: signal filtering, normalization, segmentation.*
- **Day 8:** Extract features from each segment — heart rate, pulse rate variability, waveform
  shape descriptors (systolic/diastolic peak ratios, area under the curve). These numeric
  features are what the ML model actually learns from.
  *Terms: feature extraction, feature engineering, heart rate variability (HRV).*
- **Day 9:** Build the train/validation/test split and save the processed feature table to
  `ml/data/processed/`.
  *Terms: train/validation/test split, data leakage, reproducibility (random seed).*

## Phase 3 — Model Building & Training

- **Day 10:** Train a simple baseline model (linear regression or k-nearest-neighbors) to predict
  glucose from the extracted features; measure error with MAE/RMSE. This baseline is our
  "can we beat this" reference point.
  *Terms: regression, baseline model, MAE, RMSE, overfitting.*
- **Day 11:** Try stronger classical models (Random Forest, Gradient Boosting/XGBoost) and
  compare against the baseline.
  *Terms: ensemble model, decision tree, hyperparameter, cross-validation.*
- **Day 12 (optional/stretch):** Try a small deep learning model (1D CNN or LSTM) directly on the
  raw waveform instead of hand-engineered features, and compare.
  *Terms: neural network, CNN, LSTM, epoch, loss function.*
- **Day 13:** Pick the best-performing model, save it to disk, and write an honest results
  section (including the model's real limitations) into the README.
  *Terms: model serialization (joblib/ONNX), model evaluation, bias/limitations reporting.*

## Phase 4 — Backend API

- **Day 14:** Scaffold a FastAPI backend with a `/predict` endpoint that will accept extracted
  features and return a predicted glucose value / risk category.
  *Terms: REST API, endpoint, HTTP request/response, JSON.*
- **Day 15:** Load the trained model into the backend and test it locally (via `curl` or
  Postman) with sample data.
  *Terms: model inference, request/response body, status codes.*
- **Day 16:** Add input validation, error handling, and basic automated tests.
  *Terms: validation, exception handling, unit test, pytest.*

## Phase 5 — Frontend Web App (React)

- **Day 17:** Scaffold a React app (using Vite) with a basic page layout.
  *Terms: React, component, JSX, props, state, Vite/bundler.*
- **Day 18:** Implement camera capture in the browser (getUserMedia API) so the user can point
  the camera at a fingertip and record a short clip.
  *Terms: MediaDevices API, getUserMedia, video stream.*
- **Day 19:** Connect the frontend to the backend — send captured signal/features to `/predict`
  and receive the result.
  *Terms: fetch/axios, API integration, CORS, async/await.*
- **Day 20:** Build the results UI (loading state, result display, error state, and the medical
  disclaimer).
  *Terms: conditional rendering, UX states, accessibility basics.*

## Phase 6 — Testing, Refinement, Mobile (stretch)

- **Day 21:** End-to-end test with real captures; if you have access to a real glucometer,
  compare and log the results honestly.
  *Terms: end-to-end testing, ground-truth comparison.*
- **Day 22:** Polish the UI/UX and add a "how this works" explainer page.
- **Day 23 (stretch):** Port the app to React Native for a true installable mobile app with
  full native camera control.
  *Terms: React Native, native module, Expo.*

## Phase 7 — Deployment & Portfolio Prep

- **Day 24:** Deploy the backend (e.g. Render/Railway/Fly.io free tier) and frontend (e.g.
  Vercel/Netlify).
  *Terms: deployment, hosting, environment variables, CI/CD (basic).*
- **Day 25:** Write the final README with an architecture diagram and a "what I built and why"
  section framed for interviews — every technology named, and why it was chosen.
- **Day 26:** Record a short demo video/GIF for your portfolio.

---

### How we'll work day to day

Each session we'll do exactly one numbered step above: I'll explain what we're doing and why
before writing any code, we'll build/run it together, and I'll update `PROGRESS_LOG.md` and
`GLOSSARY.md` with what's new. If a step turns out bigger than expected, we split it rather than
rushing — better to have five solid days than one messy one.
