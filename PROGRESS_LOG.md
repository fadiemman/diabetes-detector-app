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
