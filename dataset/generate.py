import os
import numpy as np
import soundfile as sf
import json
from tqdm import tqdm

# Настройки
DATASET_DIR = "morse_dataset"
os.makedirs(DATASET_DIR, exist_ok=True)

SAMPLE_RATE = 8000
TONE_FREQ = 600
FIXED_DOT_DURATION = 0.1
SPEEDS = [10, 25, 50, 65, 80]
SAMPLES_PER_SPEED = 100

# Алфавит Морзе
MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', ' ': '/'
}


def text_to_morse(text):
    return ' '.join([MORSE_CODE[char] for char in text.upper() if char in MORSE_CODE])


def generate_morse_audio(text, speed_factor=1.0):
    t_dot = np.linspace(0, FIXED_DOT_DURATION, int(SAMPLE_RATE * FIXED_DOT_DURATION), False)
    tone_dot = np.sin(2 * np.pi * TONE_FREQ * t_dot)
    tone_dash = np.sin(
        2 * np.pi * TONE_FREQ * np.linspace(0, 3 * FIXED_DOT_DURATION, int(SAMPLE_RATE * 3 * FIXED_DOT_DURATION),
                                            False))

    intra_pause = np.zeros(int(SAMPLE_RATE * FIXED_DOT_DURATION / speed_factor))
    inter_pause = np.zeros(int(SAMPLE_RATE * 3 * FIXED_DOT_DURATION / speed_factor))

    signal = []
    for char in text.upper():
        if char in MORSE_CODE:
            code = MORSE_CODE[char]
            for symbol in code:
                signal.extend(tone_dot if symbol == '.' else tone_dash)
                signal.extend(intra_pause)
            signal.extend(inter_pause if char != ' ' else intra_pause * 7)
    return np.array(signal)


# Список для хранения данных
dataset = []

for wpm in tqdm(SPEEDS, desc="Generating"):
    speed_factor = wpm / 20

    for i in range(SAMPLES_PER_SPEED):
        length = np.random.randint(5, 9)
        text = ''.join(np.random.choice(list(MORSE_CODE.keys()), size=length))
        morse_code = text_to_morse(text)

        audio = generate_morse_audio(text, speed_factor)
        filename = f"morse_{wpm}wpm_{i:04d}.wav"
        sf.write(os.path.join(DATASET_DIR, filename), audio, SAMPLE_RATE)

        dataset.append({
            "file": filename,
            "wpm": wpm,
            "text": text,
            "code": morse_code
        })

# Сохраняем в JSON
with open(os.path.join(DATASET_DIR, "decodings.json"), "w") as f:
    json.dump(dataset, f, indent=2)

print(f"\nDataset generated in {DATASET_DIR}")
print(f"Total files: {len(dataset)}")
print(f"Decodings saved to decodings.json")