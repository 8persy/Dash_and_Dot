import os
import numpy as np
import soundfile as sf
import json
from tqdm import tqdm

# Папки для сохранения
DATASET_DIR = "morse_dataset"
NOISY_DATASET_DIR = "morse_dataset_noisy"
os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(NOISY_DATASET_DIR, exist_ok=True)

# Настройки
SAMPLE_RATE = 8000
TONE_FREQ = 600
FIXED_DOT_DURATION = 0.1
SPEEDS = [10, 25, 50, 65, 80]
SAMPLES_PER_SPEED = 3
NOISE_LEVELS = [0.01, 0.02, 0.05, 0.07, 0.1]
DOT_DURATIONS = [0.05, 0.07, 0.1, 0.11, 0.12, 0.15]

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


def generate_morse_audio(text, speed_factor=1.0, dot_duration=FIXED_DOT_DURATION):
    t_dot = np.linspace(0, dot_duration, int(SAMPLE_RATE * dot_duration), False)
    tone_dot = np.sin(2 * np.pi * TONE_FREQ * t_dot)
    tone_dash = np.sin(
        2 * np.pi * TONE_FREQ * np.linspace(0, 3 * dot_duration, int(SAMPLE_RATE * 3 * dot_duration), False)
    )

    intra_pause = np.zeros(int(SAMPLE_RATE * dot_duration / speed_factor))
    inter_pause = np.zeros(int(SAMPLE_RATE * 3 * dot_duration / speed_factor))

    signal = []
    for char in text.upper():
        if char in MORSE_CODE:
            code = MORSE_CODE[char]
            if char == ' ':
                signal.extend(intra_pause * 7)
                continue
            for symbol in code:
                signal.extend(tone_dot if symbol == '.' else tone_dash)
                signal.extend(intra_pause)
            signal.extend(inter_pause if char != ' ' else intra_pause * 7)

    return np.array(signal)


def add_noise(audio, noise_level=0.02):
    noise = np.random.normal(0, 1, len(audio))
    noisy_audio = audio + noise_level * noise
    noisy_audio = noisy_audio / np.max(np.abs(noisy_audio))  # нормализация
    return noisy_audio


def generate_dataset():
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


def generate_noisy_dataset(num_samples=100, noise_levels=None):
    if noise_levels is None:
        noise_levels = NOISE_LEVELS
    noisy_dataset = []

    for wpm in SPEEDS:
        speed_factor = wpm / 20

        for i in range(num_samples):
            # Генерация случайного текста
            length = np.random.randint(5, 9)
            text = ''.join(np.random.choice(list(MORSE_CODE.keys()), size=length))
            morse_code = text_to_morse(text)

            # Генерация чистого аудио
            audio = generate_morse_audio(text, speed_factor)
            filename = f"morse_{wpm}wpm_{i:04d}.wav"
            filepath = os.path.join(NOISY_DATASET_DIR, filename)
            sf.write(filepath, audio, SAMPLE_RATE)

            # Добавление шума на разные уровни
            for level in noise_levels:
                noisy_audio = add_noise(audio, noise_level=level)
                noisy_filename = filename.replace(".wav", f"_noisy_{int(level * 1000):03d}.wav")
                noisy_filepath = os.path.join(NOISY_DATASET_DIR, noisy_filename)
                sf.write(noisy_filepath, noisy_audio, SAMPLE_RATE)

                # Сохраняем информацию о зашумлённом файле
                noisy_entry = {
                    "file": noisy_filename,
                    "wpm": wpm,
                    "text": text,
                    "code": morse_code,
                    "noisy": True,
                    "noise_level": level
                }
                noisy_dataset.append(noisy_entry)

    # Сохраняем информацию о зашумлённом датасете
    with open(os.path.join(NOISY_DATASET_DIR, "decodings_noisy.json"), "w") as f:
        json.dump(noisy_dataset, f, indent=2)


def generate_variable_dataset():
    variable_dataset = []
    DATASET_DIR = 'morse_dataset_variables'

    for duration in DOT_DURATIONS:
        for i in range(SAMPLES_PER_SPEED):
            length = np.random.randint(5, 9)
            text = ''.join(np.random.choice(list(MORSE_CODE.keys()), size=length))
            morse_code = text_to_morse(text)

            audio = generate_morse_audio(text=text, dot_duration=duration)
            filename = f"morse_{duration}dur_{i:04d}.wav"
            sf.write(os.path.join(DATASET_DIR, filename), audio, SAMPLE_RATE)

            variable_dataset.append({
                "file": filename,
                "duration": duration,
                "text": text,
                "code": morse_code
            })
    with open(os.path.join(DATASET_DIR, "decodings.json"), "w") as f:
        json.dump(variable_dataset, f, indent=2)
