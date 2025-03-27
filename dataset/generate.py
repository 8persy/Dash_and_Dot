import numpy as np
import soundfile as sf
from tqdm import tqdm  # Для прогресс-бара
import os

# Настройки датасета
DATASET_DIR = "morse_dataset"
os.makedirs(DATASET_DIR, exist_ok=True)

SAMPLE_RATE = 8000
TONE_FREQ = 600
DOT_DURATION = 0.1
NUM_SAMPLES = 1000  # Количество примеров

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


def generate_morse_audio(text, sample_rate, tone_freq, dot_duration):
    """Генерация аудиосигнала из текста."""
    t_dot = np.linspace(0, dot_duration, int(sample_rate * dot_duration), False)
    tone_dot = np.sin(2 * np.pi * tone_freq * t_dot)
    tone_dash = np.sin(
        2 * np.pi * tone_freq * np.linspace(0, 3 * dot_duration, int(sample_rate * 3 * dot_duration), False))
    silence = np.zeros(int(sample_rate * dot_duration))

    signal = []
    for char in text.upper():
        if char in MORSE_CODE:
            for symbol in MORSE_CODE[char]:
                signal.extend(tone_dot if symbol == '.' else tone_dash)
                signal.extend(silence)  # Пауза между символами
            signal.extend(silence * 2)  # Пауза между словами
    return np.array(signal)


# Генерация датасета
metadata = []
for i in tqdm(range(NUM_SAMPLES)):
    # Случайный текст (3-8 символов)
    length = np.random.randint(3, 9)
    text = ''.join(np.random.choice(list(MORSE_CODE.keys()), size=length))

    # Генерация аудио
    audio = generate_morse_audio(text, SAMPLE_RATE, TONE_FREQ, DOT_DURATION)

    # Сохранение
    filename = f"morse_{i:04d}.wav"
    sf.write(os.path.join(DATASET_DIR, filename), audio, SAMPLE_RATE)
    metadata.append(f"{filename},{text}\n")

# Сохранение метаданных
with open(os.path.join(DATASET_DIR, "labels.csv"), "w") as f:
    f.write("filename,text\n")
    f.writelines(metadata)

print(f"Датасет создан в {DATASET_DIR}")