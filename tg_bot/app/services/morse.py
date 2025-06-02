import numpy as np


MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', '0': '-----', ',': '--..--',
    '.': '.-.-.-', '?': '..--..', '/': '-..-.', '-': '-....-',
    '(': '-.--.', ')': '-.--.-', ' ': ' '
}

REVERSE_MORSE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}


def text_to_morse(text: str) -> str:
    morse_code = []
    for char in text.upper():
        if char in MORSE_CODE_DICT:
            morse_code.append(MORSE_CODE_DICT[char])
        else:
            continue
    return ' '.join(morse_code)


def morse_to_text(morse_code: str) -> str:
    text = []
    print(morse_code.replace('   ', '  ').split(' '))
    for code in morse_code.replace('   ', '  ').split(' '):
        if code in REVERSE_MORSE_DICT:
            text.append(REVERSE_MORSE_DICT[code])
        elif code == '':
            text.append(' ')
    return ''.join(text)


def generate_morse_audio(
        text, speed_factor=1.0,
        dot_duration=0.1,
        tone_freq=600,
        sample_rate=8000):
    t_dot = np.linspace(0, dot_duration, int(
        sample_rate * dot_duration), False)
    tone_dot = np.sin(2 * np.pi * tone_freq * t_dot)
    tone_dash = np.sin(
        2 * np.pi * tone_freq * np.linspace(
            0, 3 * dot_duration,
            int(sample_rate * 3 * dot_duration),
            False))

    intra_pause = np.zeros(int(sample_rate * dot_duration / speed_factor))
    inter_pause = np.zeros(int(sample_rate * 3 * dot_duration / speed_factor))

    signal = []
    for char in text.upper():
        if char in MORSE_CODE_DICT:
            code = MORSE_CODE_DICT[char]
            if char == ' ':
                signal.extend(intra_pause * 7)
                continue
            for symbol in code:
                signal.extend(tone_dot if symbol == '.' else tone_dash)
                signal.extend(intra_pause)
            signal.extend(inter_pause if char != ' ' else intra_pause * 7)
    return np.array(signal)
