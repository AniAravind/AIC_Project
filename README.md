# AIC_Project

First step: turn a song into an STFT spectrogram using Librosa.

## Setup

Use Python 3.9–3.12. From the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Create a spectrogram

```bash
python spectrogram.py "/path/to/song.wav"
```

The image is saved to `outputs/song_spectrogram.png`. WAV is recommended;
other audio formats depend on the decoders available on your system.
For MUSDB18-HQ, use a song's `mixture.wav`. Standard MUSDB18 multistream
STEMS MP4 files need to be decoded into the desired mixture first.

Optional settings:

```bash
python spectrogram.py "data/song.wav" --output outputs/my_plot.png --n-fft 2048 --hop-length 512
```

The script loads the whole song, preserves its original sample rate, and
averages stereo channels to mono. STFT analyzes overlapping Hann-windowed
sections of audio. `n_fft` sets the transform size (and window length here);
`hop_length` sets how many samples to move between sections.

The horizontal axis shows time, the vertical axis shows frequency on a log
scale, and brighter colors indicate stronger magnitudes. Colors show dB
relative to the strongest bin, with an 80 dB display range. A fully silent
file has no meaningful peak-relative contrast.

This is a visualization, not instrument separation. The STFT is a complex
matrix containing magnitude and phase; the PNG displays only magnitude and
is not a replacement for the numerical data needed to train a model.
