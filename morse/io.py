"""Input/output"""

import os
import wave

import numpy as np
from pydub import AudioSegment


def read_wave(file: os.PathLike) -> tuple[int, np.ndarray]:
    """Read WAV file into numpy array

    NOTE: only mono audio is supported. Multi-channel audio is interlaced,
    and would need to be de-interlaced into a 2D array.

    Args:
        file (os.PathLike): input WAV file

    Returns:
        tuple[int, np.ndarray]: sample rate, data

        Data type is determined from the file; for 16bit PCM (as in competition),
        the output data type is int16. For mono audio, return shape is 1D array.
    """
    with wave.open(str(file), "rb") as wav_file:
        buffer = wav_file.readframes(wav_file.getnframes())
        sample_width_bits = wav_file.getsampwidth() * 8
        _dtype = "uint8" if sample_width_bits == 8 else f"int{sample_width_bits}"
        data = np.frombuffer(buffer, dtype=_dtype)
        if wav_file.getnchannels() > 1:
            raise NotImplementedError(
                "Cannot read WAV file with more than one channels, found: "
                + str(wav_file.getnchannels())
            )
        return wav_file.getframerate(), data


def read_mp3(file: os.PathLike) -> tuple[int, np.ndarray]:
    """
    Read MP3 file into numpy array.

    NOTE: Only mono audio is supported. Stereo or multi-channel audio will raise an error.

    Args:
        file (os.PathLike): input MP3 file

    Returns:
        tuple[int, np.ndarray]: sample rate, data

        Output data is int16 numpy array, 1D for mono audio.
    """
    audio = AudioSegment.from_file(file, format="mp3")

    if audio.channels > 1:
        raise NotImplementedError(
            f"Cannot read MP3 file with more than one channel, found: {audio.channels}"
        )

    samples = np.array(audio.get_array_of_samples(), dtype=np.int16)
    return audio.frame_rate, samples


def convert_wav_to_mp3(wav_path: str, mp3_path: str, bitrate: str = "192k") -> None:
    """
    Convert a WAV file to MP3 format.

    Args:
        wav_path (str): Path to the input WAV file.
        mp3_path (str): Path where the MP3 file will be saved.
        bitrate (str): Bitrate for the MP3 file (e.g., "192k").
    """
    audio = AudioSegment.from_wav(wav_path)
    audio.export(mp3_path, format="mp3", bitrate=bitrate)
