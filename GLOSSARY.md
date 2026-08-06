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

## Day 4 terms

- **Ground truth:** The real, trusted measurement used as the "correct answer" a model is trained
  to predict — here, an actual glucose reading, not a guess.
- **Glucometer:** A handheld device that measures blood glucose from a finger-prick blood sample
  — the standard, invasive way people with diabetes check their levels at home.
- **Continuous glucose monitor (CGM):** A wearable sensor (e.g. Dexcom) that automatically reads
  glucose every few minutes without finger-pricks, usually via a small sensor under the skin.
- **Transmission vs. reflectance PPG:** Transmission PPG shines light through tissue (e.g. a
  fingertip, light passing all the way through) — how a phone camera + flash setup works.
  Reflectance PPG shines light in and measures what bounces back (e.g. a wrist-worn sensor).
  Different placements can produce meaningfully different waveform shapes.
- **Dataset license (e.g. CC BY-NC-ND):** The legal terms for how a public dataset may be used —
  "NC" means non-commercial use only, "ND" means you can't redistribute a modified version of the
  dataset itself. Worth checking before building on any public dataset.

## Day 5 terms

- **Data integrity check:** Verifying that a dataset actually means what it claims to (e.g.
  confirming a label really matches the right row) before trusting it for anything — rather than
  assuming a downloaded file is correct.
- **Interleaved / round-robin data:** Rows from several different recordings mixed together in
  rotating order (recording A's 1st sample, B's 1st sample, C's 1st sample, then A's 2nd sample...)
  rather than stored one recording after another.
- **Rolling / windowed feature:** A value recalculated periodically over a moving slice of time
  (e.g. "heart rate over the last few seconds"), as opposed to one fixed number for an entire
  recording.

## Day 6 terms

- **EDA (exploratory data analysis):** Looking at a dataset with plots and summary statistics
  before modeling it, specifically to catch problems or surprises early.
- **Histogram:** A bar chart showing how many data points fall into each range of values — used
  here to show how glucose readings are spread out across the dataset.
- **Outlier:** A data point that's unusually different from the rest (e.g. an extremely short
  recording here) — worth investigating rather than ignoring, since it can either be a real edge
  case or a sign of a data problem.
- **Exclusion criteria:** A clearly stated rule for which data points get left out of analysis/
  training (e.g. "recordings shorter than 3 seconds"), documented so the decision is transparent
  and repeatable rather than an invisible judgment call.

## Day 7 terms

- **Bandpass filter:** A filter that keeps only a chosen range of frequencies (here, 0.5-8 Hz —
  the plausible heart-rate range) and removes everything slower or faster than that range.
- **Numerical stability (of a filter):** Whether a computation stays well-behaved and accurate,
  or blows up into meaningless huge/tiny numbers due to how it's represented internally — a real
  bug we hit and fixed today by switching filter representations.
- **Second-order sections (SOS):** A more numerically robust way to represent a digital filter,
  especially important for higher-order filters or narrow frequency bands at high sample rates.
- **Dicrotic notch:** A small secondary bump in a PPG waveform shortly after the main heartbeat
  peak, caused by a reflected pulse wave bouncing back from further in the body.
- **Resampling (a signal):** Converting a signal to a different number of points while preserving
  its overall shape — used here so heartbeat cycles of different lengths (different heart rates)
  can still be compared point-for-point.

*(More terms get added here at the end of every session — this file should read like a
cheat-sheet by the time the project is done.)*
