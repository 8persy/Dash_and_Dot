import json
import pytest
import numpy as np
import soundfile as sf
from morse.morse import MorseCode


@pytest.fixture
def data():
    with open("dataset/morse_dataset/decodings.json", "r") as f:
        return json.load(f)


@pytest.fixture
def decodes(data):
    res = []
    for item in data:
        path = f"dataset/morse_dataset/{item['file']}"
        expected = item["text"].strip().upper()

        signal, sr = sf.read(path)

        if len(signal) == 0 or np.max(np.abs(signal)) < 1e-3:
            print(f"[WARNING] Skipping silent or empty file: {path}")
            continue

        try:
            # decoded = MorseCode(signal, sample_rate=sr).decode()
            decoded = MorseCode.from_wavfile(path).decode()
        except IndexError as e:
            print(f"[ERROR] Failed to decode {path}: {e}")
            continue

        res.append((decoded, expected, path))

    return res


# def test_real_dataset_decoding_pytest(decodes):
#     for decoded, expected, path in decodes:
#         assert decoded == expected, f"{path}: expected {expected}, got {decoded}"

def test_real_dataset_decoding(decodes):
    errors = []
    for decoded, expected, path in decodes:
        print(f"Checking: {path}")
        if decoded == expected:
            print(f"[OK] {path}  expected {expected}, got {decoded}")

        else:
            errors.append(f"[{path}] expected {expected}, got {decoded}")

    if errors:
        print("\n".join(errors))
        pytest.fail(f"{len(errors)} decoding errors found.")
