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
