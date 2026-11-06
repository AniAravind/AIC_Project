"""Create a magnitude STFT spectrogram from an audio file."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Save images without requiring a desktop window.
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("song", type=Path, help="Input audio file (WAV recommended)")
    parser.add_argument("--output", type=Path, help="Output PNG path")
    parser.add_argument("--n-fft", type=int, default=2048)
    parser.add_argument("--hop-length", type=int, default=512)
    args = parser.parse_args()
    if not args.song.is_file():
        parser.error(f"Audio file does not exist: {args.song}")
    if args.n_fft < 2 or not 1 <= args.hop_length <= args.n_fft:
        parser.error("Require n-fft >= 2 and 1 <= hop-length <= n-fft")

    # Keep the original sample rate; average stereo channels for this first plot.
    try:
        audio, sample_rate = librosa.load(args.song, sr=None, mono=True)
    except Exception as exc:
        parser.error(f"Could not read audio: {exc}")
    if audio.size == 0 or not np.isfinite(audio).all():
        parser.error("Audio must contain nonempty, finite samples")

    # STFT retains magnitude AND phase. Only magnitude is used for this image.
    stft = librosa.stft(audio, n_fft=args.n_fft, hop_length=args.hop_length)
    magnitude = np.abs(stft)
    # Relative dB makes quieter details visible; the loudest bin is 0 dB.
    magnitude_db = librosa.amplitude_to_db(magnitude, ref=np.max, top_db=80)

    fig, ax = plt.subplots(figsize=(12, 5), layout="constrained")
    image = librosa.display.specshow(
        magnitude_db, sr=sample_rate, n_fft=args.n_fft,
        hop_length=args.hop_length, x_axis="time", y_axis="log", ax=ax,
        vmin=-80, vmax=0,
    )
    ax.set_title(f"STFT spectrogram — {args.song.name}")
    fig.colorbar(image, ax=ax, format="%+2.0f dB", label="Magnitude relative to peak")
    output = args.output or Path("outputs") / f"{args.song.stem}_spectrogram.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=160, format="png")
    plt.close(fig)
    print(f"Audio: {sample_rate} Hz, {len(audio) / sample_rate:.2f} seconds (mono)")
    print(f"STFT: {stft.shape[0]} frequency bins × {stft.shape[1]} time frames")
    print(f"Saved: {output.resolve()}")


if __name__ == "__main__":
    main()
