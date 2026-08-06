# Glossary

Plain-language explanations of every technical term this project uses, added as we go. Written
so you can use it directly to prep for interview questions like "what does X mean and why did
you use it here."

## Day 0 terms

- **Repository (repo):** A folder whose history is tracked by git — every change is recorded so
  you can see what changed, when, and go back to an earlier version if needed.
- **Git:** The version control system that tracks those changes locally on your machine.
- **GitHub:** A website that hosts git repositories online, so your code is backed up, visible to
  others (e.g. in a job interview), and shareable.
- **README.md:** The first file people (and you, later) read to understand what a project does.
- **Markdown (.md):** A simple text formatting language (like this file) that renders nicely as
  headings, lists, and bold text on GitHub and elsewhere.
- **.gitignore:** A file listing things git should *not* track (temporary files, secrets,
  dependency folders) so the repository stays clean.

## Day 1 terms

- **Remote:** A copy of the repository stored somewhere else (here, on GitHub) that your local
  git repo can push to / pull from. `origin` is just the conventional name for "the main remote."
- **Push / pull:** Sending your local commits up to the remote (`push`) or bringing the remote's
  commits down to your machine (`pull`).
- **Personal access token (PAT):** A password-like secret that lets a tool authenticate to GitHub
  on your behalf, scoped to only the permissions/repos you allow — safer than using your actual
  GitHub password.

## Day 2 terms

- **Virtual environment:** An isolated, project-specific installation of Python and its
  libraries, so different projects on the same computer can use different (even conflicting)
  library versions without interfering with each other.
- **pip:** Python's package manager — the tool that downloads and installs libraries.
- **Package manager:** A tool that installs, updates, and tracks external code libraries your
  project depends on (`pip` for Python, `npm` for Node.js/React).
- **Dependency:** An external library your project needs in order to run.
- **requirements.txt:** A plain-text file listing every Python package (and exact version) a
  project depends on, so the environment can be recreated identically elsewhere.
- **API framework (FastAPI):** A library for building a web server that other programs (like our
  future React app) can send requests to and get structured responses back from.

## Day 3 terms

- **PPG (photoplethysmography):** Measuring blood flow using light — shine light into skin and
  measure how the reflected/transmitted amount changes with each heartbeat.
- **AC / DC component (of a PPG signal):** The DC part is the steady baseline light absorption;
  the AC part is the small rhythmic ripple caused by pulsing arterial blood — the part carrying
  useful signal.
- **SpO2 (blood oxygen saturation):** The percentage of hemoglobin in blood carrying oxygen,
  estimated from how tissue absorbs red vs. infrared light differently.
- **Heart rate variability (HRV):** The (normal, healthy) variation in time between consecutive
  heartbeats.
- **Confounder:** A factor other than the one you're trying to measure that also affects your
  signal, making it harder to isolate the true relationship (e.g. skin tone or hydration
  affecting a PPG reading meant to estimate glucose).
- **Feature engineering:** Turning raw data (like a waveform) into meaningful numeric measurements
  (like peak sharpness or heart rate) that a machine learning model can actually learn from.

*(More terms get added here at the end of every session — this file should read like a
cheat-sheet by the time the project is done.)*
