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
def data_noisy():
    with open("dataset/morse_dataset_noisy/decodings_noisy.json", "r") as f:
        return json.load(f)


@pytest.fixture
def data_variables():
    with open("dataset/morse_dataset_variables/decodings.json", "r") as f:
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


@pytest.fixture
def decodes_noisy(data_noisy):
    res = []
    for item in data_noisy:
        path = f"dataset/morse_dataset_noisy/{item['file']}"
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


@pytest.fixture
def decodes_variable(data_variables):
    res = []
    for item in data_variables:
        path = f"dataset/morse_dataset_variables/{item['file']}"
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
        pytest.fail(f"{len(errors)} decoding errors found. Count: {len(decodes)}")


def test_noisy_dataset_decoding(decodes_noisy):
    errors = []
    for decoded, expected, path in decodes_noisy:
        print(f"Checking: {path}")
        if decoded == expected:
            print(f"[OK] {path}  expected {expected}, got {decoded}")

        else:
            errors.append(f"[{path}] expected {expected}, got {decoded}")

    if errors:
        print("\n".join(errors))
        pytest.fail(f"{len(errors)} decoding errors found. Count: {len(decodes_noisy)}")


def test_noisy_dataset_variable(decodes_variable):
    errors = []
    for decoded, expected, path in decodes_variable:
        print(f"Checking: {path}")
        if decoded == expected:
            print(f"[OK] {path}  expected {expected}, got {decoded}")

        else:
            errors.append(f"[{path}] expected {expected}, got {decoded}")

    if errors:
        print("\n".join(errors))
        pytest.fail(f"{len(errors)} decoding errors found. Count: {len(decodes_variable)}")
