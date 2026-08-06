# Day 3 — PPG Fundamentals (and why glucose is the hard part)

## What is PPG?

**Photoplethysmography (PPG)** is a way of measuring blood flow using light. Shine light into
skin (or a fingertip) and measure how much of it comes back (reflected) or passes through
(transmitted) — the amount changes slightly with every heartbeat, because each pulse of blood
briefly changes how much light the tissue absorbs.

That signal has two parts:

- A **DC component** — the steady, unchanging baseline absorption from skin, tissue, bone,
  venous blood, etc.
- An **AC component** — a small, rhythmic ripple on top of that baseline, caused specifically by
  the pulsing arterial blood volume. This ripple is the part we actually care about.

This is exactly how a hospital pulse oximeter (the clip they put on your finger) works, and it's
also what your phone is doing when a fitness app has you cover the camera and flash with your
finger to measure heart rate.

## How a phone does it

The phone's camera acts as the light sensor and the LED flash acts as the light source. When you
press a fingertip over both: light from the flash passes into the fingertip, scatters, and the
camera picks up the small brightness/color changes in every video frame. Plot the average
brightness of the image over time and you get a waveform — a peak each time the heart beats. From
that waveform alone, a phone can reliably measure:

- **Heart rate** — just count the peaks per minute. This is the most reliable thing to extract
  and what most phone-camera heart-rate apps actually do.
- **Heart rate variability (HRV)** — the small variation in time between beats.
- A rough estimate of **blood oxygen saturation (SpO2)**, if the phone uses two light colors
  (red and infrared) rather than one, because oxygenated and deoxygenated blood absorb those two
  wavelengths differently. Many phones only have one usable LED colour for this, which is why
  camera-based SpO2 apps are considered a rough estimate at best, not a medical-grade reading.

## Why blood glucose is a fundamentally different, harder problem

Oxygen has a distinctive optical signature — oxygenated and deoxygenated hemoglobin absorb red
and infrared light differently in a well-understood, direct way. **Glucose does not have an
equivalent, easily-isolated optical fingerprint that a phone camera and visible-light flash can
pick up.** There is no direct "glucose absorbs this wavelength differently" signal available to a
regular RGB camera the way there is for oxygen.

Instead, research in this space (see sources below) looks for **indirect, secondary effects**
that elevated blood glucose has on the cardiovascular system, and tries to detect those in the
shape of the PPG waveform instead of its color:

- Blood glucose level affects blood viscosity and vessel elasticity in small ways, which subtly
  changes the *shape* of the pulse waveform (how sharp the peak is, how fast it decays, the
  ratio between the main pulse and the smaller reflected wave that follows it).
- These shape changes are real, but small, indirect, and easily masked by other things affecting
  the same waveform — blood pressure, body temperature, stress, hydration, age, and skin tone
  (skin pigmentation is a well-documented confounder for light-based sensors generally, including
  medical pulse oximeters).
- Because the relationship is indirect rather than a direct optical read, published approaches
  don't measure glucose from a single formula — they extract dozens of waveform-shape features
  and train a machine learning model to find whatever statistical correlation exists in a
  particular dataset. That means results are dataset-specific, and are honestly reported by
  researchers as promising but not yet a reliable substitute for an actual blood test.

This is exactly why the project's `README.md` frames this as a research prototype rather than a
diagnostic tool: we're going to build the same kind of pipeline real papers use (waveform →
engineered features → ML model → estimate), and we'll report our own model's real accuracy and
limitations honestly, the same way those papers do, rather than overselling it.

## What this means for how we'll build it

1. We need a dataset that already pairs a PPG signal with a true, lab-measured glucose value for
   each recording — we can't just record our own fingertip video and guess the label.
2. Feature *engineering* (Day 8 in the roadmap) matters more here than in problems with a direct
   sensor signal, because we're trying to squeeze an indirect, weak signal out of the waveform
   shape.
3. We evaluate honestly — a model that looks accurate on the exact people it was trained on can
   still fail on a new person's finger, skin tone, or phone camera. We'll keep a proper held-out
   test set and report error, not just a headline "works!" claim.

## Sources

- [Non-invasive Blood-Glucose Estimation Using Smartphone PPG Signals and Subspace KNN Classifier](https://www.semanticscholar.org/paper/Non-invasive-Blood-Glucose-Estimation-Using-PPG-and-Zhang-Zhang/6af3076c39bf530493d11fc7d9d0995a98625e6b)
- [Non-invasive blood glucose monitoring using PPG signals with deep learning models and TinyML — Scientific Reports, 2024](https://www.nature.com/articles/s41598-024-84265-8)
- [Improving non-invasive glucose estimation with monthly calibrated PPG and implicit HbA1c — Communications Medicine, 2025](https://www.nature.com/articles/s43856-025-01210-0)
- [A Non-invasive Blood Glucose Monitoring System Based on Smartphone PPG Signal Processing and Machine Learning — IEEE](https://ieeexplore.ieee.org/iel7/9424/4389054/09005207.pdf)
