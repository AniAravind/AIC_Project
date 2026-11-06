"""Reconstruct a mono WAV from the numerical STFT archive, not its PNG preview."""

import argparse
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf


def reconstruct(path):
    """Load a spectrogram.py archive and invert with its original settings."""
    with np.load(path, allow_pickle=False) as data:
        stft = data["stft"]
        sample_rate = int(data["sample_rate"].item())
        length = int(data["length"].item())
        n_fft = int(data["n_fft"].item())
        hop_length = int(data["hop_length"].item())
        window = str(data["window"].item())
        center = bool(data["center"].item())
    if sample_rate <= 0 or length <= 0 or n_fft < 2:
        raise ValueError("Invalid sample rate, audio length, or FFT size")
    if not 1 <= hop_length <= n_fft or window != "hann" or not center:
        raise ValueError("Unsupported STFT settings")
    if (stft.ndim != 2 or stft.shape[0] != n_fft // 2 + 1
            or stft.shape[1] != 1 + length // hop_length
            or not np.iscomplexobj(stft) or not np.isfinite(stft).all()):
        raise ValueError("Archive must contain a finite complex STFT with matching dimensions")
    audio = librosa.istft(
        stft, n_fft=n_fft, hop_length=hop_length, window=window,
        center=center, length=length,
    )
    return audio, sample_rate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spectrogram", type=Path, help=".npz file from spectrogram.py")
    parser.add_argument("--output", type=Path, help="Reconstructed .wav file")
    args = parser.parse_args()
    if args.spectrogram.suffix.lower() != ".npz":
        parser.error("Use the .npz STFT archive. A PNG lacks the original phase and numerical precision.")
    output = args.output or args.spectrogram.with_name(
        args.spectrogram.stem + "_reconstructed.wav"
    )
    if output.suffix.lower() != ".wav":
        parser.error("Output must have a .wav extension")
    try:
        audio, sample_rate = reconstruct(args.spectrogram)
        output.parent.mkdir(parents=True, exist_ok=True)
        # Floating-point WAV avoids clipping/quantization during this round trip.
        sf.write(output, audio, sample_rate, format="WAV", subtype="FLOAT")
    except (OSError, ValueError, KeyError, RuntimeError) as exc:
        parser.error(f"Could not reconstruct audio: {exc}")
    print(f"Saved: {output.resolve()}")
    print(f"Audio: {sample_rate} Hz, {len(audio) / sample_rate:.2f} seconds (mono)")


if __name__ == "__main__":
    main()
