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
