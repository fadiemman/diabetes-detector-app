# Diabetes Detector App (Learning Project)

A full-stack, research-style project that estimates blood glucose / diabetes risk from a
smartphone camera (PPG signal) and, optionally, other phone sensors — built step by step as a
learning + portfolio project.

## Important disclaimer

This project is a **research/educational prototype**, not a medical device. Camera-based
(photoplethysmography, "PPG") blood glucose estimation is an active academic research area,
not a clinically validated or regulator-approved method. Predictions from this app should
never be used to make real medical decisions. This disclaimer will also be shown inside the
app itself.

## What this project actually does

1. Captures a PPG signal — the tiny color/brightness changes in a fingertip caused by blood
   pulsing with each heartbeat — using a phone or laptop camera.
2. Extracts features from that signal (heart rate, waveform shape, pulse variability, etc.).
3. Feeds those features into a machine learning model trained on public PPG + blood-glucose
   datasets to estimate a glucose value / risk category.
4. Serves the model through a backend API and shows the result in a web (and later mobile) app.

## Project status

We are building this one step at a time — see `ROADMAP.md` for the full plan and
`PROGRESS_LOG.md` for what has actually been done so far.

## Tech stack (filled in as we build)

- **Data science / ML:** Python, pandas, numpy, scikit-learn (and possibly PyTorch/TensorFlow)
- **Backend:** FastAPI (Python)
- **Frontend:** React (web first), React Native later for a real mobile app
- **Version control:** Git + GitHub

## Repo structure

```
diabetes-detector-app/
├── README.md          – you are here
├── ROADMAP.md          – the full, day-by-day build plan
├── GLOSSARY.md         – every technical term we use, explained in plain language
├── PROGRESS_LOG.md      – dated log of what we actually did each session
├── ml/                 – datasets, notebooks, training scripts, saved models (added in Phase 1-3)
├── backend/            – API server (added in Phase 4)
└── frontend/           – React app (added in Phase 5)
```

## Why this project is good for interviews

Because we're building every layer ourselves — data acquisition, signal processing, ML model
training and evaluation, a REST API, and a React frontend — this project touches nearly every
skill a full-stack / ML-adjacent interview might probe. `GLOSSARY.md` is being kept specifically
so every term used here can be explained confidently.
